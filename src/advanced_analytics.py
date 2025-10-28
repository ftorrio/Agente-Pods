# -*- coding: utf-8 -*-
"""
Componentes Avanzados de Análisis para PODs
Incluye: Scoring de clientes, patrones anómalos, predicciones, análisis de recurrencia
"""

import sqlite3
from datetime import datetime, timedelta
from typing import Dict, Any, List
from loguru import logger
import json


class ClientScoring:
    """Scoring de calidad de PODs por cliente"""
    
    def __init__(self, db_connection):
        self.conn = db_connection
    
    def calculate_client_score(self, client_name: str) -> Dict[str, Any]:
        """
        Calcula score de calidad para un cliente (0-10)
        """
        cursor = self.conn.cursor()
        
        # Obtener PODs del cliente
        cursor.execute("""
            SELECT r.es_valido, COUNT(*) as count
            FROM gemini_analisis g
            JOIN resultados r ON g.pod_id = r.pod_id
            WHERE g.cliente LIKE ?
            GROUP BY r.es_valido
        """, (f'%{client_name}%',))
        
        results = cursor.fetchall()
        total = sum(row[1] for row in results)
        valid = sum(row[1] for row in results if row[0] == 1)
        
        score = (valid / total * 10) if total > 0 else 5.0
        
        return {
            'client': client_name,
            'score': round(score, 1),
            'total_pods': total,
            'valid_pods': valid,
            'rating': 'Excelente' if score >= 9 else ('Bueno' if score >= 7 else ('Regular' if score >= 5 else 'Problemático'))
        }


class AnomalyDetector:
    """Detecta patrones anómalos en PODs"""
    
    def __init__(self, db_connection):
        self.conn = db_connection
    
    def detect_quantity_anomaly(self, client_name: str, current_quantity: float) -> Dict[str, Any]:
        """
        Detecta si la cantidad es anómala para este cliente
        """
        cursor = self.conn.cursor()
        
        # Obtener cantidades históricas
        cursor.execute("""
            SELECT cantidad FROM gemini_analisis
            WHERE cliente LIKE ?
            AND cantidad != ''
            LIMIT 100
        """, (f'%{client_name}%',))
        
        quantities = [float(row[0].split()[0]) for row in cursor.fetchall() if row[0] and row[0][0].isdigit()]
        
        if len(quantities) >= 5:
            import statistics
            mean = statistics.mean(quantities)
            stdev = statistics.stdev(quantities)
            
            # Anomalía si está más de 2 desviaciones estándar
            z_score = abs((current_quantity - mean) / stdev) if stdev > 0 else 0
            
            is_anomaly = z_score > 2
            
            return {
                'is_anomaly': is_anomaly,
                'z_score': z_score,
                'historical_mean': mean,
                'current_value': current_quantity,
                'severity': 'High' if z_score > 3 else ('Medium' if z_score > 2 else 'Low')
            }
        
        return {'is_anomaly': False, 'reason': 'Insufficient historical data'}


class RecurrenceAnalyzer:
    """Analiza recurrencia de problemas"""
    
    def __init__(self, db_connection):
        self.conn = db_connection
    
    def find_problem_patterns(self) -> List[Dict[str, Any]]:
        """
        Identifica patrones de problemas recurrentes
        """
        cursor = self.conn.cursor()
        patterns = []
        
        # Patrón 1: Clientes con alta tasa de problemas
        cursor.execute("""
            SELECT g.cliente, 
                   COUNT(*) as total,
                   SUM(CASE WHEN r.es_valido = 0 THEN 1 ELSE 0 END) as invalidos
            FROM gemini_analisis g
            JOIN resultados r ON g.pod_id = r.pod_id
            WHERE g.cliente != ''
            GROUP BY g.cliente
            HAVING total >= 10 AND (invalidos * 100.0 / total) > 50
            ORDER BY (invalidos * 100.0 / total) DESC
            LIMIT 10
        """)
        
        for row in cursor.fetchall():
            patterns.append({
                'type': 'Problematic Client',
                'entity': row[0],
                'total_pods': row[1],
                'invalid_pods': row[2],
                'rate': round(row[2] / row[1] * 100, 1),
                'recommendation': f'Revisar contrato con cliente {row[0]}'
            })
        
        return patterns


class PredictiveAnalytics:
    """Predicciones con Machine Learning básico"""
    
    def __init__(self, db_connection):
        self.conn = db_connection
    
    def predict_next_week_issues(self) -> Dict[str, Any]:
        """
        Predice problemas para la próxima semana basado en tendencias
        """
        cursor = self.conn.cursor()
        
        # Obtener tendencia de últimas 4 semanas
        cursor.execute("""
            SELECT 
                strftime('%W', fecha_analisis) as week,
                COUNT(*) as total,
                SUM(CASE WHEN es_valido = 0 THEN 1 ELSE 0 END) as invalid
            FROM resultados
            WHERE fecha_analisis >= date('now', '-28 days')
            GROUP BY week
            ORDER BY week
        """)
        
        weeks = cursor.fetchall()
        
        if len(weeks) >= 3:
            # Calcular tendencia simple
            invalid_rates = [row[2] / row[1] * 100 for row in weeks]
            trend = (invalid_rates[-1] - invalid_rates[0]) / len(weeks)
            
            next_week_prediction = invalid_rates[-1] + trend
            
            return {
                'predicted_invalid_rate': round(next_week_prediction, 1),
                'trend': 'Increasing' if trend > 0 else 'Decreasing',
                'recommendation': 'Increase validation resources' if trend > 5 else 'Normal operations',
                'confidence': 'Medium'
            }
        
        return {'prediction': 'Insufficient data'}

