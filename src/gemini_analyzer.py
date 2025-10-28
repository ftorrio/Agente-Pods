# -*- coding: utf-8 -*-
"""
Analizador de PODs usando Google Gemini AI
Proporciona análisis inteligente y clasificación avanzada
"""

import os
import base64
from typing import Dict, Any, Optional
from loguru import logger
import google.generativeai as genai


class GeminiPODAnalyzer:
    """
    Analizador de PODs usando Google Gemini
    """
    
    def __init__(self, api_key: str = None, use_pro: bool = False):
        """
        Inicializa el analizador Gemini
        
        Args:
            api_key: API key de Google Gemini
            use_pro: Usar Gemini Pro en lugar de Flash (más preciso, más caro)
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            
            # Seleccionar modelo según configuración
            if use_pro:
                self.model = genai.GenerativeModel('gemini-1.5-pro')
                self.model_name = 'Gemini 1.5 Pro'
                logger.info("Gemini 1.5 PRO inicializado (máxima precisión)")
            else:
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.model_name = 'Gemini 1.5 Flash'
                logger.info("Gemini 1.5 Flash inicializado correctamente")
            
            self.enabled = True
            self.use_pro = use_pro
        else:
            logger.warning("Gemini API key no encontrada - modo deshabilitado")
            self.enabled = False
            self.use_pro = False
    
    def analyze_pod_image(self, image_path: str) -> Dict[str, Any]:
        """
        Analiza un POD completo con Gemini
        
        Args:
            image_path: Ruta a la imagen del POD
            
        Returns:
            Diccionario con análisis completo
        """
        if not self.enabled:
            return {'enabled': False, 'error': 'Gemini no configurado'}
        
        try:
            # Leer imagen
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            # Crear prompt específico para PODs
            prompt = """
Analiza este documento POD (Proof of Delivery / Prueba de Entrega) y responde en español:

1. FIRMA:
   - ¿Tiene firma manuscrita del cliente? (SÍ/NO)
   - ¿Dónde está ubicada? (superior/inferior/izquierda/derecha/centro)
   - ¿Parece auténtica? (SÍ/NO)

2. SELLO:
   - ¿Tiene sello? (SÍ/NO)
   - ¿Qué texto dice el sello?
   - ¿Es sello de cliente o de empresa? (indica si ves "Deacero" o "Ingetek" - son inválidos)

3. CAMPOS CLAVE:
   - Número de Factura: [extraer si visible]
   - Cliente/Razón Social: [extraer si visible]
   - Número de Pedido/Orden: [extraer si visible]
   - Productos/Materiales: [listar si visible]

4. ANOTACIONES MANUSCRITAS:
   - ¿Hay anotaciones/comentarios escritos a mano? (SÍ/NO)
   - ¿Qué dicen? [transcribir]
   - Sentimiento: (POSITIVO si confirma recepción / NEGATIVO si hay reclamación / NEUTRAL)

5. CALIDAD DEL DOCUMENTO:
   - ¿Está completo o cortado? (COMPLETO/CORTADO)
   - ¿Es legible? (SÍ/NO)
   - Calidad general: (EXCELENTE/BUENA/REGULAR/MALA)

6. CLASIFICACIÓN RECOMENDADA:
   Clasifica este POD en UNA de estas categorías:
   - OK: Tiene firma/sello válido del cliente
   - CON ANOTACIONES: Tiene comentarios manuscritos (especifica si positivos o negativos)
   - SIN ACUSE: No tiene firma, sello ni anotaciones
   - POCO LEGIBLE: Campos clave no distinguibles
   - INCORRECTO: Documento cortado o parcial

7. EXPLICACIÓN:
   Explica brevemente por qué elegiste esa clasificación.

