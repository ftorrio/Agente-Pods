# -*- coding: utf-8 -*-
"""
Módulo de detectores para análisis de PODs
"""

from .signature_detector import SignatureDetector
from .stamp_detector import StampDetector
from .legibility_analyzer import LegibilityAnalyzer
from .annotation_detector import AnnotationDetector

__all__ = [
    'SignatureDetector',
    'StampDetector',
    'LegibilityAnalyzer',
    'AnnotationDetector'
]

