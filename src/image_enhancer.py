# -*- coding: utf-8 -*-
"""
Mejorador de Imágenes para PODs
Pre-procesa imágenes para mejorar legibilidad antes de OCR y análisis
"""

import cv2
import numpy as np
from typing import Tuple
from loguru import logger


class ImageEnhancer:
    """
    Clase para mejorar la calidad de imágenes de PODs antes del análisis
    """
    
    def __init__(self, config: dict = None):
        """
        Inicializa el mejorador de imágenes
        """
        self.config = config or {}
        logger.info("Mejorador de imágenes inicializado")
    
    def enhance_pod_image(self, image: np.ndarray) -> np.ndarray:
        """
        Aplica todas las mejoras a la imagen del POD
        
        Args:
            image: Imagen original en formato numpy array
            
        Returns:
            Imagen mejorada
        """
        logger.info("Iniciando mejora de imagen...")
        
        # 1. Corrección de orientación
        image = self._correct_orientation(image)
        
        # 2. Mejora de contraste adaptativo
        image = self._enhance_contrast_adaptive(image)
        
        # 3. Eliminación de ruido
        image = self._denoise_advanced(image)
        
        # 4. Corrección de iluminación
        image = self._correct_illumination(image)
        
        # 5. Aumento de nitidez
        image = self._sharpen_image(image)
        
        # 6. Binarización adaptativa (para OCR)
        # image = self._adaptive_binarization(image)  # Opcional
        
        logger.info("Mejora de imagen completada")
        return image
    
    def _correct_orientation(self, image: np.ndarray) -> np.ndarray:
        """
        Corrige la orientación de la imagen (rotación automática)
        """
        try:
            # Convertir a escala de grises
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detectar líneas para determinar orientación
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)
            lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
            
            if lines is not None and len(lines) > 0:
                # Calcular ángulo promedio
                angles = []
                for line in lines[:10]:  # Solo primeras 10 líneas
                    rho, theta = line[0]
                    angle = np.degrees(theta) - 90
                    if abs(angle) < 45:  # Ignorar líneas muy inclinadas
                        angles.append(angle)
                
                if angles:
                    avg_angle = np.median(angles)
                    
                    # Rotar si la inclinación es significativa
                    if abs(avg_angle) > 1:  # Más de 1 grado
                        logger.debug(f"Corrigiendo orientación: {avg_angle:.2f} grados")
                        h, w = image.shape[:2]
                        center = (w // 2, h // 2)
                        M = cv2.getRotationMatrix2D(center, avg_angle, 1.0)
                        image = cv2.warpAffine(image, M, (w, h), 
                                              flags=cv2.INTER_CUBIC,
                                              borderMode=cv2.BORDER_REPLICATE)
            
            return image
            
        except Exception as e:
            logger.debug(f"No se pudo corregir orientación: {e}")
            return image
    
    def _enhance_contrast_adaptive(self, image: np.ndarray) -> np.ndarray:
        """
        Mejora el contraste usando CLAHE (Contrast Limited Adaptive Histogram Equalization)
        Funciona mejor que equalización simple
        """
        try:
            # Convertir a LAB para trabajar solo con luminosidad
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            
            # Aplicar CLAHE a canal de luminosidad
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            l = clahe.apply(l)
            
            # Recombinar canales
            enhanced_lab = cv2.merge([l, a, b])
            enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
            
            logger.debug("Contraste mejorado con CLAHE")
            return enhanced
            
        except Exception as e:
            logger.debug(f"Error en mejora de contraste: {e}")
            return image
    
    def _denoise_advanced(self, image: np.ndarray) -> np.ndarray:
        """
        Eliminación avanzada de ruido manteniendo detalles importantes
        """
        try:
            # Non-Local Means Denoising (mejor que bilateral o gaussian)
            denoised = cv2.fastNlMeansDenoisingColored(
                image,
                None,
                h=10,           # Fuerza del filtro
                hColor=10,      # Fuerza para canales de color
                templateWindowSize=7,
                searchWindowSize=21
            )
            
            logger.debug("Ruido eliminado con NLM")
            return denoised
            
        except Exception as e:
            logger.debug(f"Error en eliminación de ruido: {e}")
            return image
    
    def _correct_illumination(self, image: np.ndarray) -> np.ndarray:
        """
        Corrige problemas de iluminación desigual (sombras, reflejos)
        """
        try:
            # Convertir a escala de grises
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Estimar fondo con blur gaussiano grande
            background = cv2.GaussianBlur(gray, (51, 51), 0)
            
            # Restar fondo para normalizar iluminación
            normalized = cv2.divide(gray, background, scale=255)
            
            # Convertir de vuelta a BGR manteniendo color original
            # pero con iluminación corregida
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            
            # Reemplazar canal L con versión normalizada
            enhanced_lab = cv2.merge([normalized, a, b])
            corrected = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
            
            logger.debug("Iluminación corregida")
            return corrected
            
        except Exception as e:
            logger.debug(f"Error en corrección de iluminación: {e}")
            return image
    
    def _sharpen_image(self, image: np.ndarray) -> np.ndarray:
        """
        Aumenta la nitidez para mejorar legibilidad del texto
        """
        try:
            # Kernel de nitidez
            kernel = np.array([
                [-1, -1, -1],
                [-1,  9, -1],
                [-1, -1, -1]
            ])
            
            sharpened = cv2.filter2D(image, -1, kernel)
            
            # Mezclar con original para evitar sobre-nitidez
            alpha = 0.7  # 70% imagen nítida, 30% original
            result = cv2.addWeighted(sharpened, alpha, image, 1-alpha, 0)
            
            logger.debug("Nitidez aumentada")
            return result
            
        except Exception as e:
            logger.debug(f"Error en aumento de nitidez: {e}")
            return image
    
    def _adaptive_binarization(self, image: np.ndarray) -> np.ndarray:
        """
        Binarización adaptativa (blanco y negro inteligente)
        Mejora mucho el OCR pero pierde color
        """
        try:
            # Convertir a escala de grises
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Binarización adaptativa
            binary = cv2.adaptiveThreshold(
                gray,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                blockSize=11,
                C=2
            )
            
            # Convertir de vuelta a BGR para consistencia
            result = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
            
            logger.debug("Binarización adaptativa aplicada")
            return result
            
        except Exception as e:
            logger.debug(f"Error en binarización: {e}")
            return image
    
    def before_after_comparison(self, original: np.ndarray, enhanced: np.ndarray) -> dict:
        """
        Calcula métricas de mejora entre imagen original y mejorada
        """
        try:
            # Convertir a escala de grises
            orig_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
            enh_gray = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)
            
            # Calcular contraste (desviación estándar)
            orig_contrast = np.std(orig_gray)
            enh_contrast = np.std(enh_gray)
            
            # Calcular nitidez (varianza del Laplaciano)
            orig_sharpness = cv2.Laplacian(orig_gray, cv2.CV_64F).var()
            enh_sharpness = cv2.Laplacian(enh_gray, cv2.CV_64F).var()
            
            metrics = {
                'contrast_improvement': ((enh_contrast - orig_contrast) / orig_contrast * 100),
                'sharpness_improvement': ((enh_sharpness - orig_sharpness) / orig_sharpness * 100),
                'original_contrast': orig_contrast,
                'enhanced_contrast': enh_contrast,
                'original_sharpness': orig_sharpness,
                'enhanced_sharpness': enh_sharpness
            }
            
            logger.info(f"Mejoras: Contraste +{metrics['contrast_improvement']:.1f}%, "
                       f"Nitidez +{metrics['sharpness_improvement']:.1f}%")
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculando métricas: {e}")
            return {}