Responde en formato claro y estructurado.
            """
            
            # Enviar a Gemini
            response = self.model.generate_content([prompt, image_data])
            
            analysis = {
                'enabled': True,
                'raw_response': response.text,
                'confidence': 'high',  # Gemini generalmente tiene alta confianza
                'analyzed': True
            }
            
            # Parsear respuesta (simple)
            self._parse_gemini_response(analysis, response.text)
            
            logger.info("Análisis Gemini completado")
            return analysis
            
        except Exception as e:
            logger.error(f"Error en análisis Gemini: {e}")
            return {
                'enabled': True,
                'error': str(e),
                'analyzed': False
            }
    
    def _parse_gemini_response(self, analysis: Dict, response_text: str):
        """
        Parsea la respuesta de Gemini en campos estructurados
        """
        text_lower = response_text.lower()
        
        # Detectar clasificación recomendada
        if 'clasificación' in text_lower or 'clasificacion' in text_lower:
            if 'ok' in text_lower and 'sin acuse' not in text_lower:
                analysis['gemini_classification'] = 'OK'
            elif 'con anotaciones' in text_lower:
                analysis['gemini_classification'] = 'CON_ANOTACIONES'
            elif 'sin acuse' in text_lower:
                analysis['gemini_classification'] = 'SIN_ACUSE'
            elif 'poco legible' in text_lower:
                analysis['gemini_classification'] = 'POCO_LEGIBLE'
            elif 'incorrecto' in text_lower:
                analysis['gemini_classification'] = 'INCORRECTO'
        
        # Detectar firma
        analysis['gemini_has_signature'] = 'firma' in text_lower and ('sí' in text_lower or 'si ' in text_lower)
        
        # Detectar sello
        analysis['gemini_has_stamp'] = 'sello' in text_lower and ('sí' in text_lower or 'si ' in text_lower)
        
        # Detectar sentimiento
        if 'positivo' in text_lower:
            analysis['gemini_sentiment'] = 'positive'
        elif 'negativo' in text_lower:
            analysis['gemini_sentiment'] = 'negative'
        else:
            analysis['gemini_sentiment'] = 'neutral'
    
    def validate_signature(self, image_path: str) -> Dict[str, Any]:
        """
        Valida específicamente si hay firma usando Gemini
        """
        if not self.enabled:
            return {'enabled': False}
        
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            prompt = """
¿Este documento tiene una firma manuscrita real del cliente?

Responde SOLO:
- SÍ - si hay una firma manuscrita clara
- NO - si no hay firma
- DUDOSO - si no estás seguro

Luego explica brevemente por qué.
            """
            
            response = self.model.generate_content([prompt, image_data])
            
            result = {
                'enabled': True,
                'response': response.text,
                'has_signature': 'sí' in response.text.lower() or 'si' in response.text.lower(),
                'confidence': 'high' if 'sí' in response.text.lower() else 'medium'
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error validando firma con Gemini: {e}")
            return {'enabled': True, 'error': str(e)}
    
    def read_handwritten_text(self, image_path: str) -> Dict[str, Any]:
        """
        Lee texto manuscrito usando Gemini
        """
        if not self.enabled:
            return {'enabled': False}
        
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            prompt = """
Lee TODAS las anotaciones o texto manuscrito (escrito a mano) en este documento.

Transcribe exactamente lo que dice cada anotación.

Si no hay anotaciones manuscritas, responde: "Sin anotaciones manuscritas"
            """
            
            response = self.model.generate_content([prompt, image_data])
            
            return {
                'enabled': True,
                'text': response.text,
                'has_annotations': 'sin anotaciones' not in response.text.lower()
            }
            
        except Exception as e:
            logger.error(f"Error leyendo manuscrito con Gemini: {e}")
            return {'enabled': True, 'error': str(e)}
    
    def classify_pod(self, image_path: str) -> Dict[str, Any]:
        """
        Clasificación rápida del POD usando Gemini
        """
        if not self.enabled:
            return {'enabled': False}
        
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            prompt = """
Clasifica este POD en UNA categoría:

1. OK - Si tiene firma manuscrita Y/O sello del cliente (NO de Deacero ni Ingetek)
2. CON ANOTACIONES - Si tiene comentarios manuscritos
3. SIN ACUSE - Si NO tiene firma, sello ni anotaciones
4. POCO LEGIBLE - Si los campos (Factura, Cliente, Pedido) no se distinguen
5. INCORRECTO - Si el documento está cortado o incompleto

Responde en formato:
CLASIFICACIÓN: [nombre]
CONFIANZA: [ALTA/MEDIA/BAJA]
RAZÓN: [breve explicación]
            """
            
            response = self.model.generate_content([prompt, image_data])
            
            return {
                'enabled': True,
                'classification_text': response.text,
                'raw_response': response.text
            }
            
        except Exception as e:
            logger.error(f"Error clasificando con Gemini: {e}")
            return {'enabled': True, 'error': str(e)}
    
    def analyze_critical_annotations(self, image_path: str) -> Dict[str, Any]:
        """
        Analiza SOLO anotaciones manuscritas críticas
        Más rápido y económico que análisis completo
        """
        if not self.enabled:
            return {'enabled': False}
        
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            prompt = """
Ignora todo el texto IMPRESO del documento.

