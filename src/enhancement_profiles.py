# -*- coding: utf-8 -*-
"""
Perfiles de Mejora y Técnicas Premium
Auto-tuning, Perfiles específicos, CLAHE adaptativo
"""

import cv2
import numpy as np
from typing import Dict, Any, Tuple
from loguru import logger


class EnhancementProfiles:
    """
    Perfiles optimizados para diferentes tipos de PODs
    """
    
    PROFILES = {
        'high_quality_scan': {
            'name': 'Escaneo de alta calidad',
            'sharpen': 1.2,
            'contrast': 1.1,
            'denoise': 3,
            'super_resolution': False,
            'description': 'POD bien escaneado, solo mejora ligera'
        },
        
        'low_quality_scan': {
            'name': 'Escaneo de baja calidad',
            'sharpen': 2.0,
            'contrast': 1.8,
            'denoise': 12,
            'super_resolution': True,
            'richardson_lucy': True,
            'description': 'POD mal escaneado, mejora agresiva'
        },
        
        'photo_from_phone': {
            'name': 'Foto con teléfono',
            'sharpen': 1.6,
            'contrast': 1.5,
            'denoise': 8,
            'super_resolution': True,
            'perspective_correction': True,
            'description': 'Foto con celular, corregir perspectiva'
        },
        
        'fax_quality': {
            'name': 'Calidad fax',
            'sharpen': 2.5,
            'contrast': 2.0,
            'denoise': 15,
            'super_resolution': True,
            'binarization': True,
            'richardson_lucy': True,
            'description': 'Calidad fax, mejora extrema'
        },
        
        'with_handwriting': {
            'name': 'Con manuscritos',
            'sharpen': 1.4,
            'contrast': 1.6,
            'denoise': 5,
            'preserve_thin_lines': True,
            'adaptive_sharpen': True,
            'description': 'Con manuscritos, preservar trazos finos'
        },
        
        'old_document': {
            'name': 'Documento antiguo',
            'sharpen': 1.8,
            'contrast': 1.7,
            'denoise': 10,
            'remove_stains': True,
            'super_resolution': True,
            'description': 'Documento viejo con manchas'
        },
        
        'backlit_photo': {
            'name': 'Foto con contraluz',
            'sharpen': 1.5,
            'contrast': 2.2,
            'denoise': 6,
            'exposure_correction': True,
            'shadow_enhancement': True,
            'description': 'Foto con problemas de iluminación'
        }
    }
    
    def __init__(self):
        logger.info("Perfiles de mejora inicializados")
    
    def detect_pod_type(self, image: np.ndarray) -> str:
        """
        Detecta automáticamente el tipo de POD
        """
        logger.info("Detectando tipo de POD...")
        
        h, w = image.shape[:2]
        pixels = h * w
        
        # Calcular características
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        # Resolución
        dpi_estimate = np.sqrt(pixels) / 8  # Estimación burda
        
        # Detectar compresión JPEG
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        diff = np.abs(gray.astype(float) - blur.astype(float))
        has_compression = np.std(diff) > 10
        
        # Detectar perspectiva
        edges = cv2.Canny(gray, 50, 150)
        lines = cv2.HoughLines(edges, 1, np.pi/180, 100)
        has_perspective = False
        if lines is not None and len(lines) > 10:
            angles = [line[0][1] for line in lines]
            angle_std = np.std(angles)
            has_perspective = angle_std > 0.2
        
        # Detectar manuscritos
        edges_density = np.sum(edges > 0) / edges.size
        has_handwriting = edges_density > 0.08
        
        # Detectar manchas (documento viejo)
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        has_stains = hist[0] > pixels * 0.05  # Muchos pixels muy oscuros
        
        # Detectar problemas de iluminación
        mean_brightness = np.mean(gray)
        brightness_std = np.std(gray)
        has_lighting_issues = brightness_std > 70 or mean_brightness < 80
        
        # Clasificar
        if dpi_estimate < 100:
            pod_type = 'fax_quality'
        elif has_perspective:
            pod_type = 'photo_from_phone'
        elif has_stains:
            pod_type = 'old_document'
        elif has_lighting_issues:
            pod_type = 'backlit_photo'
        elif has_handwriting:
            pod_type = 'with_handwriting'
        elif dpi_estimate > 200 and not has_compression:
            pod_type = 'high_quality_scan'
        else:
            pod_type = 'low_quality_scan'
        
        logger.info(f"Tipo detectado: {self.PROFILES[pod_type]['name']}")
        return pod_type
    
    def get_profile(self, pod_type: str) -> Dict[str, Any]:
        """Obtiene perfil para un tipo de POD"""
        return self.PROFILES.get(pod_type, self.PROFILES['low_quality_scan'])


