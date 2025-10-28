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
    
    def enhance_pod_image(self, image: np.ndarray, level: str = 'high') -> np.ndarray:
        """
        Aplica todas las mejoras a la imagen del POD
        
        Args:
            image: Imagen original en formato numpy array
            level: Nivel de mejora ('basic', 'medium', 'high', 'ultra')
            
        Returns:
            Imagen mejorada
        """
        logger.info(f"Iniciando mejora de imagen (nivel: {level})...")
        
        # NIVEL BÁSICO (rápido)
        if level in ['basic', 'medium', 'high', 'ultra']:
            # 1. Corrección de orientación
            image = self._correct_orientation(image)
            
            # 2. Redimensionado inteligente (si es muy grande o muy pequeña)
            image = self._smart_resize(image)
        
        # NIVEL MEDIO (calidad/velocidad balanceada)
        if level in ['medium', 'high', 'ultra']:
            # 3. Mejora de contraste adaptativo
            image = self._enhance_contrast_adaptive(image)
            
            # 4. Eliminación de ruido
            image = self._denoise_advanced(image)
        
        # NIVEL ALTO (mejor calidad)
        if level in ['high', 'ultra']:
            # 5. Corrección de iluminación
            image = self._correct_illumination(image)
            
            # 6. Aumento de nitidez
            image = self._sharpen_image(image)
            
            # 7. Eliminación de sombras
            image = self._remove_shadows(image)
        
        # NIVEL ULTRA (máxima precisión)
        if level == 'ultra':
            # 8. Corrección de perspectiva (documentos inclinados)
            image = self._correct_perspective(image)
            
            # 9. Upscaling con IA (aumenta resolución)
            image = self._upscale_image(image)
            
            # 10. Realce de bordes de texto
            image = self._enhance_text_edges(image)
            
            # 11. Reducción de compresión JPEG
            image = self._reduce_jpeg_artifacts(image)
        
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
    
    def _smart_resize(self, image: np.ndarray) -> np.ndarray:
        """
        Redimensiona inteligentemente si la imagen es muy grande o muy pequeña
        """
        try:
            h, w = image.shape[:2]
            
            # Si es muy grande, reducir (para velocidad)
            if w > 3000 or h > 3000:
                scale = 3000 / max(w, h)
                new_w = int(w * scale)
                new_h = int(h * scale)
                resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
                logger.debug(f"Imagen reducida: {w}x{h} → {new_w}x{new_h}")
                return resized
            
            # Si es muy pequeña, aumentar (para OCR)
            elif w < 800 or h < 800:
                scale = 1200 / min(w, h)
                new_w = int(w * scale)
                new_h = int(h * scale)
                resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
                logger.debug(f"Imagen ampliada: {w}x{h} → {new_w}x{new_h}")
                return resized
            
            return image
            
        except Exception as e:
            logger.debug(f"Error en smart resize: {e}")
            return image
    
    def _remove_shadows(self, image: np.ndarray) -> np.ndarray:
        """
        Elimina sombras de la imagen (PODs mal escaneados)
        """
        try:
            # Convertir a escala de grises
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Dilatar para estimar fondo con sombras
            dilated = cv2.dilate(gray, np.ones((7,7), np.uint8))
            blur = cv2.medianBlur(dilated, 21)
            
            # Restar sombras
            diff = 255 - cv2.absdiff(gray, blur)
            
            # Normalizar
            norm = cv2.normalize(diff, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
            
            # Convertir de vuelta a color
            result = cv2.cvtColor(norm, cv2.COLOR_GRAY2BGR)
            
            logger.debug("Sombras eliminadas")
            return result
            
        except Exception as e:
            logger.debug(f"Error eliminando sombras: {e}")
            return image
    
    def _correct_perspective(self, image: np.ndarray) -> np.ndarray:
        """
        Corrige la perspectiva de documentos fotografiados en ángulo
        """
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 200)
            
            # Encontrar contornos
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Buscar el contorno más grande (probablemente el documento)
                largest_contour = max(contours, key=cv2.contourArea)
                
                # Aproximar a rectángulo
                peri = cv2.arcLength(largest_contour, True)
                approx = cv2.approxPolyDP(largest_contour, 0.02 * peri, True)
                
                if len(approx) == 4:
                    # Ordenar puntos
                    pts = approx.reshape(4, 2)
                    rect = self._order_points(pts)
                    
                    # Calcular dimensiones del documento corregido
                    (tl, tr, br, bl) = rect
                    widthA = np.linalg.norm(br - bl)
                    widthB = np.linalg.norm(tr - tl)
                    maxWidth = max(int(widthA), int(widthB))
                    
                    heightA = np.linalg.norm(tr - br)
                    heightB = np.linalg.norm(tl - bl)
                    maxHeight = max(int(heightA), int(heightB))
                    
                    # Puntos de destino
                    dst = np.array([
                        [0, 0],
                        [maxWidth - 1, 0],
                        [maxWidth - 1, maxHeight - 1],
                        [0, maxHeight - 1]], dtype="float32")
                    
                    # Transformación de perspectiva
                    M = cv2.getPerspectiveTransform(rect, dst)
                    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
                    
                    logger.debug("Perspectiva corregida")
                    return warped
            
            return image
            
        except Exception as e:
            logger.debug(f"Error corrigiendo perspectiva: {e}")
            return image
    
    def _order_points(self, pts):
        """Ordena puntos: top-left, top-right, bottom-right, bottom-left"""
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        return rect
    
    def _upscale_image(self, image: np.ndarray) -> np.ndarray:
        """
        Aumenta la resolución usando super-resolución
        """
        try:
            h, w = image.shape[:2]
            
            # Solo upscale si la imagen es relativamente pequeña
            if w < 2000 and h < 2000:
                # Upscale 2x usando interpolación bicúbica de alta calidad
                scale = 2
                new_w = w * scale
                new_h = h * scale
                
                upscaled = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
                
                # Aplicar unsharp mask para nitidez después de upscale
                blurred = cv2.GaussianBlur(upscaled, (0, 0), 3)
                upscaled = cv2.addWeighted(upscaled, 1.5, blurred, -0.5, 0)
                
                logger.debug(f"Imagen ampliada: {w}x{h} → {new_w}x{new_h}")
                return upscaled
            
            return image
            
        except Exception as e:
            logger.debug(f"Error en upscaling: {e}")
            return image
    
    def _enhance_text_edges(self, image: np.ndarray) -> np.ndarray:
        """
        Realza específicamente los bordes del texto
        """
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detectar bordes con Sobel
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            edges = np.sqrt(sobelx**2 + sobely**2)
            edges = np.uint8(edges / edges.max() * 255)
            
            # Combinar con imagen original
            enhanced = cv2.addWeighted(
                cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR),
                0.7,
                cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR),
                0.3,
                0
            )
            
            logger.debug("Bordes de texto realzados")
            return enhanced
            
        except Exception as e:
            logger.debug(f"Error realzando bordes: {e}")
            return image
    
    def _reduce_jpeg_artifacts(self, image: np.ndarray) -> np.ndarray:
        """
        Reduce artefactos de compresión JPEG (bloques, ruido de compresión)
        """
        try:
            # Filtro bilateral para suavizar artefactos manteniendo bordes
            deblocked = cv2.bilateralFilter(image, 9, 75, 75)
            
            # Mezclar para no perder demasiado detalle
            result = cv2.addWeighted(deblocked, 0.7, image, 0.3, 0)
            
            logger.debug("Artefactos JPEG reducidos")
            return result
            
        except Exception as e:
            logger.debug(f"Error reduciendo artefactos JPEG: {e}")
            return image

