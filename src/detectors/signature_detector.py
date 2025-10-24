# -*- coding: utf-8 -*-
"""
Detector de Firmas
Identifica firmas manuscritas en documentos POD
"""

import cv2
import numpy as np
from typing import List, Dict, Any, Tuple
from loguru import logger


class SignatureDetector:
    """
    Clase para detectar firmas manuscritas en imágenes
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa el detector de firmas
        
        Args:
            config: Diccionario de configuración
        """
        self.config = config
        self.min_area = config['thresholds']['signature_min_area']
        self.max_area = config['thresholds']['signature_max_area']
        self.confidence_threshold = config['thresholds']['signature_confidence']
        
        logger.info("Detector de firmas inicializado")
    
    def detect_signatures(self, image: np.ndarray, 
                         zones: Dict[str, np.ndarray] = None) -> List[Dict[str, Any]]:
        """
        Detecta firmas en la imagen
        
        Args:
            image: Imagen completa del documento
            zones: Diccionario opcional con zonas específicas a analizar
            
        Returns:
            Lista de firmas detectadas con su información
        """
        signatures = []
        
        # Si hay zonas específicas, analizar cada zona
        if zones:
            for zone_name, zone_image in zones.items():
                zone_signatures = self._detect_in_region(zone_image, zone_name)
                signatures.extend(zone_signatures)
        else:
            # Analizar imagen completa
            signatures = self._detect_in_region(image, "completo")
        
        logger.info(f"Detectadas {len(signatures)} firma(s)")
        return signatures
    
    def _detect_in_region(self, image: np.ndarray, region_name: str) -> List[Dict[str, Any]]:
        """
        Detecta firmas en una región específica
        
        Args:
            image: Imagen de la región
            region_name: Nombre de la región
            
        Returns:
            Lista de firmas detectadas
        """
        signatures = []
        
        # Convertir a escala de grises
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Aplicar umbralización adaptativa
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 21, 10
        )
        
        # Operaciones morfológicas para limpiar
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(
            binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Filtrar por área
            if self.min_area <= area <= self.max_area:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / h if h > 0 else 0
                
                # Las firmas suelen tener cierta relación de aspecto
                if 0.5 <= aspect_ratio <= 5.0:
                    # Calcular características adicionales
                    confidence = self._calculate_signature_confidence(
                        binary[y:y+h, x:x+w], contour
                    )
                    
                    if confidence >= self.confidence_threshold:
                        signature = {
                            'region': region_name,
                            'bbox': (x, y, w, h),
                            'area': area,
                            'aspect_ratio': aspect_ratio,
                            'confidence': confidence,
                            'type': 'firma_manuscrita'
                        }
                        signatures.append(signature)
        
        return signatures
    
    def _calculate_signature_confidence(self, roi: np.ndarray, 
                                       contour: np.ndarray) -> float:
        """
        Calcula la confianza de que un contorno sea una firma
        
        Args:
            roi: Región de interés binaria
            contour: Contorno detectado
            
        Returns:
            Valor de confianza entre 0 y 1
        """
        confidence_factors = []
        
        # Factor 1: Densidad de píxeles (firmas tienen densidad media)
        total_pixels = roi.size
        white_pixels = cv2.countNonZero(roi)
        density = white_pixels / total_pixels if total_pixels > 0 else 0
        
        # Firmas típicamente tienen densidad entre 0.1 y 0.5
        if 0.1 <= density <= 0.5:
            density_score = 1.0
        elif density < 0.1:
            density_score = density / 0.1
        else:
            density_score = max(0, 1.0 - (density - 0.5) / 0.5)
        
        confidence_factors.append(density_score)
        
        # Factor 2: Complejidad del contorno (firmas son complejas)
        perimeter = cv2.arcLength(contour, True)
        area = cv2.contourArea(contour)
        compactness = (4 * np.pi * area) / (perimeter ** 2) if perimeter > 0 else 0
        
        # Firmas suelen tener baja compacidad (formas irregulares)
        complexity_score = 1.0 - compactness
        confidence_factors.append(complexity_score)
        
        # Factor 3: Variabilidad de trazos
        # Calcular la varianza de la distancia de los píxeles al centro
        moments = cv2.moments(contour)
        if moments['m00'] > 0:
            cx = int(moments['m10'] / moments['m00'])
            cy = int(moments['m01'] / moments['m00'])
            
            distances = []
            for point in contour:
                px, py = point[0]
                dist = np.sqrt((px - cx)**2 + (py - cy)**2)
                distances.append(dist)
            
            if len(distances) > 0:
                var_score = min(1.0, np.std(distances) / 50)
                confidence_factors.append(var_score)
        
        # Promedio ponderado de los factores
        confidence = np.mean(confidence_factors)
        return confidence
    
    def has_valid_signature(self, signatures: List[Dict[str, Any]]) -> bool:
        """
        Determina si hay al menos una firma válida
        
        Args:
            signatures: Lista de firmas detectadas
            
        Returns:
            True si hay al menos una firma válida
        """
        # Verificar si hay firmas en las zonas válidas (6, 7, 8)
        valid_zones = ['zone_6', 'zone_7', 'zone_8']
        
        for sig in signatures:
            if sig['region'] in valid_zones and sig['confidence'] >= self.confidence_threshold:
                return True
        
        return False
    
    def draw_signatures(self, image: np.ndarray, 
                       signatures: List[Dict[str, Any]]) -> np.ndarray:
        """
        Dibuja las firmas detectadas en la imagen
        
        Args:
            image: Imagen original
            signatures: Lista de firmas detectadas
            
        Returns:
            Imagen con firmas marcadas
        """
        annotated = image.copy()
        
        for sig in signatures:
            x, y, w, h = sig['bbox']
            confidence = sig['confidence']
            
            # Color según confianza (verde = alta, amarillo = media, rojo = baja)
            if confidence >= 0.8:
                color = (0, 255, 0)
            elif confidence >= 0.6:
                color = (0, 255, 255)
            else:
                color = (0, 0, 255)
            
            cv2.rectangle(annotated, (x, y), (x + w, y + h), color, 2)
            
            label = f"Firma {confidence:.2f}"
            cv2.putText(annotated, label, (x, y - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        return annotated

