# -*- coding: utf-8 -*-
"""
Sistema Híbrido Multi-OCR
Combina múltiples motores de OCR para máxima precisión
"""

import cv2
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from loguru import logger
from difflib import SequenceMatcher

# OCR Engines
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    logger.warning("Tesseract no disponible")

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False
    logger.warning("EasyOCR no disponible - pip install easyocr")

try:
    from paddleocr import PaddleOCR
    PADDLEOCR_AVAILABLE = True
except ImportError:
    PADDLEOCR_AVAILABLE = False
    logger.warning("PaddleOCR no disponible - pip install paddleocr")

try:
    from transformers import TrOCRProcessor, VisionEncoderDecoderModel
    from PIL import Image
    TROCR_AVAILABLE = True
except ImportError:
    TROCR_AVAILABLE = False
    logger.warning("TrOCR no disponible - pip install transformers pillow")

try:
    from google.cloud import vision
    GOOGLE_VISION_AVAILABLE = True
except ImportError:
    GOOGLE_VISION_AVAILABLE = False
    logger.warning("Google Cloud Vision no disponible")


class HybridOCR:
    """
    Sistema híbrido que combina múltiples motores de OCR
    para máxima precisión y robustez
    """
    
    def __init__(self, config: Dict = None):
        """
        Inicializa todos los motores de OCR disponibles
        """
        self.config = config or {}
        self.ocr_engines = {}
        
        # 1. Tesseract (rápido, confiable para texto impreso)
        if TESSERACT_AVAILABLE:
            self.ocr_engines['tesseract'] = {
                'enabled': True,
                'priority': 1,
                'best_for': 'printed_text',
                'speed': 'fast',
                'accuracy': 0.85
            }
            logger.info("✅ Tesseract OCR disponible")
        
        # 2. EasyOCR (excelente con manuscritos y múltiples idiomas)
        if EASYOCR_AVAILABLE:
            try:
                self.easyocr_reader = easyocr.Reader(['es', 'en'], gpu=False)
                self.ocr_engines['easyocr'] = {
                    'enabled': True,
                    'priority': 2,
                    'best_for': 'handwriting',
                    'speed': 'medium',
                    'accuracy': 0.90
                }
                logger.info("✅ EasyOCR disponible (español + inglés)")
            except Exception as e:
                logger.error(f"Error inicializando EasyOCR: {e}")
        
        # 3. PaddleOCR (muy rápido, buen balance)
        if PADDLEOCR_AVAILABLE:
            try:
                self.paddle_ocr = PaddleOCR(
                    lang='es',
                    use_angle_cls=True,
                    show_log=False
                )
                self.ocr_engines['paddleocr'] = {
                    'enabled': True,
                    'priority': 3,
                    'best_for': 'mixed_text',
                    'speed': 'very_fast',
                    'accuracy': 0.88
                }
                logger.info("✅ PaddleOCR disponible (español)")
            except Exception as e:
                logger.error(f"Error inicializando PaddleOCR: {e}")
        
        # 4. TrOCR (estado del arte con Transformers)
        if TROCR_AVAILABLE:
            try:
                self.trocr_processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-printed')
                self.trocr_model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-printed')
                self.ocr_engines['trocr'] = {
                    'enabled': True,
                    'priority': 4,
                    'best_for': 'premium_quality',
                    'speed': 'slow',
                    'accuracy': 0.95
                }
                logger.info("✅ TrOCR (Microsoft) disponible")
            except Exception as e:
                logger.error(f"Error inicializando TrOCR: {e}")
        
        # 5. Google Cloud Vision (cloud, muy preciso)
        if GOOGLE_VISION_AVAILABLE:
            self.ocr_engines['google_vision'] = {
                'enabled': self.config.get('use_cloud_ocr', False),
                'priority': 5,
                'best_for': 'cloud_processing',
                'speed': 'medium',
                'accuracy': 0.92,
                'cost': 'paid'
            }
            if self.ocr_engines['google_vision']['enabled']:
                logger.info("✅ Google Cloud Vision disponible")
        
        logger.info(f"Sistema Híbrido OCR: {len(self.ocr_engines)} motores disponibles")
    
    def extract_text_hybrid(self, image: np.ndarray, method: str = 'voting') -> Dict[str, Any]:
        """
        Extrae texto usando múltiples OCR y combina resultados
        
        Args:
            image: Imagen a procesar
            method: 'voting' (consenso), 'best' (mejor confianza), 'all' (todos)
        
        Returns:
            Texto extraído + confianza + metadata
        """
        logger.info(f"Extrayendo texto con método: {method}")
        
        results = {}
        
        # Ejecutar todos los OCR disponibles
        if 'tesseract' in self.ocr_engines:
            results['tesseract'] = self._ocr_tesseract(image)
        
        if 'easyocr' in self.ocr_engines:
            results['easyocr'] = self._ocr_easyocr(image)
        
        if 'paddleocr' in self.ocr_engines:
            results['paddleocr'] = self._ocr_paddleocr(image)
        
        if 'trocr' in self.ocr_engines and self.ocr_engines['trocr']['enabled']:
            results['trocr'] = self._ocr_trocr(image)
        
        if 'google_vision' in self.ocr_engines and self.ocr_engines['google_vision']['enabled']:
            results['google_vision'] = self._ocr_google_vision(image)
        
        # Combinar resultados según método
        if method == 'voting':
            final_result = self._combine_by_voting(results)
        elif method == 'best':
            final_result = self._combine_by_best_confidence(results)
        elif method == 'all':
            final_result = self._combine_all_results(results)
        else:
            final_result = self._combine_by_voting(results)
        
        final_result['engines_used'] = list(results.keys())
        final_result['individual_results'] = results
        
        logger.info(f"Texto extraído: {len(final_result['text'])} caracteres, "
                   f"confianza: {final_result['confidence']:.2f}")
        
        return final_result
    
    def _ocr_tesseract(self, image: np.ndarray) -> Dict[str, Any]:
        """Tesseract OCR"""
        try:
            # Convertir a escala de grises
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Extraer texto
            text = pytesseract.image_to_string(gray, lang='spa', config='--psm 6')
            
            # Obtener confianza
            data = pytesseract.image_to_data(gray, lang='spa', output_type=pytesseract.Output.DICT)
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return {
                'engine': 'tesseract',
                'text': text.strip(),
                'confidence': avg_confidence / 100,
                'words_count': len(text.split()),
                'success': True
            }
        except Exception as e:
            logger.error(f"Error en Tesseract: {e}")
            return {'engine': 'tesseract', 'text': '', 'confidence': 0, 'success': False}
    
    def _ocr_easyocr(self, image: np.ndarray) -> Dict[str, Any]:
        """EasyOCR - Excelente con manuscritos"""
        try:
            # EasyOCR necesita imagen RGB
            if len(image.shape) == 2:  # Grayscale
                image_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            else:
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Extraer texto
            results = self.easyocr_reader.readtext(image_rgb)
            
            # Combinar textos
            texts = [result[1] for result in results]
            confidences = [result[2] for result in results]
            
            full_text = ' '.join(texts)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return {
                'engine': 'easyocr',
                'text': full_text.strip(),
                'confidence': avg_confidence,
                'words_count': len(texts),
                'success': True
            }
        except Exception as e:
            logger.error(f"Error en EasyOCR: {e}")
            return {'engine': 'easyocr', 'text': '', 'confidence': 0, 'success': False}
    
    def _ocr_paddleocr(self, image: np.ndarray) -> Dict[str, Any]:
        """PaddleOCR - Muy rápido y preciso"""
        try:
            # PaddleOCR acepta numpy array directamente
            results = self.paddle_ocr.ocr(image, cls=True)
            
            if not results or not results[0]:
                return {'engine': 'paddleocr', 'text': '', 'confidence': 0, 'success': False}
            
            # Extraer textos y confianzas
            texts = []
            confidences = []
            for line in results[0]:
                text = line[1][0]
                conf = line[1][1]
                texts.append(text)
                confidences.append(conf)
            
            full_text = ' '.join(texts)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return {
                'engine': 'paddleocr',
                'text': full_text.strip(),
                'confidence': avg_confidence,
                'words_count': len(texts),
                'success': True
            }
        except Exception as e:
            logger.error(f"Error en PaddleOCR: {e}")
            return {'engine': 'paddleocr', 'text': '', 'confidence': 0, 'success': False}
    
    def _ocr_trocr(self, image: np.ndarray) -> Dict[str, Any]:
        """TrOCR - Microsoft Transformer OCR (estado del arte)"""
        try:
            # Convertir a PIL Image
            if len(image.shape) == 2:
                pil_image = Image.fromarray(image).convert('RGB')
            else:
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(image_rgb)
            
            # Procesar con TrOCR
            pixel_values = self.trocr_processor(pil_image, return_tensors="pt").pixel_values
            generated_ids = self.trocr_model.generate(pixel_values)
            generated_text = self.trocr_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            
            return {
                'engine': 'trocr',
                'text': generated_text.strip(),
                'confidence': 0.95,  # TrOCR es muy preciso
                'words_count': len(generated_text.split()),
                'success': True
            }
        except Exception as e:
            logger.error(f"Error en TrOCR: {e}")
            return {'engine': 'trocr', 'text': '', 'confidence': 0, 'success': False}
    
    def _ocr_google_vision(self, image: np.ndarray) -> Dict[str, Any]:
        """Google Cloud Vision OCR"""
        try:
            client = vision.ImageAnnotatorClient()
            
            # Convertir imagen a bytes
            success, encoded_image = cv2.imencode('.jpg', image)
            content = encoded_image.tobytes()
            
            image_vision = vision.Image(content=content)
            response = client.text_detection(image=image_vision)
            texts = response.text_annotations
            
            if texts:
                full_text = texts[0].description
                confidence = 0.92  # Google Vision es muy preciso
                
                return {
                    'engine': 'google_vision',
                    'text': full_text.strip(),
                    'confidence': confidence,
                    'words_count': len(full_text.split()),
                    'success': True
                }
            else:
                return {'engine': 'google_vision', 'text': '', 'confidence': 0, 'success': False}
        except Exception as e:
            logger.error(f"Error en Google Vision: {e}")
            return {'engine': 'google_vision', 'text': '', 'confidence': 0, 'success': False}
    
    def _combine_by_voting(self, results: Dict[str, Dict]) -> Dict[str, Any]:
        """
        Combina resultados por consenso/voting
        El texto que más OCR engines detectan es el elegido
        """
        if not results:
            return {'text': '', 'confidence': 0, 'method': 'voting'}
        
        # Filtrar resultados exitosos
        successful_results = {k: v for k, v in results.items() if v.get('success')}
        
        if not successful_results:
            return {'text': '', 'confidence': 0, 'method': 'voting'}
        
        # Si solo hay un resultado, devolverlo
        if len(successful_results) == 1:
            result = list(successful_results.values())[0]
            return {
                'text': result['text'],
                'confidence': result['confidence'],
                'method': 'voting',
                'consensus': 1.0
            }
        
        # Comparar textos entre sí
        texts = [r['text'] for r in successful_results.values()]
        confidences = [r['confidence'] for r in successful_results.values()]
        
        # Encontrar el texto con mayor similitud con los demás
        best_text = ''
        best_score = 0
        
        for i, text1 in enumerate(texts):
            similarity_sum = 0
            for j, text2 in enumerate(texts):
                if i != j:
                    similarity = SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
                    similarity_sum += similarity
            
            avg_similarity = similarity_sum / (len(texts) - 1) if len(texts) > 1 else 0
            weighted_score = avg_similarity * confidences[i]
            
            if weighted_score > best_score:
                best_score = weighted_score
                best_text = text1
        
        avg_confidence = sum(confidences) / len(confidences)
        
        return {
            'text': best_text,
            'confidence': avg_confidence,
            'method': 'voting',
            'consensus': best_score
        }
    
    def _combine_by_best_confidence(self, results: Dict[str, Dict]) -> Dict[str, Any]:
        """Elige el resultado con mayor confianza"""
        if not results:
            return {'text': '', 'confidence': 0, 'method': 'best_confidence'}
        
        successful_results = {k: v for k, v in results.items() if v.get('success')}
        
        if not successful_results:
            return {'text': '', 'confidence': 0, 'method': 'best_confidence'}
        
        # Encontrar el de mayor confianza
        best_result = max(successful_results.values(), key=lambda x: x['confidence'])
        
        return {
            'text': best_result['text'],
            'confidence': best_result['confidence'],
            'method': 'best_confidence',
            'winner': best_result['engine']
        }
    
    def _combine_all_results(self, results: Dict[str, Dict]) -> Dict[str, Any]:
        """Devuelve todos los resultados para análisis manual"""
        all_texts = []
        confidences = []
        
        for engine, result in results.items():
            if result.get('success'):
                all_texts.append(f"[{engine}]: {result['text']}")
                confidences.append(result['confidence'])
        
        combined_text = '\n'.join(all_texts)
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        return {
            'text': combined_text,
            'confidence': avg_confidence,
            'method': 'all_results',
            'engines_count': len(all_texts)
        }

