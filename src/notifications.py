# -*- coding: utf-8 -*-
"""
Sistema de Notificaciones y Alertas
Envía alertas cuando se detectan PODs con problemas
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, Any, List
from loguru import logger
import json


class NotificationSystem:
    """
    Sistema de notificaciones para alertas de PODs
    """
    
    def __init__(self, config_path: str = "config/notifications.json"):
        """
        Inicializa el sistema de notificaciones
        
        Args:
            config_path: Ruta al archivo de configuración
        """
        self.config = self._load_config(config_path)
        self.enabled = self.config.get('enabled', False)
        self.alerts_log = []
        
        if self.enabled:
            logger.info("Sistema de notificaciones habilitado")
        else:
            logger.info("Sistema de notificaciones deshabilitado")
    
    def _load_config(self, config_path: str) -> Dict:
        """Carga configuración de notificaciones"""
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'enabled': False,
            'email': {
                'enabled': False,
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'sender_email': '',
                'sender_password': '',
                'recipients': []
            },
            'alerts': {
                'negative_annotations': True,
                'sin_acuse_threshold': 10,
                'poco_legible_threshold': 20,
                'processing_complete': True
            }
        }
    
    def check_and_alert(self, result: Dict[str, Any]) -> List[Dict]:
        """
        Verifica si un resultado requiere alerta
        
        Args:
            result: Resultado de clasificación del POD
            
        Returns:
            Lista de alertas generadas
        """
        alerts = []
        
        # ALERTA 1: Anotación Negativa (Reclamación)
        if result['details']['annotations'].get('sentiment') == 'negative':
            alert = {
                'type': '🔴 URGENTE',
                'priority': 'HIGH',
                'title': 'POD con Reclamación Detectada',
                'message': f"POD: {result['source_file']}\n"
                          f"Tiene anotaciones NEGATIVAS que indican reclamación.\n"
                          f"Anotaciones: {result['details']['annotations'].get('text_content', [])}\n"
                          f"ACCIÓN REQUERIDA: Revisar inmediatamente",
                'pod_file': result['source_file'],
                'timestamp': datetime.now()
            }
            alerts.append(alert)
            self._send_alert(alert)
        
        # ALERTA 2: Sin Acuse (No tiene firma ni sello)
        if result['classification_code'] == 'SIN_ACUSE':
            alert = {
                'type': '⚠️ Advertencia',
                'priority': 'MEDIUM',
                'title': 'POD Sin Acuse de Recibo',
                'message': f"POD: {result['source_file']}\n"
                          f"No tiene firma, sello ni anotaciones.\n"
                          f"ACCIÓN: Solicitar POD con firma del cliente",
                'pod_file': result['source_file'],
                'timestamp': datetime.now()
            }
            alerts.append(alert)
        
        # ALERTA 3: Documento Incorrecto (Cortado)
        if result['classification_code'] == 'INCORRECTO':
            alert = {
                'type': '❌ Error',
                'priority': 'MEDIUM',
                'title': 'POD Incompleto o Cortado',
                'message': f"POD: {result['source_file']}\n"
                          f"Documento no completamente digitalizado.\n"
                          f"ACCIÓN: Re-escanear el documento completo",
                'pod_file': result['source_file'],
                'timestamp': datetime.now()
            }
            alerts.append(alert)
        
        # Guardar alertas
        self.alerts_log.extend(alerts)
        
        return alerts
    
    def _send_alert(self, alert: Dict):
        """
        Envía una alerta por el canal configurado
        """
        if not self.enabled:
            return
        
        # Log siempre
        logger.warning(f"{alert['type']} - {alert['title']}: {alert['pod_file']}")
        
        # Email si está configurado
        if self.config['email']['enabled']:
            self._send_email_alert(alert)
    
    def _send_email_alert(self, alert: Dict):
        """
        Envía alerta por email
        """
        try:
            email_config = self.config['email']
            
            # Crear mensaje
            msg = MIMEMultipart()
            msg['From'] = email_config['sender_email']
            msg['To'] = ', '.join(email_config['recipients'])
            msg['Subject'] = f"{alert['type']} - {alert['title']}"
            
            body = f"""
<html>
<body>
<h2 style="color: red;">{alert['type']} {alert['title']}</h2>

<p><strong>POD:</strong> {alert['pod_file']}</p>

