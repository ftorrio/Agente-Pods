# -*- coding: utf-8 -*-
"""
Detector de Anotaciones
Identifica anotaciones manuscritas y determina si son positivas o negativas
"""

import cv2
import numpy as np
import pytesseract
from typing import Dict, Any, List
from loguru import logger
import os

# Configurar ruta de Tesseract si está en la ubicación estándar
if os.path.exists(r"C:\Program Files\Tesseract-OCR\tesseract.exe"):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class AnnotationDetector:
    """
    Clase para detectar anotaciones manuscritas en documentos POD
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa el detector de anotaciones
        
        Args:
            config: Diccionario de configuración
        """
        self.config = config
        self.positive_keywords = [k.lower() for k in config['annotation_keywords']['positive']]
        self.negative_keywords = [k.lower() for k in config['annotation_keywords']['negative']]
        self.handwriting_confidence = config['thresholds']['handwriting_confidence']
        
        logger.info("Detector de anotaciones inicializado")
    
    def detect_annotations(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Detecta anotaciones manuscritas en el documento
        
        Args:
            image: Imagen del documento
            
        Returns:
            Diccionario con información sobre las anotaciones
        """
        results = {
            'has_annotations': False,
            'annotation_count': 0,
            'annotations': [],
            'sentiment': 'neutral',  # 'positive', 'negative', 'neutral'
            'text_content': []
        }
        
        # 1. Detectar áreas con escritura manuscrita
        handwriting_regions = self._detect_handwriting_regions(image)
        
        if not handwriting_regions:
            logger.info("No se detectaron anotaciones manuscritas")
            return results
        
        results['has_annotations'] = True
        results['annotation_count'] = len(handwriting_regions)
        
        # 2. Analizar cada región para extraer texto
        for idx, region in enumerate(handwriting_regions):
            x, y, w, h = region['bbox']
            roi = image[y:y+h, x:x+w]
            
            # Intentar OCR en la región
            text = self._extract_handwritten_text(roi)
            
            annotation = {
                'id': idx,
                'bbox': region['bbox'],
                'text': text,
                'sentiment': 'neutral'
            }
            
            # Analizar sentimiento del texto
            if text:
                sentiment = self._analyze_sentiment(text)
                annotation['sentiment'] = sentiment
                results['text_content'].append(text)
            
            results['annotations'].append(annotation)
        
        # 3. Determinar sentimiento general
        results['sentiment'] = self._determine_overall_sentiment(results['annotations'])
        
        logger.info(f"Detectadas {results['annotation_count']} anotación(es) - "
                   f"Sentimiento: {results['sentiment']}")
        
        return results
    
    def _detect_handwriting_regions(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detecta regiones con escritura manuscrita
        
        Args:
            image: Imagen del documento
            
        Returns:
            Lista de regiones con escritura manuscrita
        """
        regions = []
        
        # Convertir a escala de grises
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Aplicar umbralización adaptativa
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 15, 10
        )
        
        # Operaciones morfológicas para conectar trazos de escritura
        kernel_horizontal = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 1))
        kernel_vertical = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 20))
        
        # Detectar líneas horizontales (texto manuscrito típico)
        horizontal = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel_horizontal)
        vertical = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel_vertical)
        
        # Combinar
        combined = cv2.add(horizontal, vertical)
        
        # Dilatar para unir componentes cercanos
        kernel_dilate = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        dilated = cv2.dilate(combined, kernel_dilate, iterations=2)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Filtrar por área mínima
            if area > 500:  # Ajustar según necesidad
                x, y, w, h = cv2.boundingRect(contour)
                
                # Filtrar por relación de aspecto (evitar líneas impresas)
                aspect_ratio = w / h if h > 0 else 0
                
                if 0.5 <= aspect_ratio <= 20:  # Texto manuscrito típico
                    # Calcular densidad de píxeles en la región
                    roi = binary[y:y+h, x:x+w]
                    density = cv2.countNonZero(roi) / roi.size if roi.size > 0 else 0
                    
                    # Escritura manuscrita suele tener densidad moderada
                    if 0.05 <= density <= 0.4:
                        region = {
                            'bbox': (x, y, w, h),
                            'area': area,
                            'density': density,
                            'aspect_ratio': aspect_ratio
                        }
                        regions.append(region)
        
        return regions
    
    def _extract_handwritten_text(self, roi: np.ndarray) -> str:
        """
        Extrae texto de una región con escritura manuscrita
        
        Args:
            roi: Región de interés
            
        Returns:
            Texto extraído
        """
        try:
            # Preprocesar para mejorar OCR de escritura manuscrita
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY) if len(roi.shape) == 3 else roi
            
            # Mejorar contraste
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(gray)
            
            # Umbralización
            _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # OCR con configuración para escritura manuscrita
            config = '--psm 6 --oem 3'
            text = pytesseract.image_to_string(
                binary,
                lang=self.config['ocr']['language'],
                config=config
            )
            
            return text.strip().lower()
            
        except Exception as e:
            logger.debug(f"Error extrayendo texto manuscrito: {e}")
            return ""
    
    def _analyze_sentiment(self, text: str) -> str:
        """
        Analiza el sentimiento de una anotación
        
        Args:
            text: Texto de la anotación
            
        Returns:
            'positive', 'negative', o 'neutral'
        """
        text_lower = text.lower()
        
        # Buscar palabras clave positivas
        positive_count = sum(1 for keyword in self.positive_keywords if keyword in text_lower)
        
        # Buscar palabras clave negativas
        negative_count = sum(1 for keyword in self.negative_keywords if keyword in text_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _determine_overall_sentiment(self, annotations: List[Dict[str, Any]]) -> str:
        """
        Determina el sentimiento general basado en todas las anotaciones
        
        Args:
            annotations: Lista de anotaciones
            
        Returns:
            Sentimiento general
        """
        if not annotations:
            return 'neutral'
        
        sentiments = [ann['sentiment'] for ann in annotations]
        
        positive_count = sentiments.count('positive')
        negative_count = sentiments.count('negative')
        
        if negative_count > 0:
            # Si hay alguna negativa, el sentimiento general es negativo
            return 'negative'
        elif positive_count > 0:
            return 'positive'
        else:
            return 'neutral'
    
    def has_positive_annotations(self, annotations_data: Dict[str, Any]) -> bool:
        """
        Determina si hay anotaciones que confirman recepción
        
        Args:
            annotations_data: Datos de anotaciones
            
        Returns:
            True si hay anotaciones positivas
        """
        return annotations_data.get('sentiment') == 'positive'
    
    def has_negative_annotations(self, annotations_data: Dict[str, Any]) -> bool:
        """
        Determina si hay anotaciones que indican reclamación
        
        Args:
            annotations_data: Datos de anotaciones
            
        Returns:
            True si hay anotaciones negativas
        """
        return annotations_data.get('sentiment') == 'negative'
    
    def draw_annotations(self, image: np.ndarray, 
                        annotations_data: Dict[str, Any]) -> np.ndarray:
        """
        Dibuja las anotaciones detectadas en la imagen
        
        Args:
            image: Imagen original
            annotations_data: Datos de anotaciones
            
        Returns:
            Imagen con anotaciones marcadas
        """
        annotated = image.copy()
        
        for ann in annotations_data.get('annotations', []):
            x, y, w, h = ann['bbox']
            sentiment = ann['sentiment']
            
            # Color según sentimiento
            if sentiment == 'positive':
                color = (0, 255, 0)  # Verde
            elif sentiment == 'negative':
                color = (0, 0, 255)  # Rojo
            else:
                color = (255, 0, 0)  # Azul
            
            cv2.rectangle(annotated, (x, y), (x + w, y + h), color, 2)
            
            label = f"Anotacion ({sentiment})"
            cv2.putText(annotated, label, (x, y - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        return annotated