Enfócate SOLO en texto MANUSCRITO (escrito a mano):

¿Hay anotaciones manuscritas?
- Si NO: Responde "Sin anotaciones manuscritas"
- Si SÍ: 
  * Transcribe EXACTAMENTE lo que dice
  * Sentimiento: POSITIVO (confirma/acepta) / NEGATIVO (reclama/rechaza) / NEUTRAL
  * Urgencia: URGENTE / NORMAL / INFO
  * Resumen: [breve descripción de 1 línea]

Formato:
MANUSCRITO: [SÍ/NO]
TEXTO: [transcripción exacta]
SENTIMIENTO: [POSITIVO/NEGATIVO/NEUTRAL]
URGENCIA: [URGENTE/NORMAL/INFO]
RESUMEN: [descripción breve]
            """
            
            response = self.model.generate_content([prompt, image_data])
            text_response = response.text.lower()
            
            result = {
                'enabled': True,
                'raw_response': response.text,
                'has_annotations': 'sin anotaciones' not in text_response,
                'sentiment': 'neutral',
                'urgency': 'normal',
                'transcription': ''
            }
            
            # Parsear respuesta
            if result['has_annotations']:
                if 'negativo' in text_response or 'reclama' in text_response:
                    result['sentiment'] = 'negative'
                elif 'positivo' in text_response or 'acepta' in text_response or 'conforme' in text_response:
                    result['sentiment'] = 'positive'
                
                if 'urgente' in text_response:
                    result['urgency'] = 'urgent'
                
                # Extraer transcripción
                lines = response.text.split('\n')
                for line in lines:
                    if 'TEXTO:' in line.upper():
                        result['transcription'] = line.split(':', 1)[1].strip()
                        break
            
            return result
            
        except Exception as e:
            logger.error(f"Error analizando manuscritos: {e}")
            return {'enabled': True, 'error': str(e)}
    
    def validate_signature_authenticity(self, image_path: str) -> Dict[str, Any]:
        """
        Valida si la firma es manuscrita real o sello/impresión
        """
        if not self.enabled:
            return {'enabled': False}
        
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            prompt = """
Enfócate SOLO en la FIRMA del documento (usualmente abajo).

Clasifica la firma como:
1. MANUSCRITA REAL - Trazos únicos, variaciones naturales, presión visible
2. SELLO/IMPRESIÓN - Perfectamente uniforme, repetible, sin variaciones
3. FIRMA DIGITAL - Muy limpia, sin variaciones, perfecta
4. NO HAY FIRMA - No se ve ninguna firma

Responde en formato:
TIPO: [1/2/3/4]
CONFIANZA: [ALTA/MEDIA/BAJA]
EXPLICACIÓN: [breve razón de por qué]
UBICACIÓN: [donde está la firma]
            """
            
            response = self.model.generate_content([prompt, image_data])
            text_response = response.text
            
            result = {
                'enabled': True,
                'raw_response': text_response,
                'is_authentic': False,
                'signature_type': 'unknown',
                'confidence': 'low'
            }
            
            # Parsear tipo
            if 'TIPO: 1' in text_response or 'MANUSCRITA REAL' in text_response.upper():
                result['is_authentic'] = True
                result['signature_type'] = 'handwritten'
            elif 'TIPO: 2' in text_response or 'SELLO' in text_response.upper():
                result['signature_type'] = 'stamp'
            elif 'TIPO: 3' in text_response or 'DIGITAL' in text_response.upper():
                result['signature_type'] = 'digital'
            elif 'TIPO: 4' in text_response or 'NO HAY' in text_response.upper():
                result['signature_type'] = 'none'
            
            # Parsear confianza
            if 'ALTA' in text_response.upper():
                result['confidence'] = 'high'
            elif 'MEDIA' in text_response.upper():
                result['confidence'] = 'medium'
            
            return result
            
        except Exception as e:
            logger.error(f"Error validando firma: {e}")
            return {'enabled': True, 'error': str(e)}
    
    def extract_key_fields(self, image_path: str) -> Dict[str, Any]:
        """
        Extrae campos clave específicos del POD
        """
        if not self.enabled:
            return {'enabled': False}
        
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
            
            prompt = """