class AdaptiveCLAHE:
    """
    CLAHE (Contrast Limited Adaptive Histogram Equalization) adaptativo
    Se adapta a cada región del documento
    """
    
    def __init__(self):
        logger.info("CLAHE adaptativo inicializado")
    
    def enhance(self, image: np.ndarray, grid_size: int = 8) -> np.ndarray:
        """
        Aplica CLAHE adaptativo según características de cada región
        """
        logger.info("Aplicando CLAHE adaptativo...")
        
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
            
            # Dividir en grid
            h, w = gray.shape
            cell_h = h // grid_size
            cell_w = w // grid_size
            
            enhanced = np.zeros_like(gray)
            
            for i in range(grid_size):
                for j in range(grid_size):
                    # Extraer celda
                    y1, y2 = i * cell_h, (i + 1) * cell_h if i < grid_size - 1 else h
                    x1, x2 = j * cell_w, (j + 1) * cell_w if j < grid_size - 1 else w
                    cell = gray[y1:y2, x1:x2]
                    
                    # Analizar celda
                    avg_brightness = np.mean(cell)
                    contrast = np.std(cell)
                    
                    # Determinar clip limit según características
                    if avg_brightness < 80:  # Región muy oscura
                        clip_limit = 3.5
                    elif avg_brightness > 180:  # Región muy clara
                        clip_limit = 2.5
                    elif contrast < 20:  # Región uniforme
                        clip_limit = 1.5
                    elif contrast > 60:  # Región con mucho detalle
                        clip_limit = 2.0
                    else:  # Región normal
                        clip_limit = 2.5
                    
                    # Aplicar CLAHE con parámetros adaptativos
                    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
                    enhanced_cell = clahe.apply(cell)
                    
                    # Guardar
                    enhanced[y1:y2, x1:x2] = enhanced_cell
            
            # Suavizar transiciones entre celdas
            enhanced = cv2.GaussianBlur(enhanced, (3, 3), 0)
            
            # Si es color, aplicar en canal L de LAB
            if len(image.shape) == 3:
                lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
                lab[:, :, 0] = enhanced
                result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
            else:
                result = enhanced
            
            logger.info("CLAHE adaptativo completado")
            return result
            
        except Exception as e:
            logger.error(f"Error en CLAHE adaptativo: {e}")
            return image


class AutoTuner:
    """
    Auto-tuning de parámetros usando búsqueda simple
    (Versión simplificada sin sklearn para evitar dependencia)
    """
    
    def __init__(self):
        logger.info("Auto-tuner inicializado")
    
    def optimize_parameters(self, image: np.ndarray, quick_mode: bool = True) -> Dict[str, Any]:
        """
        Encuentra los mejores parámetros de mejora para esta imagen
        
        Args:
            image: Imagen a optimizar
            quick_mode: Si True, prueba menos combinaciones (más rápido)
        """
        logger.info("Optimizando parámetros automáticamente...")
        
        # Espacio de búsqueda
        if quick_mode:
            # Modo rápido: 12 combinaciones
            param_space = {
                'contrast_alpha': [1.0, 1.5, 2.0],
                'sharpen_amount': [1.0, 1.5, 2.0],
                'denoise_strength': [0, 8],
                'brightness_delta': [0, 20]
            }
        else:
            # Modo completo: 81 combinaciones
            param_space = {
                'contrast_alpha': [1.0, 1.3, 1.6, 2.0, 2.5],
                'sharpen_amount': [0.8, 1.2, 1.6, 2.0],
                'denoise_strength': [0, 5, 10, 15],
                'brightness_delta': [-20, 0, 20, 40]
            }
        
        best_score = 0
        best_params = {}
        best_image = image
        
        # Generar todas las combinaciones
        import itertools
        keys = param_space.keys()
        combinations = list(itertools.product(*[param_space[k] for k in keys]))
        
        total_combinations = len(combinations)
        logger.info(f"Probando {total_combinations} combinaciones...")
        
        for i, values in enumerate(combinations):
            params = dict(zip(keys, values))
            
            # Aplicar mejoras con estos parámetros
            enhanced = self._apply_enhancements(image, params)
            
            # Evaluar calidad
            score = self._evaluate_quality(enhanced)
            
            if score > best_score:
                best_score = score
                best_params = params
                best_image = enhanced
                logger.debug(f"Nueva mejor combinación: score={score:.2f}, params={params}")
        
        logger.info(f"Optimización completada. Mejor score: {best_score:.2f}")
        
        return {
            'optimized_image': best_image,
            'best_params': best_params,
            'quality_score': best_score,
            'improvement': best_score / self._evaluate_quality(image)
        }
    
    def _apply_enhancements(self, image: np.ndarray, params: Dict) -> np.ndarray:
        """Aplica mejoras con parámetros específicos"""
        enhanced = image.copy()
        
        # 1. Ajustar brillo
        if params['brightness_delta'] != 0:
            enhanced = cv2.convertScaleAbs(enhanced, alpha=1, beta=params['brightness_delta'])
        
        # 2. Ajustar contraste
        if params['contrast_alpha'] != 1.0:
            enhanced = cv2.convertScaleAbs(enhanced, alpha=params['contrast_alpha'], beta=0)
        
        # 3. Denoise
        if params['denoise_strength'] > 0:
            if len(enhanced.shape) == 3:
                enhanced = cv2.fastNlMeansDenoisingColored(
                    enhanced, None, params['denoise_strength'], 
                    params['denoise_strength'], 7, 21
                )
            else:
                enhanced = cv2.fastNlMeansDenoising(
                    enhanced, None, params['denoise_strength'], 7, 21
                )
        
        # 4. Sharpen
        if params['sharpen_amount'] > 1.0:
            gaussian = cv2.GaussianBlur(enhanced, (0, 0), 2.0)
            enhanced = cv2.addWeighted(
                enhanced, params['sharpen_amount'], 
                gaussian, 1 - params['sharpen_amount'], 0
            )
        
        return enhanced
    
    def _evaluate_quality(self, image: np.ndarray) -> float:
        """
        Evalúa calidad de imagen (0-100)
        Combinación de nitidez, contraste y claridad
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        # Sharpness (Laplacian variance)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        sharpness_score = min(laplacian_var / 500 * 100, 100)
        
        # Contrast (std deviation)
        contrast_score = min(np.std(gray) / 60 * 100, 100)
        
        # Text clarity (edge density)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        clarity_score = min(edge_density / 0.10 * 100, 100)
        
        # Weighted combination
        total_score = (
            sharpness_score * 0.4 +
            contrast_score * 0.3 +
            clarity_score * 0.3
        )
        
        return total_score

