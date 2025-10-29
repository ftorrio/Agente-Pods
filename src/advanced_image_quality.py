# -*- coding: utf-8 -*-
"""
Evaluación y Mejora Avanzada de Calidad de Imagen
Técnicas de estado del arte para máxima nitidez y legibilidad
"""

import cv2
import numpy as np
from typing import Dict, Any, List, Tuple
from loguru import logger
from scipy.signal import convolve2d
from scipy.ndimage import gaussian_filter


class ImageQualityAnalyzer:
    """
    Evaluación multi-dimensional de calidad de imagen
    """
    
    def __init__(self):
        logger.info("Analizador de calidad de imagen inicializado")
    
    def comprehensive_quality_score(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Score de calidad completo (0-100) evaluando 10 aspectos
        """
        logger.info("Calculando score de calidad comprehensivo...")
        
        scores = {
            'sharpness': self._measure_sharpness(image),
            'contrast': self._measure_contrast(image),
            'brightness': self._measure_brightness(image),
            'noise_level': self._measure_noise(image),
            'compression': self._measure_compression(image),
            'resolution': self._measure_resolution(image),
            'color_balance': self._measure_color_balance(image),
            'saturation': self._measure_saturation(image),
            'exposure': self._measure_exposure(image),
            'text_clarity': self._measure_text_clarity(image)
        }
        
        # Pesos ponderados (más importantes para OCR)
        weights = {
            'sharpness': 0.25,
            'contrast': 0.20,
            'text_clarity': 0.20,
            'resolution': 0.15,
            'brightness': 0.10,
            'noise_level': 0.05,
            'compression': 0.03,
            'color_balance': 0.01,
            'saturation': 0.01,
            'exposure': 0.00
        }
        
        final_score = sum(scores[k] * weights[k] * 100 for k in scores)
        
        # Clasificar por grado
        grade = self._get_grade(final_score)
        
        # Identificar puntos débiles y fuertes
        weak_points = [k for k, v in scores.items() if v < 0.5]
        strong_points = [k for k, v in scores.items() if v > 0.8]
        
        # Generar recomendaciones
        recommendations = self._generate_recommendations(scores)
        
        result = {
            'overall_score': round(final_score, 1),
            'grade': grade,
            'individual_scores': {k: round(v * 100, 1) for k, v in scores.items()},
            'weak_points': weak_points,
            'strong_points': strong_points,
            'recommendations': recommendations,
            'requires_enhancement': final_score < 70
        }
        
        logger.info(f"Score de calidad: {final_score:.1f}/100 (Grado: {grade})")
        return result
    
    def _measure_sharpness(self, image: np.ndarray) -> float:
        """Mide nitidez usando varianza del Laplaciano"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        # Normalizar a 0-1 (100 es bueno, 500+ es excelente)
        return min(laplacian_var / 500, 1.0)
    
    def _measure_contrast(self, image: np.ndarray) -> float:
        """Mide contraste usando desviación estándar"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        std_dev = np.std(gray)
        # Normalizar (60+ es bueno)
        return min(std_dev / 60, 1.0)
    
    def _measure_brightness(self, image: np.ndarray) -> float:
        """Mide si el brillo es adecuado (ideal: 120-140)"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        mean_brightness = np.mean(gray)
        # Penalizar si está muy oscuro o muy claro
        if 100 <= mean_brightness <= 160:
            return 1.0
        elif 80 <= mean_brightness <= 180:
            return 0.8
        else:
            return max(0.3, 1.0 - abs(mean_brightness - 120) / 120)
    
    def _measure_noise(self, image: np.ndarray) -> float:
        """Mide nivel de ruido (menor es mejor)"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        # Estimar ruido con desviación estándar de filtro gaussiano
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        noise = np.std(gray - blurred)
        # Invertir (menos ruido = mejor score)
        return max(0, 1.0 - noise / 20)
    
    def _measure_compression(self, image: np.ndarray) -> float:
        """Detecta artefactos de compresión JPEG"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        # Detectar bloques 8x8 típicos de JPEG
        dct = cv2.dct(np.float32(gray))
        # Si hay muchos bloques, hay compresión fuerte
        block_artifacts = np.sum(np.abs(dct[::8, ::8])) / dct.size
        return max(0, 1.0 - block_artifacts * 10)
    
    def _measure_resolution(self, image: np.ndarray) -> float:
        """Evalúa si la resolución es adecuada"""
        h, w = image.shape[:2]
        pixels = h * w
        # Ideal: 1200x1600 = 1,920,000 pixels
        if pixels >= 1500000:
            return 1.0
        elif pixels >= 800000:
            return 0.8
        elif pixels >= 400000:
            return 0.6
        else:
            return max(0.3, pixels / 1920000)
    
    def _measure_color_balance(self, image: np.ndarray) -> float:
        """Mide balance de color"""
        if len(image.shape) == 2:
            return 1.0  # Grayscale está balanceado
        b, g, r = cv2.split(image)
        avg_b, avg_g, avg_r = np.mean(b), np.mean(g), np.mean(r)
        # Calcular desbalance
        imbalance = np.std([avg_b, avg_g, avg_r])
        return max(0, 1.0 - imbalance / 50)
    
    def _measure_saturation(self, image: np.ndarray) -> float:
        """Mide saturación de color"""
        if len(image.shape) == 2:
            return 1.0
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        saturation = np.mean(hsv[:, :, 1])
        # Ideal: 50-150
        if 50 <= saturation <= 150:
            return 1.0
        else:
            return max(0.5, 1.0 - abs(saturation - 100) / 100)
    
    def _measure_exposure(self, image: np.ndarray) -> float:
        """Mide si la exposición es correcta"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        # Imagen bien expuesta tiene distribución uniforme
        hist_std = np.std(hist)
        return min(hist_std / 1000, 1.0)
    
    def _measure_text_clarity(self, image: np.ndarray) -> float:
        """Mide qué tan claro es el texto (específico para OCR)"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        # Detectar bordes (texto tiene muchos bordes)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        # Ideal: 5-15% de pixels son bordes
        if 0.05 <= edge_density <= 0.15:
            return 1.0
        else:
            return max(0.4, 1.0 - abs(edge_density - 0.10) / 0.10)
    
    def _get_grade(self, score: float) -> str:
        """Convierte score numérico a letra"""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
    
    def _generate_recommendations(self, scores: Dict[str, float]) -> List[str]:
        """Genera recomendaciones basadas en scores"""
        recommendations = []
        
        if scores['sharpness'] < 0.6:
            recommendations.append("Aplicar Richardson-Lucy deconvolution para mejorar nitidez")
        
        if scores['contrast'] < 0.6:
            recommendations.append("Aplicar CLAHE adaptativo para mejorar contraste")
        
        if scores['brightness'] < 0.6:
            recommendations.append("Ajustar brillo (gamma correction)")
        
        if scores['noise_level'] < 0.6:
            recommendations.append("Aplicar Non-Local Means denoising")
        
        if scores['resolution'] < 0.6:
            recommendations.append("Aplicar super-resolución ESRGAN")
        
        if scores['text_clarity'] < 0.6:
            recommendations.append("Aplicar edge-preserving sharpening")
        
        if not recommendations:
            recommendations.append("Imagen de buena calidad - aplicar mejoras ligeras")
        
        return recommendations
    
    def detect_problems(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Detecta problemas específicos en la imagen
        """
        logger.info("Detectando problemas en imagen...")
        
        problems = []
        
        # Problema 1: Motion blur
        if self._detect_motion_blur(image):
            problems.append({
                'type': 'motion_blur',
                'severity': 'high',
                'solution': 'Richardson-Lucy deconvolution',
                'estimated_fix_time': 3
            })
        
        # Problema 2: Out of focus
        if self._detect_out_of_focus(image):
            problems.append({
                'type': 'out_of_focus',
                'severity': 'high',
                'solution': 'Unsharp masking + super-resolution',
                'estimated_fix_time': 4
            })
        
        # Problema 3: JPEG artifacts
        if self._detect_compression_artifacts(image):
            problems.append({
                'type': 'jpeg_artifacts',
                'severity': 'medium',
                'solution': 'Deblocking filter',
                'estimated_fix_time': 2
            })
        
        # Problema 4: Low resolution
        if self._detect_low_resolution(image):
            problems.append({
                'type': 'low_resolution',
                'severity': 'high',
                'solution': 'ESRGAN super-resolution',
                'estimated_fix_time': 5
            })
        
        # Problema 5: Poor lighting
        if self._detect_poor_lighting(image):
            problems.append({
                'type': 'poor_lighting',
                'severity': 'medium',
                'solution': 'Adaptive histogram equalization',
                'estimated_fix_time': 1
            })
        
        # Problema 6: Small text
        if self._detect_small_text(image):
            problems.append({
                'type': 'small_text',
                'severity': 'high',
                'solution': 'Upscale 2x + adaptive sharpen',
                'estimated_fix_time': 3
            })
        
        total_fix_time = sum(p['estimated_fix_time'] for p in problems)
        
        severity_weight = {'high': 3, 'medium': 2, 'low': 1}
        priority_order = sorted(problems, key=lambda x: severity_weight[x['severity']], reverse=True)
        
        result = {
            'problems_found': len(problems),
            'problems': problems,
            'total_fix_time': total_fix_time,
            'priority_order': priority_order,
            'requires_fixing': len(problems) > 0
        }
        
        logger.info(f"Problemas detectados: {len(problems)}")
        return result
    
    def _detect_motion_blur(self, image: np.ndarray) -> bool:
        """Detecta blur por movimiento"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        # Motion blur tiene patrón direccional en FFT
        f = np.fft.fft2(gray)
        fshift = np.fft.fftshift(f)
        magnitude = 20 * np.log(np.abs(fshift) + 1)
        # Si hay líneas prominentes, hay motion blur
        threshold = np.percentile(magnitude, 99)
        return np.sum(magnitude > threshold) > 100
    
    def _detect_out_of_focus(self, image: np.ndarray) -> bool:
        """Detecta desenfoque"""
        sharpness = self._measure_sharpness(image)
        return sharpness < 0.4
    
    def _detect_compression_artifacts(self, image: np.ndarray) -> bool:
        """Detecta artefactos JPEG"""
        compression_score = self._measure_compression(image)
        return compression_score < 0.6
    
    def _detect_low_resolution(self, image: np.ndarray) -> bool:
        """Detecta baja resolución"""
        resolution_score = self._measure_resolution(image)
        return resolution_score < 0.6
    
    def _detect_poor_lighting(self, image: np.ndarray) -> bool:
        """Detecta mala iluminación"""
        brightness_score = self._measure_brightness(image)
        return brightness_score < 0.6
    
    def _detect_small_text(self, image: np.ndarray) -> bool:
        """Detecta texto muy pequeño"""
        # Si la resolución es baja Y hay poco detalle
        return self._measure_resolution(image) < 0.5 and self._measure_text_clarity(image) < 0.5


class AdvancedSharpening:
    """
    Técnicas avanzadas de sharpening y mejora de nitidez
    """
    
    def __init__(self):
        logger.info("Módulo de sharpening avanzado inicializado")
    
    def richardson_lucy_deblur(self, image: np.ndarray, iterations: int = 10) -> np.ndarray:
        """
        Richardson-Lucy deconvolution para deblurring avanzado
        """
        logger.info(f"Aplicando Richardson-Lucy deconvolution ({iterations} iteraciones)...")
        
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
            
            # Estimar Point Spread Function (PSF)
            psf = self._estimate_psf(gray)
            
            # Richardson-Lucy algorithm
            deblurred = gray.astype(np.float64)
            psf_mirror = np.flip(np.flip(psf, 0), 1)
            
            for i in range(iterations):
                # Convolución
                conv = convolve2d(deblurred, psf, mode='same', boundary='symm')
                
                # Evitar división por cero
                conv = np.clip(conv, 1e-10, None)
                
                # Actualización
                relative_blur = gray / conv
                deblurred *= convolve2d(relative_blur, psf_mirror, mode='same', boundary='symm')
            
            # Convertir de vuelta
            result = np.clip(deblurred, 0, 255).astype(np.uint8)
            
            # Si es color, aplicar a cada canal
            if len(image.shape) == 3:
                result_color = image.copy()
                for channel in range(3):
                    result_color[:, :, channel] = self.richardson_lucy_deblur(
                        image[:, :, channel:channel+1], iterations
                    ).squeeze()
                return result_color
            
            logger.info("Richardson-Lucy completado")
            return result
            
        except Exception as e:
            logger.error(f"Error en Richardson-Lucy: {e}")
            return image
    
    def _estimate_psf(self, image: np.ndarray, size: int = 5) -> np.ndarray:
        """Estima Point Spread Function para deblurring"""
        # PSF gaussiano simple como aproximación
        psf = np.zeros((size, size))
        center = size // 2
        for i in range(size):
            for j in range(size):
                psf[i, j] = np.exp(-((i - center)**2 + (j - center)**2) / (2 * 1.5**2))
        psf /= np.sum(psf)
        return psf
    
    def adaptive_unsharp_mask(self, image: np.ndarray) -> np.ndarray:
        """
        Unsharp masking adaptativo por regiones
        """
        logger.info("Aplicando unsharp masking adaptativo...")
        
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
            
            # Detectar regiones con texto (altas frecuencias)
            edges = cv2.Canny(gray, 50, 150)
            text_mask = cv2.dilate(edges, np.ones((5, 5), np.uint8), iterations=2)
            
            # Detectar regiones uniformes (bajas frecuencias)
            blur = cv2.GaussianBlur(gray, (15, 15), 0)
            uniform_mask = np.abs(gray.astype(float) - blur.astype(float)) < 10
            
            # Sharpening fuerte para texto
            gaussian_strong = cv2.GaussianBlur(gray, (0, 0), 2.0)
            sharpened_strong = cv2.addWeighted(gray, 2.5, gaussian_strong, -1.5, 0)
            
            # Sharpening medio para resto
            gaussian_medium = cv2.GaussianBlur(gray, (0, 0), 1.5)
            sharpened_medium = cv2.addWeighted(gray, 1.8, gaussian_medium, -0.8, 0)
            
            # Sharpening suave para áreas uniformes
            gaussian_mild = cv2.GaussianBlur(gray, (0, 0), 1.0)
            sharpened_mild = cv2.addWeighted(gray, 1.3, gaussian_mild, -0.3, 0)
            
            # Combinar
            result = gray.copy()
            result[text_mask > 0] = sharpened_strong[text_mask > 0]
            result[uniform_mask] = sharpened_mild[uniform_mask]
            result[~text_mask.astype(bool) & ~uniform_mask] = sharpened_medium[~text_mask.astype(bool) & ~uniform_mask]
            
            # Si es color, aplicar preservando color
            if len(image.shape) == 3:
                # Convertir a LAB y reemplazar canal L
                lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
                lab[:, :, 0] = result
                result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
            
            logger.info("Unsharp masking adaptativo completado")
            return result
            
        except Exception as e:
            logger.error(f"Error en unsharp adaptativo: {e}")
            return image
    
    def frequency_sharpen(self, image: np.ndarray, boost_factor: float = 2.0) -> np.ndarray:
        """
        Sharpening en dominio de frecuencia (Fourier)
        """
        logger.info("Aplicando sharpening en dominio de frecuencia...")
        
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
            
            # FFT
            f = np.fft.fft2(gray)
            fshift = np.fft.fftshift(f)
            
            # Crear filtro high-pass boost
            rows, cols = gray.shape
            crow, ccol = rows // 2, cols // 2
            
            # Filtro que amplifica altas frecuencias
            y, x = np.ogrid[:rows, :cols]
            dist_from_center = np.sqrt((x - ccol)**2 + (y - crow)**2)
            max_dist = np.sqrt(crow**2 + ccol**2)
            
            # High-pass con boost
            high_pass = 1 + (dist_from_center / max_dist) * boost_factor
            
            # Aplicar filtro
            fshift_filtered = fshift * high_pass
            
            # Transformada inversa
            f_ishift = np.fft.ifftshift(fshift_filtered)
            img_back = np.fft.ifft2(f_ishift)
            img_back = np.abs(img_back)
            
            # Normalizar
            result = np.clip(img_back, 0, 255).astype(np.uint8)
            
            # Si es color
            if len(image.shape) == 3:
                lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
                lab[:, :, 0] = result
                result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
            
            logger.info("Frequency sharpening completado")
            return result
            
        except Exception as e:
            logger.error(f"Error en frequency sharpen: {e}")
            return image
    
    def edge_preserving_sharpen(self, image: np.ndarray) -> np.ndarray:
        """
        Sharpening que preserva bordes naturales (sin halos)
        """
        logger.info("Aplicando edge-preserving sharpening...")
        
        try:
            # Detectar bordes con Canny
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
            edges = cv2.Canny(gray, 50, 150)
            
            # Expandir bordes
            kernel = np.ones((3, 3), np.uint8)
            edge_mask = cv2.dilate(edges, kernel, iterations=2)
            
            # Sharpen fuerte solo en bordes
            gaussian = cv2.GaussianBlur(image, (0, 0), 2.0)
            sharpened = cv2.addWeighted(image, 2.0, gaussian, -1.0, 0)
            
            # Combinar
            result = image.copy()
            if len(image.shape) == 3:
                for channel in range(3):
                    result[:, :, channel][edge_mask > 0] = sharpened[:, :, channel][edge_mask > 0]
            else:
                result[edge_mask > 0] = sharpened[edge_mask > 0]
            
            # Suavizar transiciones con bilateral filter
            result = cv2.bilateralFilter(result, 5, 50, 50)
            
            logger.info("Edge-preserving sharpening completado")
            return result
            
        except Exception as e:
            logger.error(f"Error en edge-preserving: {e}")
            return image

