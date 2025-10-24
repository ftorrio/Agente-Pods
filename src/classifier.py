# -*- coding: utf-8 -*-
"""
Clasificador de PODs
Determina la categoría de cada documento POD según los criterios establecidos
"""

from typing import Dict, Any, List
from loguru import logger

from detectors.signature_detector import SignatureDetector
from detectors.stamp_detector import StampDetector
from detectors.legibility_analyzer import LegibilityAnalyzer
from detectors.annotation_detector import AnnotationDetector

# Importar sistema de notificaciones si está disponible
try:
    from notifications import NotificationSystem
    NOTIFICATIONS_AVAILABLE = True
except ImportError:
    NOTIFICATIONS_AVAILABLE = False
    logger.warning("Sistema de notificaciones no disponible")

# Importar Gemini AI si está disponible
try:
    from gemini_analyzer import GeminiPODAnalyzer, get_gemini_api_key_from_config
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("Gemini AI no disponible")


class PODClassifier:
    """
    Clase principal para clasificar documentos POD
    
    Categorías:
    1. Poco Legible - Campos no distinguibles
    2. Sin Acuse - Sin firma, sello o anotaciones
    3. Incorrecto - Documento cortado o parcial
    4. Con Anotaciones - Tiene comentarios manuscritos
    5. OK - Válido con firma/sello del cliente
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa el clasificador
        
        Args:
            config: Diccionario de configuración
        """
        self.config = config
        self.classifications = config['classifications']
        
        # Inicializar detectores
        self.signature_detector = SignatureDetector(config)
        self.stamp_detector = StampDetector(config)
        self.legibility_analyzer = LegibilityAnalyzer(config)
        self.annotation_detector = AnnotationDetector(config)
        
        # Inicializar sistema de notificaciones
        if NOTIFICATIONS_AVAILABLE:
            self.notification_system = NotificationSystem()
        else:
            self.notification_system = None
        
        # Inicializar Gemini AI
        if GEMINI_AVAILABLE:
            api_key = get_gemini_api_key_from_config()
            self.gemini_analyzer = GeminiPODAnalyzer(api_key)
            if self.gemini_analyzer.enabled:
                logger.info("Gemini AI activado como revisor inteligente")
            else:
                self.gemini_analyzer = None
                logger.warning("Gemini AI no pudo inicializarse (falta API key)")
        else:
            self.gemini_analyzer = None
        
        logger.info("Clasificador de PODs inicializado")
    
    def classify_document(self, page_data: Dict[str, Any], 
                         zones: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clasifica un documento POD completo
        
        Args:
            page_data: Datos de la página procesada
            zones: Zonas de interés extraídas
            
        Returns:
            Diccionario con la clasificación y detalles
        """
        logger.info(f"Clasificando documento: {page_data['source_file']}")
        
        # Estructura del resultado
        result = {
            'source_file': page_data['source_file'],
            'page_number': page_data['page_number'],
            'classification': None,
            'classification_code': None,
            'confidence': 0.0,
            'is_valid': False,
            'details': {},
            'issues': [],
            'recommendations': []
        }
        
        # PASO 1: Analizar legibilidad
        legibility = self.legibility_analyzer.analyze_legibility(page_data)
        result['details']['legibility'] = legibility
        
        # PASO 2: Verificar si está completo
        is_complete = self.legibility_analyzer.is_document_complete(page_data['original_image'])
        result['details']['is_complete'] = is_complete
        
        # PASO 3: Detectar firmas
        signatures = self.signature_detector.detect_signatures(
            page_data['processed_image'], 
            zones
        )
        result['details']['signatures'] = signatures
        has_valid_signature = self.signature_detector.has_valid_signature(signatures)
        
        # PASO 4: Detectar sellos
        stamps = self.stamp_detector.detect_stamps(page_data['processed_image'])
        result['details']['stamps'] = stamps
        has_valid_stamp = self.stamp_detector.has_valid_stamp(stamps)
        
        # PASO 5: Detectar anotaciones
        annotations = self.annotation_detector.detect_annotations(page_data['processed_image'])
        result['details']['annotations'] = annotations
        
        # CLASIFICACIÓN SEGÚN PRIORIDAD
        
        # 1. INCORRECTO - Documento cortado o parcialmente digitalizado
        if not is_complete:
            result['classification'] = self.classifications['INCORRECTO']
            result['classification_code'] = 'INCORRECTO'
            result['is_valid'] = False
            result['confidence'] = 0.9
            result['issues'].append("Documento no completamente digitalizado (cortado o parcial)")
            result['recommendations'].append("Re-digitalizar el documento completo")
            logger.warning(f"Clasificado como INCORRECTO: {page_data['source_file']}")
            return result
        
        # 2. POCO LEGIBLE - Campos no distinguibles
        if not legibility['is_legible']:
            result['classification'] = self.classifications['POCO_LEGIBLE']
            result['classification_code'] = 'POCO_LEGIBLE'
            result['is_valid'] = False
            result['confidence'] = 0.85
            result['issues'].extend(legibility['issues'])
            result['recommendations'].append("Mejorar la calidad de digitalización")
            result['recommendations'].append(f"Campos faltantes: {', '.join(legibility['fields_missing'])}")
            logger.warning(f"Clasificado como POCO LEGIBLE: {page_data['source_file']}")
            return result
        
        # 3. OK - Válido con firma y nombre del cliente o sello válido
        if has_valid_signature or has_valid_stamp:
            result['classification'] = self.classifications['OK']
            result['classification_code'] = 'OK'
            result['is_valid'] = True
            result['confidence'] = 0.95
            
            if has_valid_signature:
                result['issues'].append(f"Firma válida detectada ({len(signatures)} firma(s))")
            if has_valid_stamp:
                result['issues'].append(f"Sello válido del cliente detectado ({len([s for s in stamps if s['is_valid']])} sello(s))")
            
            # Verificar si también tiene anotaciones
            if annotations['has_annotations']:
                if annotations['sentiment'] == 'negative':
                    result['issues'].append("ADVERTENCIA: Contiene anotaciones negativas (posible reclamación)")
                    result['recommendations'].append("Revisar manualmente las anotaciones")
                elif annotations['sentiment'] == 'positive':
                    result['issues'].append("Contiene anotaciones positivas confirmando recepción")
            
            logger.info(f"Clasificado como OK: {page_data['source_file']}")
            return result
        
        # 4. CON ANOTACIONES - Tiene comentarios manuscritos
        if annotations['has_annotations']:
            result['classification'] = self.classifications['CON_ANOTACIONES']
            result['classification_code'] = 'CON_ANOTACIONES'
            result['confidence'] = 0.8
            
            if annotations['sentiment'] == 'positive':
                result['is_valid'] = True
                result['issues'].append("Anotaciones confirman recepción del producto")
                result['recommendations'].append("Revisar anotaciones para confirmar")
            elif annotations['sentiment'] == 'negative':
                result['is_valid'] = False
                result['issues'].append("Anotaciones indican posible reclamación")
                result['recommendations'].append("Revisión urgente requerida - posible problema con la entrega")
            else:
                result['is_valid'] = False
                result['issues'].append("Anotaciones presentes pero sentimiento no claro")
                result['recommendations'].append("Revisión manual requerida para interpretar anotaciones")
            
            logger.info(f"Clasificado como CON ANOTACIONES ({annotations['sentiment']}): {page_data['source_file']}")
            return result
        
        # 5. SIN ACUSE - No tiene firma, sello ni anotaciones
        result['classification'] = self.classifications['SIN_ACUSE']
        result['classification_code'] = 'SIN_ACUSE'
        result['is_valid'] = False
        result['confidence'] = 0.9
        result['issues'].append("Documento sin evidencia de acuse (sin firma, sello o anotaciones)")
        result['recommendations'].append("Solicitar documento con firma o sello del cliente")
        logger.warning(f"Clasificado como SIN ACUSE: {page_data['source_file']}")
        
        # ========== GEMINI AI COMO REVISOR INTELIGENTE ==========
        if self.gemini_analyzer:
            try:
                logger.info("Activando Gemini AI como revisor inteligente...")
                image_path = page_data['source_file']
                
                # 1. Análisis de manuscritos críticos (si hay anotaciones o baja confianza)
                if result['details']['annotations']['detected'] or result['confidence'] < 0.7:
                    logger.info("Analizando manuscritos con Gemini...")
                    manuscripts = self.gemini_analyzer.analyze_critical_annotations(image_path)
                    result['details']['gemini_manuscripts'] = manuscripts
                    
                    # Si Gemini detecta reclamación NEGATIVA urgente
                    if manuscripts.get('has_annotations') and manuscripts.get('sentiment') == 'negative':
                        if manuscripts.get('urgency') == 'urgent':
                            result['classification'] = self.classifications['CON_ANOTACIONES']
                            result['classification_code'] = 'CON_ANOTACIONES'
                            result['is_valid'] = False
                            result['issues'].append(f"URGENTE - Reclamación detectada por Gemini: {manuscripts.get('transcription', '')}")
                            logger.critical(f"Gemini detectó reclamación URGENTE en: {page_data['source_file']}")
                
                # 2. Validación de autenticidad de firma (si hay firma detectada)
                if result['details']['signature']['detected']:
                    logger.info("Validando autenticidad de firma con Gemini...")
                    signature_auth = self.gemini_analyzer.validate_signature_authenticity(image_path)
                    result['details']['gemini_signature'] = signature_auth
                    
                    # Si la firma NO es auténtica (es sello o digital)
                    if not signature_auth.get('is_authentic') and signature_auth.get('signature_type') in ['stamp', 'digital']:
                        logger.warning(f"Gemini detectó firma no auténtica: {signature_auth.get('signature_type')}")
                        result['issues'].append(f"Firma detectada como {signature_auth.get('signature_type')} (no manuscrita)")
                        # Reclasificar si era OK solo por la firma
                        if result['classification_code'] == 'OK' and not result['details']['stamp']['detected']:
                            result['classification'] = self.classifications['SIN_ACUSE']
                            result['classification_code'] = 'SIN_ACUSE'
                            result['is_valid'] = False
                            logger.warning("Reclasificado a SIN_ACUSE por firma no auténtica")
                
                # 3. Extracción de campos clave (para datos estructurados)
                logger.info("Extrayendo campos clave con Gemini...")
                key_fields = self.gemini_analyzer.extract_key_fields(image_path)
                result['details']['gemini_fields'] = key_fields
                
                # 4. Clasificación de Gemini (como segundo opinión)
                logger.info("Obteniendo clasificación de Gemini...")
                gemini_classification = self.gemini_analyzer.classify_pod(image_path)
                result['details']['gemini_classification'] = gemini_classification
                
                # Detectar discrepancias entre Tesseract y Gemini
                if 'classification_text' in gemini_classification:
                    gemini_class_text = gemini_classification['classification_text'].upper()
                    if ('OK' in gemini_class_text and result['classification_code'] != 'OK') or \
                       ('SIN ACUSE' in gemini_class_text and result['classification_code'] == 'OK'):
                        result['needs_review'] = True
                        result['review_reason'] = 'Discrepancia entre clasificación OCR y Gemini AI'
                        logger.warning(f"Discrepancia detectada: OCR={result['classification_code']}, Gemini sugiere revisión")
                
                logger.info("Análisis con Gemini completado exitosamente")
                
            except Exception as e:
                logger.error(f"Error en análisis de Gemini: {e}")
                result['details']['gemini_error'] = str(e)
        
        # Generar alertas con sistema de notificaciones
        if self.notification_system:
            self.notification_system.check_and_alert(result)
        
        return result
    
    def get_classification_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Genera un resumen de múltiples clasificaciones
        
        Args:
            results: Lista de resultados de clasificación
            
        Returns:
            Diccionario con estadísticas resumidas
        """
        summary = {
            'total_documents': len(results),
            'valid_documents': 0,
            'invalid_documents': 0,
            'by_classification': {
                'OK': 0,
                'CON_ANOTACIONES': 0,
                'SIN_ACUSE': 0,
                'POCO_LEGIBLE': 0,
                'INCORRECTO': 0
            },
            'validation_rate': 0.0,
            'issues_summary': []
        }
        
        for result in results:
            if result['is_valid']:
                summary['valid_documents'] += 1
            else:
                summary['invalid_documents'] += 1
            
            classification = result['classification_code']
            if classification in summary['by_classification']:
                summary['by_classification'][classification] += 1
        
        # Calcular tasa de validación
        if summary['total_documents'] > 0:
            summary['validation_rate'] = (summary['valid_documents'] / summary['total_documents']) * 100
        
        # Agregar resumen de problemas comunes
        all_issues = []
        for result in results:
            all_issues.extend(result['issues'])
        
        # Contar problemas más comunes
        from collections import Counter
        issue_counts = Counter(all_issues)
        summary['issues_summary'] = [
            {'issue': issue, 'count': count}
            for issue, count in issue_counts.most_common(10)
        ]
        
        return summary

