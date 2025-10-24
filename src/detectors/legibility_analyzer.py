# -*- coding: utf-8 -*-
"""
Analizador de Legibilidad
Determina si un documento POD es legible analizando campos clave
"""

import cv2
import numpy as np
import pytesseract
from typing import Dict, Any, List, Tuple
from loguru import logger
import os

# Configurar ruta de Tesseract si está en la ubicación estándar
if os.path.exists(r"C:\Program Files\Tesseract-OCR\tesseract.exe"):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class LegibilityAnalyzer:
    """
    Clase para analizar la legibilidad de documentos POD
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa el analizador de legibilidad
        
        Args:
            config: Diccionario de configuración
        """
        self.config = config
        self.required_fields = config['required_fields']
        self.min_text_quality = config['thresholds']['min_text_quality']
        self.min_fields_detected = config['thresholds']['min_fields_detected']
        self.blur_threshold = config['thresholds']['blur_threshold']
        self.min_confidence = config['ocr']['min_confidence']
        
        logger.info("Analizador de legibilidad inicializado")
    
    def analyze_legibility(self, page_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analiza la legibilidad de un documento
        
        Args:
            page_data: Datos de la página procesada
            
        Returns:
            Diccionario con resultados del análisis de legibilidad
        """
        results = {
            'is_legible': True,
            'blur_score': page_data['blur_score'],
            'is_blurry': page_data['is_blurry'],
            'fields_detected': [],
            'fields_missing': [],
            'text_quality': 0.0,
            'ocr_confidence': 0.0,
            'issues': []
        }
        
        # 1. Verificar desenfoque
        if page_data['is_blurry']:
            results['is_legible'] = False
            results['issues'].append(f"Imagen borrosa (score: {page_data['blur_score']:.1f})")
        
        # 2. Extraer y analizar texto
        text_data = self._extract_text_with_confidence(page_data['processed_image'])
        results['ocr_confidence'] = text_data['mean_confidence']
        
        # 3. Detectar campos requeridos
        detected_fields, missing_fields = self._detect_required_fields(text_data['text'])
        results['fields_detected'] = detected_fields
        results['fields_missing'] = missing_fields
        
        # 4. Calcular calidad de texto
        text_quality = self._calculate_text_quality(
            text_data['text'],
            text_data['mean_confidence'],
            len(detected_fields)
        )
        results['text_quality'] = text_quality
        
        # 5. Verificar si cumple con criterios mínimos
        if len(detected_fields) < self.min_fields_detected:
            results['is_legible'] = False
            results['issues'].append(
                f"Campos insuficientes detectados: {len(detected_fields)}/{self.min_fields_detected}"
            )
        
        if text_quality < self.min_text_quality:
            results['is_legible'] = False
            results['issues'].append(
                f"Calidad de texto baja: {text_quality:.2f}/{self.min_text_quality}"
            )
        
        if text_data['mean_confidence'] < self.min_confidence:
            results['is_legible'] = False
            results['issues'].append(
                f"Confianza OCR baja: {text_data['mean_confidence']:.1f}/{self.min_confidence}"
            )
        
        logger.info(f"Legibilidad: {'SÍ' if results['is_legible'] else 'NO'} - "
                   f"Campos: {len(detected_fields)}/{len(self.required_fields)}")
        
        return results
    
    def _extract_text_with_confidence(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Extrae texto de la imagen con información de confianza
        
        Args:
            image: Imagen del documento
            
        Returns:
            Diccionario con texto y confianza
        """
        try:
            # Configurar OCR para español
            config = f"--psm {self.config['ocr']['psm']} --oem {self.config['ocr']['oem']}"
            
            # Extraer texto con detalles
            data = pytesseract.image_to_data(
                image, 
                lang=self.config['ocr']['language'],
                config=config,
                output_type=pytesseract.Output.DICT
            )
            
            # Filtrar palabras con confianza suficiente
            valid_confidences = [
                float(conf) for conf in data['conf'] 
                if conf != '-1' and float(conf) > 0
            ]
            
            mean_conf = np.mean(valid_confidences) if valid_confidences else 0
            
            # Extraer todo el texto
            full_text = pytesseract.image_to_string(
                image,
                lang=self.config['ocr']['language'],
                config=config
            )
            
            return {
                'text': full_text.lower(),
                'mean_confidence': mean_conf,
                'word_count': len([w for w in data['text'] if w.strip()])
            }
            
        except Exception as e:
            logger.error(f"Error en OCR: {e}")
            return {
                'text': '',
                'mean_confidence': 0,
                'word_count': 0
            }
    
    def _detect_required_fields(self, text: str) -> Tuple[List[str], List[str]]:
        """
        Detecta qué campos requeridos están presentes en el texto
        
        Args:
            text: Texto extraído del documento
            
        Returns:
            Tupla (campos_detectados, campos_faltantes)
        """
        detected = []
        missing = []
        
        # Palabras clave alternativas para cada campo
        field_keywords = {
            'factura': ['factura', 'fact', 'invoice', 'no.', 'núm', 'numero'],
            'cliente': ['cliente', 'client', 'razón social', 'razon social'],
            'pedido': ['pedido', 'orden', 'order', 'o.c.', 'oc'],
            'producto': ['producto', 'material', 'descripción', 'articulo', 'artículo'],
            'firma': ['firma', 'recibí', 'recibi', 'nombre', 'autoriza']
        }
        
        for field in self.required_fields:
            keywords = field_keywords.get(field, [field])
            found = False
            
            for keyword in keywords:
                if keyword in text:
                    detected.append(field)
                    found = True
                    break
            
            if not found:
                missing.append(field)
        
        return detected, missing
    
    def _calculate_text_quality(self, text: str, ocr_confidence: float, 
                                fields_count: int) -> float:
        """
        Calcula una puntuación de calidad del texto
        
        Args:
            text: Texto extraído
            ocr_confidence: Confianza media del OCR
            fields_count: Número de campos detectados
            
        Returns:
            Puntuación de calidad (0-1)
        """
        factors = []
        
        # Factor 1: Confianza OCR normalizada
        conf_factor = ocr_confidence / 100.0
        factors.append(conf_factor)
        
        # Factor 2: Proporción de campos detectados
        field_factor = fields_count / len(self.required_fields)
        factors.append(field_factor)
        
        # Factor 3: Cantidad de texto (más texto suele ser mejor)
        word_count = len(text.split())
        text_amount_factor = min(1.0, word_count / 50)  # 50 palabras = 1.0
        factors.append(text_amount_factor)
        
        # Factor 4: Proporción de caracteres alfanuméricos
        if len(text) > 0:
            alnum_ratio = sum(c.isalnum() or c.isspace() for c in text) / len(text)
            factors.append(alnum_ratio)
        
        # Promedio ponderado
        quality = np.mean(factors)
        return quality
    
    def is_document_complete(self, image: np.ndarray) -> bool:
        """
        Verifica si el documento está completamente digitalizado (no cortado)
        
        Args:
            image: Imagen del documento
            
        Returns:
            True si parece estar completo
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        
        # Verificar bordes (documentos cortados suelen tener bordes negros/blancos irregulares)
        border_size = 10
        
        # Analizar borde superior
        top_border = gray[0:border_size, :]
        # Analizar borde inferior
        bottom_border = gray[h-border_size:h, :]
        # Analizar borde izquierdo
        left_border = gray[:, 0:border_size]
        # Analizar borde derecho
        right_border = gray[:, w-border_size:w]
        
        # Calcular varianza de cada borde (bordes uniformes = posible corte)
        top_var = np.var(top_border)
        bottom_var = np.var(bottom_border)
        left_var = np.var(left_border)
        right_var = np.var(right_border)
        
        # Si algún borde tiene muy poca varianza, puede estar cortado
        min_variance = 100
        
        if any(var < min_variance for var in [top_var, bottom_var, left_var, right_var]):
            logger.warning("Posible documento cortado detectado")
            return False
        
        return True

