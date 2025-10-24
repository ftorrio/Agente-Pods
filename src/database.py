# -*- coding: utf-8 -*-
"""
Gestor de Base de Datos para PODs
Almacena y gestiona historial completo de validaciones
"""

import sqlite3
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from loguru import logger
import json


class PODDatabase:
    """
    Gestor de base de datos SQLite para PODs
    """
    
    def __init__(self, db_path: str = "database/pods.db"):
        """
        Inicializa la conexión a la base de datos
        
        Args:
            db_path: Ruta al archivo de base de datos
        """
        self.db_path = db_path
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Conectar a la base de datos
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        
        # Crear tablas si no existen
        self._create_tables()
        
        logger.info(f"Base de datos inicializada: {db_path}")
    
    def _create_tables(self):
        """
        Crea las tablas necesarias en la base de datos
        """
        cursor = self.conn.cursor()
        
        # Tabla de PODs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_archivo TEXT UNIQUE NOT NULL,
                ruta_original TEXT,
                tamaño_mb REAL,
                formato TEXT,
                fecha_creacion TEXT,
                fecha_procesamiento TEXT,
                fuente TEXT,
                hash_archivo TEXT
            )
        """)
        
        # Tabla de resultados de clasificación
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resultados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pod_id INTEGER NOT NULL,
                clasificacion TEXT NOT NULL,
                codigo_clasificacion TEXT NOT NULL,
                es_valido BOOLEAN NOT NULL,
                confianza REAL NOT NULL,
                fecha_analisis TEXT NOT NULL,
                FOREIGN KEY (pod_id) REFERENCES pods(id)
            )
        """)
        
        # Tabla de detecciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detecciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pod_id INTEGER NOT NULL,
                num_firmas INTEGER,
                num_sellos INTEGER,
                sellos_validos INTEGER,
                num_anotaciones INTEGER,
                sentimiento TEXT,
                campos_detectados TEXT,
                confianza_ocr REAL,
                es_borroso BOOLEAN,
                es_completo BOOLEAN,
                FOREIGN KEY (pod_id) REFERENCES pods(id)
            )
        """)
        
        # Tabla de alertas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alertas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pod_id INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                prioridad TEXT NOT NULL,
                titulo TEXT NOT NULL,
                mensaje TEXT,
                fecha TEXT NOT NULL,
                leida BOOLEAN DEFAULT 0,
                FOREIGN KEY (pod_id) REFERENCES pods(id)
            )
        """)
        
        # Índices para búsquedas rápidas
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pod_nombre ON pods(nombre_archivo)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_clasificacion ON resultados(codigo_clasificacion)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_fecha_proceso ON pods(fecha_procesamiento)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_alertas_prioridad ON alertas(prioridad)")
        
        self.conn.commit()
        logger.info("Tablas de base de datos creadas/verificadas")
    
    def save_pod_result(self, result: Dict[str, Any]) -> int:
        """
        Guarda un resultado completo en la base de datos
        
        Args:
            result: Diccionario con resultado de clasificación
            
        Returns:
            ID del POD guardado
        """
        cursor = self.conn.cursor()
        
        try:
            # Extraer información del archivo
            nombre_archivo = os.path.basename(result['source_file'])
            
            # Verificar si ya existe
            cursor.execute("SELECT id FROM pods WHERE nombre_archivo = ?", (nombre_archivo,))
            existing = cursor.fetchone()
            
            if existing:
                pod_id = existing[0]
                logger.debug(f"POD ya existe en BD: {nombre_archivo} (ID: {pod_id})")
            else:
                # Insertar POD
                doc_info = result.get('document_info', {})
                cursor.execute("""
                    INSERT INTO pods (nombre_archivo, ruta_original, tamaño_mb, formato, 
                                    fecha_procesamiento, fuente)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    nombre_archivo,
                    result['source_file'],
                    doc_info.get('size_mb', 0),
                    doc_info.get('extension', ''),
                    datetime.now().isoformat(),
                    'cloud' if 'Temp' in result['source_file'] else 'local'
                ))
                pod_id = cursor.lastrowid
                logger.info(f"Nuevo POD guardado en BD: {nombre_archivo} (ID: {pod_id})")
            
            # Guardar resultado de clasificación
            cursor.execute("""
                INSERT INTO resultados (pod_id, clasificacion, codigo_clasificacion, 
                                      es_valido, confianza, fecha_analisis)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                pod_id,
                result['classification'],
                result['classification_code'],
                result['is_valid'],
                result['confidence'],
                datetime.now().isoformat()
            ))
            
            # Guardar detecciones
            details = result.get('details', {})
            cursor.execute("""
                INSERT INTO detecciones (pod_id, num_firmas, num_sellos, num_anotaciones,
                                       sentimiento, campos_detectados, confianza_ocr,
                                       es_borroso, es_completo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                pod_id,
                len(details.get('signatures', [])),
                len(details.get('stamps', [])),
                details.get('annotations', {}).get('annotation_count', 0),
                details.get('annotations', {}).get('sentiment', 'neutral'),
                json.dumps(details.get('legibility', {}).get('fields_detected', [])),
                details.get('legibility', {}).get('ocr_confidence', 0),
                details.get('is_blurry', False),
                details.get('is_complete', True)
            ))
            
            self.conn.commit()
            return pod_id
            
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error guardando en BD: {e}")
            return -1
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas generales de la base de datos
        """
        cursor = self.conn.cursor()
        
        stats = {}
        
        # Total de PODs
        cursor.execute("SELECT COUNT(*) FROM pods")
        stats['total_pods'] = cursor.fetchone()[0]
        
        # Por clasificación
        cursor.execute("""
            SELECT codigo_clasificacion, COUNT(*) as count
            FROM resultados
            GROUP BY codigo_clasificacion
        """)
        stats['por_clasificacion'] = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Válidos vs inválidos
        cursor.execute("SELECT es_valido, COUNT(*) FROM resultados GROUP BY es_valido")
        validos_data = {row[0]: row[1] for row in cursor.fetchall()}
        stats['validos'] = validos_data.get(1, 0)
        stats['invalidos'] = validos_data.get(0, 0)
        
        # Último procesamiento
        cursor.execute("SELECT MAX(fecha_procesamiento) FROM pods")
        stats['ultimo_proceso'] = cursor.fetchone()[0]
        
        # Tamaño de BD
        if os.path.exists(self.db_path):
            stats['tamaño_bd_mb'] = round(os.path.getsize(self.db_path) / (1024*1024), 2)
        
        return stats
    
    def search_pods(self, clasificacion: str = None, fecha_desde: str = None,
                   fecha_hasta: str = None, es_valido: bool = None,
                   limit: int = 100) -> List[Dict]:
        """
        Busca PODs con filtros
        """
        cursor = self.conn.cursor()
        
        query = """
            SELECT p.*, r.clasificacion, r.es_valido, r.confianza, r.fecha_analisis,
                   d.num_firmas, d.num_sellos, d.sentimiento
            FROM pods p
            JOIN resultados r ON p.id = r.pod_id
            JOIN detecciones d ON p.id = d.pod_id
            WHERE 1=1
        """
        params = []
        
        if clasificacion:
            query += " AND r.codigo_clasificacion = ?"
            params.append(clasificacion)
        
        if fecha_desde:
            query += " AND p.fecha_procesamiento >= ?"
            params.append(fecha_desde)
        
        if fecha_hasta:
            query += " AND p.fecha_procesamiento <= ?"
            params.append(fecha_hasta)
        
        if es_valido is not None:
            query += " AND r.es_valido = ?"
            params.append(es_valido)
        
        query += f" ORDER BY p.fecha_procesamiento DESC LIMIT {limit}"
        
        cursor.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        
        return results
    
    def pod_exists(self, nombre_archivo: str) -> bool:
        """
        Verifica si un POD ya fue procesado
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM pods WHERE nombre_archivo = ?", (nombre_archivo,))
        return cursor.fetchone() is not None
    
    def get_pod_history(self, nombre_archivo: str) -> List[Dict]:
        """
        Obtiene el historial completo de un POD
        """
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT r.*, d.*
            FROM pods p
            JOIN resultados r ON p.id = r.pod_id
            JOIN detecciones d ON p.id = d.pod_id
            WHERE p.nombre_archivo = ?
            ORDER BY r.fecha_analisis DESC
        """, (nombre_archivo,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def close(self):
        """
        Cierra la conexión a la base de datos
        """
        if self.conn:
            self.conn.close()
            logger.info("Conexión a BD cerrada")


