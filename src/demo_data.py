# -*- coding: utf-8 -*-
"""
Datos de demostración para Streamlit Cloud
Resultados pre-calculados para mostrar funcionalidad sin necesidad de procesar
"""

import json

# Datos de ejemplo basados en PODs reales procesados
DEMO_RESULTS = [
    {
        "source_file": "QC8261_1024008261.jpg",
        "classification": "Poco Legible",
        "classification_code": "POCO_LEGIBLE",
        "is_valid": False,
        "confidence": 0.85,
        "details": {
            "signatures": [
                {"region": "zone_7", "confidence": 0.82},
                {"region": "zone_8", "confidence": 0.75}
            ],
            "stamps": [
                {"type": "circular", "is_valid": False, "text": "deacero"}
            ],
            "annotations": {
                "has_annotations": True,
                "annotation_count": 5,
                "sentiment": "neutral"
            },
            "legibility": {
                "is_legible": False,
                "fields_detected": ["factura", "cliente", "pedido"],
                "fields_missing": ["producto", "firma"],
                "ocr_confidence": 51.7,
                "text_quality": 0.36
            }
        },
        "issues": [
            "Campos insuficientes detectados: 3/5",
            "Calidad de texto baja: 0.36/0.6",
            "Sello inválido: Deacero"
        ]
    },
    {
        "source_file": "QM2015_1033002015.jpg",
        "classification": "Poco Legible",
        "classification_code": "POCO_LEGIBLE",
        "is_valid": False,
        "confidence": 0.85,
        "details": {
            "signatures": [
                {"region": "zone_6", "confidence": 0.88},
                {"region": "zone_7", "confidence": 0.91},
                {"region": "zone_8", "confidence": 0.85}
            ],
            "stamps": [
                {"type": "rectangular", "is_valid": True}
            ],
            "annotations": {
                "has_annotations": True,
                "annotation_count": 3,
                "sentiment": "neutral"
            },
            "legibility": {
                "is_legible": False,
                "fields_detected": [],
                "fields_missing": ["factura", "cliente", "pedido", "producto", "firma"],
                "ocr_confidence": 44.2,
                "text_quality": 0.32
            }
        },
        "issues": [
            "Campos insuficientes detectados: 0/5",
            "Confianza OCR baja: 44.2/60"
        ]
    },
    {
        "source_file": "QP7957_1036007957.jpg",
        "classification": "Incorrecto",
        "classification_code": "INCORRECTO",
        "is_valid": False,
        "confidence": 0.90,
        "details": {
            "signatures": [
                {"region": "zone_7", "confidence": 0.79},
                {"region": "zone_8", "confidence": 0.82}
            ],
            "stamps": [
                {"type": "circular", "is_valid": True}
            ],
            "annotations": {
                "has_annotations": True,
                "annotation_count": 6,
                "sentiment": "neutral"
            },
            "legibility": {
                "is_legible": False,
                "fields_detected": [],
                "fields_missing": ["factura", "cliente", "pedido", "producto", "firma"],
                "ocr_confidence": 38.5,
                "text_quality": 0.28
            }
        },
        "issues": [
            "Documento no completamente digitalizado (cortado o parcial)"
        ]
    },
    {
        "source_file": "DEMO_POD_OK_001.jpg",
        "classification": "OK",
        "classification_code": "OK",
        "is_valid": True,
        "confidence": 0.95,
        "details": {
            "signatures": [
                {"region": "zone_7", "confidence": 0.92}
            ],
            "stamps": [
                {"type": "circular", "is_valid": True, "text": "Cliente ABC"}
            ],
            "annotations": {
                "has_annotations": True,
                "annotation_count": 1,
                "sentiment": "positive",
                "text_content": ["Recibido conforme"]
            },
            "legibility": {
                "is_legible": True,
                "fields_detected": ["factura", "cliente", "pedido", "producto"],
                "fields_missing": [],
                "ocr_confidence": 85.3,
                "text_quality": 0.82
            }
        },
        "issues": [
            "Firma válida detectada (1 firma)",
            "Sello válido del cliente detectado",
            "Contiene anotaciones positivas confirmando recepción"
        ]
    },
    {
        "source_file": "DEMO_POD_SIN_ACUSE_001.jpg",
        "classification": "Sin Acuse",
        "classification_code": "SIN_ACUSE",
        "is_valid": False,
        "confidence": 0.90,
        "details": {
            "signatures": [],
            "stamps": [],
            "annotations": {
                "has_annotations": False,
                "annotation_count": 0,
                "sentiment": "neutral"
            },
            "legibility": {
                "is_legible": True,
                "fields_detected": ["factura", "cliente", "pedido", "producto"],
                "fields_missing": ["firma"],
                "ocr_confidence": 78.5,
                "text_quality": 0.75
            }
        },
        "issues": [
            "Documento sin evidencia de acuse (sin firma, sello o anotaciones)"
        ]
    }
]


def get_demo_results():
    """
    Retorna resultados de demo para mostrar funcionalidad
    """
    return DEMO_RESULTS


def get_demo_statistics():
    """
    Calcula estadísticas de los datos de demo
    """
    total = len(DEMO_RESULTS)
    valid = sum(1 for r in DEMO_RESULTS if r['is_valid'])
    
    stats = {
        'total': total,
        'valid': valid,
        'invalid': total - valid,
        'percentage': (valid / total * 100) if total > 0 else 0,
        'by_classification': {}
    }
    
    for result in DEMO_RESULTS:
        code = result['classification_code']
        stats['by_classification'][code] = stats['by_classification'].get(code, 0) + 1
    
    return stats

