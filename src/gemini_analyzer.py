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
    
    def __init__(self, api_key: str = None):
        """
        Inicializa el analizador Gemini
        
        Args:
            api_key: API key de Google Gemini
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("Gemini AI inicializado correctamente")
            self.enabled = True
        else:
            logger.warning("Gemini API key no encontrada - modo deshabilitado")
            self.enabled = False
    
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