Extrae SOLO estos campos del POD:

1. Número de Factura: [________]
2. Cliente/Razón Social: [________]
3. Número de Pedido: [________]
4. Fecha de Entrega: [________]
5. Productos principales: [________]
6. Cantidad/Peso: [________]
7. Dirección de entrega: [________]

Si un campo NO está visible, pon: "No visible"

Responde en formato de lista numerada exactamente como arriba.
            """
            
            response = self.model.generate_content([prompt, image_data])
            
            result = {
                'enabled': True,
                'raw_response': response.text,
                'fields': {
                    'invoice_number': '',
                    'client_name': '',
                    'order_number': '',
                    'delivery_date': '',
                    'products': '',
                    'quantity': '',
                    'address': ''
                }
            }
            
            # Parsear campos
            lines = response.text.split('\n')
            for line in lines:
                if 'Factura:' in line or '1.' in line:
                    result['fields']['invoice_number'] = line.split(':', 1)[1].strip() if ':' in line else ''
                elif 'Cliente' in line or 'Razón Social' in line or '2.' in line:
                    result['fields']['client_name'] = line.split(':', 1)[1].strip() if ':' in line else ''
                elif 'Pedido' in line or '3.' in line:
                    result['fields']['order_number'] = line.split(':', 1)[1].strip() if ':' in line else ''
                elif 'Fecha' in line or '4.' in line:
                    result['fields']['delivery_date'] = line.split(':', 1)[1].strip() if ':' in line else ''
                elif 'Productos' in line or '5.' in line:
                    result['fields']['products'] = line.split(':', 1)[1].strip() if ':' in line else ''
                elif 'Cantidad' in line or 'Peso' in line or '6.' in line:
                    result['fields']['quantity'] = line.split(':', 1)[1].strip() if ':' in line else ''
                elif 'Dirección' in line or '7.' in line:
                    result['fields']['address'] = line.split(':', 1)[1].strip() if ':' in line else ''
            
            return result
            
        except Exception as e:
            logger.error(f"Error extrayendo campos: {e}")
            return {'enabled': True, 'error': str(e)}
    
    def compare_pods(self, image_path1: str, image_path2: str) -> Dict[str, Any]:
        """
        Compara dos PODs para detectar duplicados o alteraciones
        """
        if not self.enabled:
            return {'enabled': False}
        
        try:
            with open(image_path1, 'rb') as f1:
                image_data1 = f1.read()
            with open(image_path2, 'rb') as f2:
                image_data2 = f2.read()
            
            prompt = """
Compara estas dos imágenes de PODs:

¿Son el MISMO documento? (SÍ/NO)

Si SÍ son el mismo:
- ¿Hay modificaciones o alteraciones? (SÍ/NO)
- ¿Qué cambió? [describir]
- Nivel de similitud: [0-100]%

Si NO son el mismo:
- ¿Son del mismo cliente? (SÍ/NO)
- ¿Misma fecha de entrega? (SÍ/NO)
- ¿Mismo número de pedido? (SÍ/NO)
- Nivel de similitud: [0-100]%

Responde en formato claro y estructurado.
            """
            
            response = self.model.generate_content([prompt, image_data1, image_data2])
            text_response = response.text.upper()
            
            result = {
                'enabled': True,
                'raw_response': response.text,
                'are_same': 'MISMO DOCUMENTO' in text_response or '¿SON EL MISMO' in text_response and 'SÍ' in text_response,
                'has_modifications': 'MODIFICACIONES' in text_response or 'ALTERACIONES' in text_response,
                'similarity': 0
            }
            
            # Extraer porcentaje de similitud
            import re
            similarity_match = re.search(r'(\d+)%', response.text)
            if similarity_match:
                result['similarity'] = int(similarity_match.group(1))
            
            return result
            
        except Exception as e:
            logger.error(f"Error comparando PODs: {e}")
            return {'enabled': True, 'error': str(e)}


def get_gemini_api_key_from_config() -> Optional[str]:
    """
    Intenta obtener la API key desde configuración o variables de entorno
    """
    # Intentar desde variable de entorno
    api_key = os.getenv('GEMINI_API_KEY')
    
    if api_key:
        return api_key
    
    # Intentar desde archivo de configuración
    config_file = 'config/gemini_api_key.txt'
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            api_key = f.read().strip()
            return api_key
    
    return None


