# -*- coding: utf-8 -*-
"""
Generador de Reportes Ejecutivos Automáticos
Crea reportes en PDF/Excel con dashboards, KPIs y recomendaciones
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List
from loguru import logger
import json


class ExecutiveReportGenerator:
    """Genera reportes ejecutivos automáticos"""
    
    def __init__(self, db_connection):
        self.conn = db_connection
        logger.info("Generador de reportes ejecutivos inicializado")
    
    def generate_weekly_report(self) -> Dict[str, Any]:
        """
        Genera reporte semanal ejecutivo
        """
        cursor = self.conn.cursor()
        
        # Período: última semana
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        
        # KPIs principales
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN es_valido = 1 THEN 1 ELSE 0 END) as valid,
                SUM(CASE WHEN es_valido = 0 THEN 1 ELSE 0 END) as invalid
            FROM resultados
            WHERE fecha_analisis >= ?
        """, (week_ago,))
        
        kpis = cursor.fetchone()
        
        # Por clasificación
        cursor.execute("""
            SELECT codigo_clasificacion, COUNT(*)
            FROM resultados
            WHERE fecha_analisis >= ?
            GROUP BY codigo_clasificacion
        """, (week_ago,))
        
        by_class = dict(cursor.fetchall())
        
        # Alertas críticas
        cursor.execute("""
            SELECT COUNT(*)
            FROM alertas
            WHERE fecha >= ? AND prioridad = 'HIGH'
        """, (week_ago,))
        
        critical_alerts = cursor.fetchone()[0]
        
        report = {
            'period': 'Últimos 7 días',
            'generated_at': datetime.now().isoformat(),
            'kpis': {
                'total_pods': kpis[0],
                'valid_pods': kpis[1],
                'invalid_pods': kpis[2],
                'validation_rate': round(kpis[1] / kpis[0] * 100, 1) if kpis[0] > 0 else 0
            },
            'by_classification': by_class,
            'critical_alerts': critical_alerts,
            'recommendations': self._generate_recommendations(kpis, by_class, critical_alerts)
        }
        
        logger.info(f"Reporte semanal generado: {report['kpis']['total_pods']} PODs procesados")
        return report
    
    def _generate_recommendations(self, kpis, by_class, critical_alerts) -> List[str]:
        """
        Genera recomendaciones automáticas basadas en métricas
        """
        recommendations = []
        
        validation_rate = (kpis[1] / kpis[0] * 100) if kpis[0] > 0 else 0
        
        if validation_rate < 70:
            recommendations.append("⚠️ Tasa de validación baja (<70%). Revisar proceso de recepción.")
        
        if critical_alerts > 10:
            recommendations.append(f"🔴 {critical_alerts} alertas críticas. Revisar reclamaciones urgentes.")
        
        sin_acuse = by_class.get('SIN_ACUSE', 0)
        if sin_acuse > kpis[0] * 0.3:
            recommendations.append("⚠️ Más del 30% de PODs sin acuse. Reforzar política de firmas.")
        
        if not recommendations:
            recommendations.append("✅ Métricas saludables. Continuar con proceso actual.")
        
        return recommendations


class SentimentTrendAnalyzer:
    """Analiza tendencias de sentimiento en el tiempo"""
    
    def __init__(self, db_connection):
        self.conn = db_connection
    
    def analyze_sentiment_trend(self, client_name: str = None, days: int = 30) -> Dict[str, Any]:
        """
        Analiza tendencia de sentimiento (para detectar deterioro en satisfacción)
        """
        cursor = self.conn.cursor()
        
        date_limit = (datetime.now() - timedelta(days=days)).isoformat()
        
        query = """
            SELECT 
                strftime('%W', fecha_analisis) as week,
                manuscritos_sentimiento,
                COUNT(*) as count
            FROM gemini_analisis
            WHERE fecha_analisis >= ?
        """
        
        params = [date_limit]
        
        if client_name:
            query += " AND cliente LIKE ?"
            params.append(f'%{client_name}%')
        
        query += " GROUP BY week, manuscritos_sentimiento ORDER BY week"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        # Calcular tendencia
        weeks_data = {}
        for week, sentiment, count in results:
            if week not in weeks_data:
                weeks_data[week] = {'positive': 0, 'negative': 0, 'neutral': 0}
            weeks_data[week][sentiment] = count
        
        # Analizar tendencia
        trend_direction = 'stable'
        if len(weeks_data) >= 3:
            weeks_list = sorted(weeks_data.items())
            first_week = weeks_list[0][1]
            last_week = weeks_list[-1][1]
            
            first_negative_rate = first_week.get('negative', 0) / sum(first_week.values()) if sum(first_week.values()) > 0 else 0
            last_negative_rate = last_week.get('negative', 0) / sum(last_week.values()) if sum(last_week.values()) > 0 else 0
            
            if last_negative_rate > first_negative_rate + 0.1:
                trend_direction = 'deteriorating'
            elif last_negative_rate < first_negative_rate - 0.1:
                trend_direction = 'improving'
        
        return {
            'trend': trend_direction,
            'weeks_analyzed': len(weeks_data),
            'data': weeks_data,
            'alert': trend_direction == 'deteriorating',
            'recommendation': 'Contactar cliente proactivamente' if trend_direction == 'deteriorating' else 'Continuar monitoreo'
        }


class AutomatedReportScheduler:
    """Programador de reportes automáticos"""
    
    def __init__(self, report_config: Dict = None):
        self.config = report_config or {
            'frequency': 'weekly',
            'recipients': [],
            'format': 'pdf'
        }
        logger.info("Programador de reportes inicializado")
    
    def schedule_report(self, report_type: str, frequency: str = 'weekly'):
        """
        Programa generación automática de reportes
        """
        # NOTA: Requiere configuración de scheduler (cron/celery)
        logger.info(f"Reporte {report_type} programado: {frequency}")
        
        return {
            'scheduled': True,
            'type': report_type,
            'frequency': frequency,
            'next_run': 'Configurar con Task Scheduler o Cron'
        }

