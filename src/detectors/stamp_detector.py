# -*- coding: utf-8 -*-
"""
Detector de Sellos
Identifica sellos en documentos POD y valida si son válidos
"""

import cv2
import numpy as np
import pytesseract
from typing import List, Dict, Any
from loguru import logger
import os

# Configurar ruta de Tesseract si está en la ubicación estándar
if os.path.exists(r"C:\Program Files\Tesseract-OCR\tesseract.exe"):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class StampDetector:
    """
    Clase para detectar sellos en imágenes
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa el detector de sellos
        
        Args:
            config: Diccionario de configuración
        """
        self.config = config
        self.min_area = config['thresholds']['stamp_min_area']
        self.max_area = config['thresholds']['stamp_max_area']
        self.circularity = config['thresholds']['stamp_circularity']
        self.invalid_stamps = [s.lower() for s in config['invalid_stamps']]
        
        logger.info("Detector de sellos inicializado")
    
    def detect_stamps(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detecta sellos en la imagen
        
        Args:
            image: Imagen del documento
            
        Returns:
            Lista de sellos detectados con su información
        """
        stamps = []
        
        # Convertir a escala de grises
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Detectar formas circulares/elípticas (sellos típicos)
        stamps_circular = self._detect_circular_stamps(gray, image)
        stamps.extend(stamps_circular)
        
        # Detectar sellos rectangulares
        stamps_rectangular = self._detect_rectangular_stamps(gray, image)
        stamps.extend(stamps_rectangular)
        
        # Validar cada sello detectado
        for stamp in stamps:
            stamp['is_valid'] = self._validate_stamp(stamp)
        
        logger.info(f"Detectados {len(stamps)} sello(s)")
        return stamps
    
    def _detect_circular_stamps(self, gray: np.ndarray, 
                                original: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detecta sellos con forma circular/elíptica
        
        Args:
            gray: Imagen en escala de grises
            original: Imagen original para OCR
            
        Returns:
            Lista de sellos circulares detectados
        """
        stamps = []
        
        # Aplicar umbralización
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Operaciones morfológicas
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            if self.min_area <= area <= self.max_area:
                # Calcular circularidad
                perimeter = cv2.arcLength(contour, True)
                if perimeter == 0:
                    continue
                
                circularity = (4 * np.pi * area) / (perimeter ** 2)
                
                if circularity >= self.circularity:
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Extraer ROI para OCR
                    roi = original[y:y+h, x:x+w]
                    text = self._extract_text_from_roi(roi)
                    
                    stamp = {
                        'type': 'circular',
                        'bbox': (x, y, w, h),
                        'area': area,
                        'circularity': circularity,
                        'text': text,
                        'is_valid': True  # Se validará después
                    }
                    stamps.append(stamp)
        
        return stamps
    
    def _detect_rectangular_stamps(self, gray: np.ndarray, 
                                   original: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detecta sellos con forma rectangular
        
        Args:
            gray: Imagen en escala de grises
            original: Imagen original para OCR
            
        Returns:
            Lista de sellos rectangulares detectados
        """
        stamps = []
        
        # Aplicar umbralización
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Operaciones morfológicas
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            if self.min_area <= area <= self.max_area:
                # Aproximar el contorno a un polígono
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                # Sellos rectangulares tienen ~4 vértices
                if len(approx) >= 4 and len(approx) <= 6:
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h if h > 0 else 0
                    
                    # Filtrar por relación de aspecto razonable
                    if 0.5 <= aspect_ratio <= 3.0:
                        # Extraer ROI para OCR
                        roi = original[y:y+h, x:x+w]
                        text = self._extract_text_from_roi(roi)
                        
                        stamp = {
                            'type': 'rectangular',
                            'bbox': (x, y, w, h),
                            'area': area,
                            'circularity': 0,
                            'text': text,
                            'is_valid': True  # Se validará después
                        }
                        stamps.append(stamp)
        
        return stamps
    
    def _extract_text_from_roi(self, roi: np.ndarray) -> str:
        """
        Extrae texto de una región usando OCR
        
        Args:
            roi: Región de interés
            
        Returns:
            Texto extraído
        """
        try:
            # Configuración de OCR
            config = '--psm 6 --oem 3'
            text = pytesseract.image_to_string(roi, lang='spa', config=config)
            text = text.strip().lower()
            return text
        except Exception as e:
            logger.debug(f"Error en OCR de sello: {e}")
            return ""
    
    def _validate_stamp(self, stamp: Dict[str, Any]) -> bool:
        """
        Valida si un sello es válido (no es de Deacero o Ingetek)
        
        Args:
            stamp: Diccionario con información del sello
            
        Returns:
            True si el sello es válido
        """
        text = stamp.get('text', '').lower()
        
        # Verificar si contiene palabras de sellos inválidos
        for invalid in self.invalid_stamps:
            if invalid in text:
                logger.debug(f"Sello inválido detectado: {invalid}")
                return False
        
        return True
    
    def has_valid_stamp(self, stamps: List[Dict[str, Any]]) -> bool:
        """
        Determina si hay al menos un sello válido
        
        Args:
            stamps: Lista de sellos detectados
            
        Returns:
            True si hay al menos un sello válido
        """
        return any(stamp['is_valid'] for stamp in stamps)
    
    def draw_stamps(self, image: np.ndarray, 
                   stamps: List[Dict[str, Any]]) -> np.ndarray:
        """
        Dibuja los sellos detectados en la imagen
        
        Args:
            image: Imagen original
            stamps: Lista de sellos detectados
            
        Returns:
            Imagen con sellos marcados
        """
        annotated = image.copy()
        
        for stamp in stamps:
            x, y, w, h = stamp['bbox']
            is_valid = stamp['is_valid']
            
            # Verde si es válido, rojo si no
            color = (0, 255, 0) if is_valid else (0, 0, 255)
            
            cv2.rectangle(annotated, (x, y), (x + w, y + h), color, 2)
            
            label = f"Sello ({'OK' if is_valid else 'INVALIDO'})"
            cv2.putText(annotated, label, (x, y - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        return annotated

