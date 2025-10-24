# -*- coding: utf-8 -*-
"""
Módulo para leer PODs desde Google Cloud Storage
"""

import requests
import os
from typing import List, Dict, Any
from pathlib import Path
import tempfile
from loguru import logger


class CloudStorageReader:
    """
    Clase para leer documentos POD desde Google Cloud Storage
    """
    
    def __init__(self, base_url: str = None):
        """
        Inicializa el lector de almacenamiento en la nube
        
        Args:
            base_url: URL base del bucket de Google Cloud Storage
        """
        self.base_url = base_url or "https://storage.cloud.google.com/dea-documents-das/pod"
        self.temp_dir = tempfile.mkdtemp(prefix="pods_")
        logger.info(f"Cloud Storage Reader inicializado: {self.base_url}")
        logger.info(f"Directorio temporal: {self.temp_dir}")
    
    def list_files_from_bucket(self, prefix: str = "IES161108I36") -> List[str]:
        """
        Lista archivos disponibles en el bucket
        
        Args:
            prefix: Prefijo de la carpeta (ej: IES161108I36)
            
        Returns:
            Lista de nombres de archivos
        """
        # Nota: Google Cloud Storage público no siempre permite listar
        # Por ahora retornamos lista vacía - necesitaremos conocer los nombres
        logger.warning("Listado de archivos no disponible en bucket público")
        logger.info("Proporciona una lista de nombres de archivos para descargar")
        return []
    
    def download_file_from_cloud(self, folder: str, filename: str) -> str:
        """
        Descarga un archivo desde Google Cloud Storage
        
        Args:
            folder: Carpeta/prefijo (ej: IES161108I36)
            filename: Nombre del archivo (ej: QC8261_1024008261.jpg)
            
        Returns:
            Ruta local del archivo descargado
        """
        try:
            # Construir URL completa
            url = f"{self.base_url}/{folder}/{filename}"
            logger.info(f"Descargando desde: {url}")
            
            # Descargar archivo
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                # Guardar en directorio temporal
                local_path = os.path.join(self.temp_dir, filename)
                
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                
                logger.info(f"Archivo descargado: {filename} ({len(response.content)} bytes)")
                return local_path
            
            elif response.status_code == 404:
                logger.error(f"Archivo no encontrado en la nube: {filename}")
                return None
            
            else:
                logger.error(f"Error descargando archivo: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error descargando {filename}: {e}")
            return None
    
    def download_multiple_files(self, folder: str, filenames: List[str]) -> List[str]:
        """
        Descarga múltiples archivos desde la nube
        
        Args:
            folder: Carpeta/prefijo
            filenames: Lista de nombres de archivos
            
        Returns:
            Lista de rutas locales descargadas
        """
        downloaded_files = []
        
        for filename in filenames:
            local_path = self.download_file_from_cloud(folder, filename)
            if local_path:
                downloaded_files.append(local_path)
        
        logger.info(f"Descargados {len(downloaded_files)}/{len(filenames)} archivos")
        return downloaded_files
    
    def download_folder_by_pattern(self, folder: str, 
                                   file_pattern: str = "pod_*.jpg") -> List[str]:
        """
        Descarga archivos que coincidan con un patrón
        
        Args:
            folder: Carpeta/prefijo
            file_pattern: Patrón de búsqueda
            
        Returns:
            Lista de archivos descargados
        """
        # Para Google Cloud Storage público, necesitamos saber los nombres exactos
        # Esta función requeriría autenticación o una API de listado
        logger.warning("Esta función requiere conocer los nombres de archivos exactos")
        return []
    
    def get_file_url(self, folder: str, filename: str) -> str:
        """
        Construye la URL completa de un archivo
        
        Args:
            folder: Carpeta/prefijo
            filename: Nombre del archivo
            
        Returns:
            URL completa
        """
        return f"{self.base_url}/{folder}/{filename}"
    
    def cleanup_temp_files(self):
        """
        Limpia archivos temporales descargados
        """
        try:
            import shutil
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                logger.info(f"Directorio temporal limpiado: {self.temp_dir}")
        except Exception as e:
            logger.error(f"Error limpiando archivos temporales: {e}")


def download_pods_from_cloud(folder: str = "IES161108I36", 
                             filenames: List[str] = None) -> List[str]:
    """
    Función de conveniencia para descargar PODs desde la nube
    
    Args:
        folder: Carpeta en el bucket
        filenames: Lista de nombres de archivos a descargar
        
    Returns:
        Lista de rutas locales de archivos descargados
    """
    reader = CloudStorageReader()
    
    if not filenames:
        # Si no se proporcionan nombres, intentar con nombres comunes
        logger.info("No se proporcionaron nombres de archivos")
        return []
    
    downloaded = reader.download_multiple_files(folder, filenames)
    return downloaded


# Lista de archivos conocidos en IES161108I36
# NOTA: Los archivos en el bucket NO tienen el prefijo "pod_IES161108I36_"
KNOWN_PODS_IES161108I36 = [
    "QC8261_1024008261.jpg",
    "QM2015_1033002015.jpg",
    "QP7957_1036007957.jpg",
    "QP7960_1036007960.jpg",
    "QP7959_1036007959.jpg",
]

