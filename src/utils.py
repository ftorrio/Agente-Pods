# -*- coding: utf-8 -*-
"""
Utilidades para el Sistema de Validación de PODs
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, List
from loguru import logger
import cv2
import numpy as np
from datetime import datetime


def load_config(config_path: str = "config/settings.yaml") -> Dict[str, Any]:
    """
    Carga la configuración desde el archivo YAML
    
    Args:
        config_path: Ruta al archivo de configuración
        
    Returns:
        Diccionario con la configuración
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        logger.info(f"Configuración cargada desde {config_path}")
        return config
    except Exception as e:
        logger.error(f"Error al cargar configuración: {e}")
        return {}


def ensure_directories(config: Dict[str, Any]) -> None:
    """
    Asegura que todos los directorios necesarios existan
    
    Args:
        config: Diccionario de configuración
    """
    paths_to_create = [
        config['paths']['input_dir'],
        config['paths']['output_dir'],
        config['paths']['processed_dir'],
        config['paths']['examples_dir'],
        os.path.join(config['paths']['output_dir'], 'imagenes_anotadas'),
        os.path.join(config['paths']['output_dir'], 'reportes'),
    ]
    
    for path in paths_to_create:
        Path(path).mkdir(parents=True, exist_ok=True)
        logger.debug(f"Directorio verificado: {path}")


def get_files_from_directory(directory: str, extensions: List[str]) -> List[str]:
    """
    Obtiene todos los archivos con las extensiones especificadas de un directorio
    
    Args:
        directory: Ruta del directorio
        extensions: Lista de extensiones permitidas (ej: ['.pdf', '.gif'])
        
    Returns:
        Lista de rutas de archivos encontrados
    """
    files_set = set()  # Usar set para evitar duplicados
    for ext in extensions:
        files_set.update(Path(directory).glob(f'*{ext}'))
        files_set.update(Path(directory).glob(f'*{ext.upper()}'))
    
    # Convertir a lista y filtrar el archivo .gitkeep
    files = [str(f) for f in files_set if f.name != '.gitkeep']
    logger.info(f"Encontrados {len(files)} archivos en {directory}")
    return files


def convert_pdf_to_images(pdf_path: str, dpi: int = 300) -> List[np.ndarray]:
    """
    Convierte un PDF a lista de imágenes (una por página)
    
    Args:
        pdf_path: Ruta al archivo PDF
        dpi: Resolución de conversión
        
    Returns:
        Lista de imágenes en formato numpy array
    """
    try:
        from pdf2image import convert_from_path
        
        images = convert_from_path(pdf_path, dpi=dpi)
        # Convertir de PIL a numpy/OpenCV
        cv_images = [cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR) for img in images]
        logger.info(f"PDF convertido: {len(cv_images)} página(s)")
        return cv_images
    except Exception as e:
        logger.error(f"Error al convertir PDF {pdf_path}: {e}")
        return []


def load_image(image_path: str, max_dimension: int = 3000) -> np.ndarray:
    """
    Carga una imagen y la redimensiona si es necesario
    
    Args:
        image_path: Ruta a la imagen
        max_dimension: Dimensión máxima permitida
        
    Returns:
        Imagen en formato numpy array
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            logger.error(f"No se pudo cargar la imagen: {image_path}")
            return None
        
        # Redimensionar si es muy grande
        h, w = image.shape[:2]
        if max(h, w) > max_dimension:
            scale = max_dimension / max(h, w)
            new_w = int(w * scale)
            new_h = int(h * scale)
            image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
            logger.debug(f"Imagen redimensionada de {w}x{h} a {new_w}x{new_h}")
        
        return image
    except Exception as e:
        logger.error(f"Error al cargar imagen {image_path}: {e}")
        return None


def preprocess_image(image: np.ndarray, enhance_contrast: bool = True, 
                     denoise: bool = True) -> np.ndarray:
    """
    Preprocesa una imagen para mejorar la calidad del análisis
    
    Args:
        image: Imagen original
        enhance_contrast: Si se debe mejorar el contraste
        denoise: Si se debe reducir el ruido
        
    Returns:
        Imagen procesada
    """
    processed = image.copy()
    
    if denoise:
        processed = cv2.fastNlMeansDenoisingColored(processed, None, 10, 10, 7, 21)
    
    if enhance_contrast:
        lab = cv2.cvtColor(processed, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        processed = cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2BGR)
    
    return processed


def calculate_blur(image: np.ndarray) -> float:
    """
    Calcula el nivel de desenfoque de una imagen usando Laplaciano
    
    Args:
        image: Imagen a analizar
        
    Returns:
        Valor de desenfoque (menor = más borroso)
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var


def get_zone_coordinates(image: np.ndarray, zone_config: Dict[str, float]) -> tuple:
    """
    Convierte coordenadas relativas de zona a coordenadas absolutas
    
    Args:
        image: Imagen de referencia
        zone_config: Configuración de la zona con coordenadas relativas
        
    Returns:
        Tupla (x1, y1, x2, y2) con coordenadas absolutas
    """
    h, w = image.shape[:2]
    x1 = int(zone_config['x_start'] * w)
    x2 = int(zone_config['x_end'] * w)
    y1 = int(zone_config['y_start'] * h)
    y2 = int(zone_config['y_end'] * h)
    return (x1, y1, x2, y2)


def draw_zone(image: np.ndarray, zone_coords: tuple, label: str, 
              color: tuple = (0, 255, 0)) -> np.ndarray:
    """
    Dibuja una zona en la imagen con etiqueta
    
    Args:
        image: Imagen donde dibujar
        zone_coords: Coordenadas (x1, y1, x2, y2)
        label: Etiqueta de la zona
        color: Color BGR
        
    Returns:
        Imagen con la zona dibujada
    """
    img_copy = image.copy()
    x1, y1, x2, y2 = zone_coords
    cv2.rectangle(img_copy, (x1, y1), (x2, y2), color, 2)
    cv2.putText(img_copy, label, (x1 + 5, y1 + 25), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    return img_copy


def save_annotated_image(image: np.ndarray, output_path: str) -> None:
    """
    Guarda una imagen anotada
    
    Args:
        image: Imagen a guardar
        output_path: Ruta de salida
    """
    try:
        cv2.imwrite(output_path, image)
        logger.info(f"Imagen anotada guardada: {output_path}")
    except Exception as e:
        logger.error(f"Error al guardar imagen: {e}")


def generate_timestamp() -> str:
    """
    Genera un timestamp formateado
    
    Returns:
        String con timestamp
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def sanitize_filename(filename: str) -> str:
    """
    Sanitiza un nombre de archivo removiendo caracteres especiales
    
    Args:
        filename: Nombre de archivo original
        
    Returns:
        Nombre de archivo sanitizado
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

