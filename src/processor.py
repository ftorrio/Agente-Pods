# -*- coding: utf-8 -*-
"""
Procesador de Documentos POD
Maneja la carga y conversión de diferentes formatos de documento
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import cv2
import numpy as np
from loguru import logger

from utils import (
    load_image, 
    convert_pdf_to_images, 
    preprocess_image,
    calculate_blur
)


class DocumentProcessor:
    """
    Clase para procesar documentos POD en diferentes formatos
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa el procesador de documentos
        
        Args:
            config: Diccionario de configuración
        """
        self.config = config
        self.supported_formats = config['supported_formats']
        self.max_dimension = config['image_processing']['max_dimension']
        self.dpi = config['image_processing']['dpi']
        self.enhance_contrast = config['image_processing']['enhance_contrast']
        self.denoise = config['image_processing']['denoise']
        
        logger.info("Procesador de documentos inicializado")
    
    def is_supported_format(self, file_path: str) -> bool:
        """
        Verifica si el formato del archivo es soportado
        
        Args:
            file_path: Ruta al archivo
            
        Returns:
            True si el formato es soportado
        """
        ext = Path(file_path).suffix.lower()
        return ext in self.supported_formats
    
    def process_document(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Procesa un documento y retorna lista de páginas/imágenes
        
        Args:
            file_path: Ruta al documento
            
        Returns:
            Lista de diccionarios con información de cada página
        """
        if not self.is_supported_format(file_path):
            logger.warning(f"Formato no soportado: {file_path}")
            return []
        
        file_ext = Path(file_path).suffix.lower()
        pages = []
        
        try:
            if file_ext == '.pdf':
                pages = self._process_pdf(file_path)
            else:
                pages = self._process_image(file_path)
            
            logger.info(f"Documento procesado: {file_path} - {len(pages)} página(s)")
            return pages
            
        except Exception as e:
            logger.error(f"Error procesando documento {file_path}: {e}")
            return []
    
    def _process_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Procesa un archivo PDF
        
        Args:
            pdf_path: Ruta al PDF
            
        Returns:
            Lista de páginas procesadas
        """
        images = convert_pdf_to_images(pdf_path, self.dpi)
        pages = []
        
        for idx, image in enumerate(images):
            page_data = self._process_image_array(image, pdf_path, page_num=idx+1)
            if page_data:
                pages.append(page_data)
        
        return pages
    
    def _process_image(self, image_path: str) -> List[Dict[str, Any]]:
        """
        Procesa un archivo de imagen
        
        Args:
            image_path: Ruta a la imagen
            
        Returns:
            Lista con una página procesada
        """
        image = load_image(image_path, self.max_dimension)
        if image is None:
            return []
        
        page_data = self._process_image_array(image, image_path, page_num=1)
        return [page_data] if page_data else []
    
    def _process_image_array(self, image: np.ndarray, source_path: str, 
                            page_num: int = 1) -> Optional[Dict[str, Any]]:
        """
        Procesa un array de imagen
        
        Args:
            image: Imagen como numpy array
            source_path: Ruta del archivo original
            page_num: Número de página
            
        Returns:
            Diccionario con datos de la página
        """
        # Calcular calidad de la imagen
        blur_score = calculate_blur(image)
        
        # Preprocesar imagen
        processed_image = preprocess_image(
            image, 
            self.enhance_contrast, 
            self.denoise
        )
        
        # Crear escala de grises para análisis
        gray_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
        
        page_data = {
            'source_file': source_path,
            'page_number': page_num,
            'original_image': image,
            'processed_image': processed_image,
            'gray_image': gray_image,
            'dimensions': (image.shape[1], image.shape[0]),  # (width, height)
            'blur_score': blur_score,
            'is_blurry': blur_score < self.config['thresholds']['blur_threshold'],
        }
        
        return page_data
    
    def extract_zones(self, page_data: Dict[str, Any]) -> Dict[str, np.ndarray]:
        """
        Extrae las zonas de interés definidas en la configuración
        
        Args:
            page_data: Datos de la página
            
        Returns:
            Diccionario con imágenes de cada zona
        """
        zones = {}
        image = page_data['processed_image']
        h, w = image.shape[:2]
        
        zone_configs = self.config['zones']
        
        for zone_name, zone_config in zone_configs.items():
            x1 = int(zone_config['x_start'] * w)
            x2 = int(zone_config['x_end'] * w)
            y1 = int(zone_config['y_start'] * h)
            y2 = int(zone_config['y_end'] * h)
            
            zone_image = image[y1:y2, x1:x2]
            zones[zone_name] = zone_image
        
        return zones
    
    def get_document_info(self, file_path: str) -> Dict[str, Any]:
        """
        Obtiene información básica del documento
        
        Args:
            file_path: Ruta al documento
            
        Returns:
            Diccionario con información del documento
        """
        file_stat = os.stat(file_path)
        
        return {
            'filename': os.path.basename(file_path),
            'filepath': file_path,
            'extension': Path(file_path).suffix.lower(),
            'size_bytes': file_stat.st_size,
            'size_mb': round(file_stat.st_size / (1024 * 1024), 2),
            'modified_date': file_stat.st_mtime,
        }

