# -*- coding: utf-8 -*-
"""
Autenticación con Google Cloud Storage
"""

from google.cloud import storage
from typing import List
from loguru import logger
import os


class AuthenticatedCloudReader:
    """
    Lector autenticado para Google Cloud Storage
    """
    
    def __init__(self, credentials_path: str = None, credentials_dict: dict = None):
        """
        Inicializa el lector autenticado
        
        Args:
            credentials_path: Ruta al archivo JSON de credenciales
            credentials_dict: Diccionario con credenciales (para Streamlit Cloud)
        """
        self.credentials_path = credentials_path
        self.client = None
        
        # Opción 1: Desde diccionario (Streamlit secrets)
        if credentials_dict:
            from google.oauth2 import service_account
            credentials = service_account.Credentials.from_service_account_info(credentials_dict)
            self.client = storage.Client(credentials=credentials, project=credentials_dict.get('project_id'))
            logger.info("Cliente autenticado con credenciales de Streamlit secrets")
        # Opción 2: Desde archivo local
        elif credentials_path and os.path.exists(credentials_path):
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
            self.client = storage.Client()
            logger.info(f"Cliente autenticado inicializado con: {credentials_path}")
        else:
            logger.warning("No se proporcionaron credenciales o no existen")
    
    def list_blobs_in_folder(self, bucket_name: str, prefix: str, 
                            start_date: str = None, end_date: str = None) -> List[str]:
        """
        Lista todos los archivos en una carpeta del bucket
        
        Args:
            bucket_name: Nombre del bucket (ej: dea-documents-das)
            prefix: Prefijo/carpeta (ej: pod/IES161108I36/)
            start_date: Fecha de inicio (YYYY-MM-DD) - opcional
            end_date: Fecha de fin (YYYY-MM-DD) - opcional
            
        Returns:
            Lista de nombres de archivos
        """
        if not self.client:
            logger.error("Cliente no autenticado")
            return []
        
        try:
            from datetime import datetime
            
            bucket = self.client.bucket(bucket_name)
            blobs = bucket.list_blobs(prefix=prefix)
            
            # Convertir fechas si se proporcionaron
            start_datetime = None
            end_datetime = None
            
            if start_date:
                start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
            if end_date:
                end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
                # Incluir todo el día final
                from datetime import timedelta
                end_datetime = end_datetime + timedelta(days=1)
            
            files = []
            for blob in blobs:
                # Solo archivos, no carpetas
                if not blob.name.endswith('/'):
                    # Filtrar por fecha si se especificó
                    if start_datetime or end_datetime:
                        blob_time = blob.time_created.replace(tzinfo=None)
                        
                        if start_datetime and blob_time < start_datetime:
                            continue
                        if end_datetime and blob_time >= end_datetime:
                            continue
                    
                    # Obtener solo el nombre del archivo
                    filename = blob.name.split('/')[-1]
                    if filename:  # No vacío
                        files.append(filename)
            
            logger.info(f"Encontrados {len(files)} archivos en {bucket_name}/{prefix}")
            if start_date or end_date:
                logger.info(f"Filtrado por fecha: {start_date or 'inicio'} a {end_date or 'fin'}")
            return files
            
        except Exception as e:
            logger.error(f"Error listando archivos: {e}")
            return []
    
    def download_blob(self, bucket_name: str, blob_name: str, 
                     destination_path: str) -> bool:
        """
        Descarga un blob desde el bucket
        
        Args:
            bucket_name: Nombre del bucket
            blob_name: Nombre completo del blob (con ruta)
            destination_path: Ruta local de destino
            
        Returns:
            True si se descargó correctamente
        """
        if not self.client:
            logger.error("Cliente no autenticado")
            return False
        
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.download_to_filename(destination_path)
            
            logger.info(f"Descargado: {blob_name} -> {destination_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error descargando {blob_name}: {e}")
            return False
    
    def download_file_from_cloud(self, folder: str, filename: str, 
                                 temp_dir: str) -> str:
        """
        Descarga un archivo desde el bucket usando autenticación
        
        Args:
            folder: Carpeta/prefijo (ej: IES161108I36)
            filename: Nombre del archivo
            temp_dir: Directorio temporal para guardar
            
        Returns:
            Ruta local del archivo descargado
        """
        blob_name = f"pod/{folder}/{filename}"
        local_path = os.path.join(temp_dir, filename)
        
        if self.download_blob('dea-documents-das', blob_name, local_path):
            return local_path
        return None