<p><strong>Mensaje:</strong></p>
<p>{alert['message'].replace(chr(10), '<br>')}</p>

<p><strong>Fecha/Hora:</strong> {alert['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</p>

<hr>
<p><em>Sistema de Validación de PODs - Alerta Automática</em></p>
</body>
</html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Enviar email
            with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
                server.starttls()
                server.login(email_config['sender_email'], email_config['sender_password'])
                server.send_message(msg)
            
            logger.info(f"Alerta enviada por email: {alert['title']}")
            
        except Exception as e:
            logger.error(f"Error enviando email: {e}")
    
    def generate_summary_alert(self, results: List[Dict[str, Any]]):
        """
        Genera alerta resumen al finalizar procesamiento
        """
        if not self.enabled:
            return
        
        if not self.config['alerts']['processing_complete']:
            return
        
        # Calcular estadísticas
        total = len(results)
        valid = sum(1 for r in results if r['is_valid'])
        invalid = total - valid
        
        # Contar por tipo
        sin_acuse = sum(1 for r in results if r['classification_code'] == 'SIN_ACUSE')
        poco_legible = sum(1 for r in results if r['classification_code'] == 'POCO_LEGIBLE')
        incorrecto = sum(1 for r in results if r['classification_code'] == 'INCORRECTO')
        con_anotaciones_neg = sum(1 for r in results 
                                  if r['details']['annotations'].get('sentiment') == 'negative')
        
        # Crear alerta de resumen
        alert = {
            'type': '📊 Resumen',
            'priority': 'LOW',
            'title': f'Procesamiento Completado - {total} PODs',
            'message': f"""
RESUMEN DE PROCESAMIENTO:

Total PODs procesados: {total}
✅ Válidos: {valid} ({valid/total*100:.1f}%)
❌ Con defectos: {invalid} ({invalid/total*100:.1f}%)

DESGLOSE:
⚠️ Sin Acuse: {sin_acuse}
❌ Poco Legible: {poco_legible}
❌ Incorrecto: {incorrecto}
🔴 Con Reclamaciones: {con_anotaciones_neg}

ALERTAS GENERADAS: {len(self.alerts_log)}

Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """,
            'timestamp': datetime.now()
        }
        
        self._send_alert(alert)
        
        # Alerta especial si hay muchos problemas
        if sin_acuse >= self.config['alerts']['sin_acuse_threshold']:
            urgent_alert = {
                'type': '🔴 URGENTE',
                'priority': 'HIGH',
                'title': f'Alerta: {sin_acuse} PODs Sin Acuse',
                'message': f"Se detectaron {sin_acuse} PODs sin acuse de recibo.\n"
                          f"Esto supera el umbral de {self.config['alerts']['sin_acuse_threshold']}.\n"
                          f"ACCIÓN: Revisar proceso de recepción",
                'timestamp': datetime.now()
            }
            self._send_alert(urgent_alert)
    
    def get_alerts_log(self) -> List[Dict]:
        """
        Retorna el log de alertas generadas
        """
        return self.alerts_log
    
    def save_alerts_to_file(self, filepath: str = "resultados/alertas.json"):
        """
        Guarda las alertas en un archivo
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.alerts_log, f, indent=2, ensure_ascii=False, default=str)
            logger.info(f"Alertas guardadas en: {filepath}")
        except Exception as e:
            logger.error(f"Error guardando alertas: {e}")


def create_default_notification_config():
    """
    Crea un archivo de configuración de notificaciones por defecto
    """
    config = {
        "enabled": True,
        "email": {
            "enabled": False,
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "tu-email@gmail.com",
            "sender_password": "tu-contraseña-de-app",
            "recipients": [
                "supervisor@empresa.com",
                "validador@empresa.com"
            ]
        },
        "alerts": {
            "negative_annotations": True,
            "sin_acuse_threshold": 10,
            "poco_legible_threshold": 20,
            "incorrecto_threshold": 15,
            "processing_complete": True
        },
        "alert_levels": {
            "HIGH": ["negative_annotations"],
            "MEDIUM": ["sin_acuse", "incorrecto"],
            "LOW": ["processing_complete"]
        }
    }
    
    os.makedirs('config', exist_ok=True)
    with open('config/notifications.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    logger.info("Configuración de notificaciones creada: config/notifications.json")

