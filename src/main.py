# -*- coding: utf-8 -*-
"""
Sistema de Validación de PODs (Proof of Delivery)
Aplicación principal
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd
from datetime import datetime
from loguru import logger
import cv2

# Configurar logger
logger.remove()
logger.add(sys.stderr, format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>")
logger.add("logs/pod_validation_{time}.log", rotation="1 day", retention="7 days")

from utils import (
    load_config, 
    ensure_directories, 
    get_files_from_directory,
    save_annotated_image,
    generate_timestamp,
    sanitize_filename,
    draw_zone
)
from processor import DocumentProcessor
from classifier import PODClassifier

# Importar base de datos si está disponible
try:
    from database import PODDatabase
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    logger.warning("Módulo de base de datos no disponible")


class PODValidationSystem:
    """
    Sistema principal de validación de PODs
    """
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        """
        Inicializa el sistema de validación
        
        Args:
            config_path: Ruta al archivo de configuración
        """
        logger.info("=" * 80)
        logger.info("SISTEMA DE VALIDACIÓN DE PODs (PROOF OF DELIVERY)")
        logger.info("=" * 80)
        
        # Cargar configuración
        self.config = load_config(config_path)
        if not self.config:
            logger.error("No se pudo cargar la configuración. Saliendo...")
            sys.exit(1)
        
        # Asegurar directorios
        ensure_directories(self.config)
        
        # Inicializar componentes
        self.processor = DocumentProcessor(self.config)
        self.classifier = PODClassifier(self.config)
        
        # Inicializar base de datos si está disponible
        if DATABASE_AVAILABLE:
            self.db = PODDatabase()
            logger.info("Base de datos conectada")
        else:
            self.db = None
        
        logger.info("Sistema inicializado correctamente")
    
    def process_single_file(self, file_path: str, save_annotated: bool = True) -> Dict[str, Any]:
        """
        Procesa un solo archivo POD
        
        Args:
            file_path: Ruta al archivo
            save_annotated: Si se deben guardar imágenes anotadas
            
        Returns:
            Resultado de la clasificación
        """
        logger.info(f"\nProcesando archivo: {file_path}")
        
        # Obtener información del documento
        doc_info = self.processor.get_document_info(file_path)
        logger.info(f"Tamaño: {doc_info['size_mb']} MB | Formato: {doc_info['extension']}")
        
        # Procesar documento
        pages = self.processor.process_document(file_path)
        
        if not pages:
            logger.error(f"No se pudo procesar el documento: {file_path}")
            return None
        
        # Procesar cada página (típicamente 1 para PODs)
        results = []
        
        for page_data in pages:
            # Extraer zonas de interés
            zones = self.processor.extract_zones(page_data)
            
            # Clasificar
            result = self.classifier.classify_document(page_data, zones)
            
            # Agregar información del documento
            result['document_info'] = doc_info
            
            # Generar imagen anotada si se solicita
            if save_annotated and self.config['output']['save_annotated_images']:
                annotated_image = self._create_annotated_image(page_data, result, zones)
                
                # Guardar imagen anotada
                output_dir = os.path.join(self.config['paths']['output_dir'], 'imagenes_anotadas')
                filename = f"{sanitize_filename(Path(file_path).stem)}_page{page_data['page_number']}.jpg"
                output_path = os.path.join(output_dir, filename)
                save_annotated_image(annotated_image, output_path)
                
                result['annotated_image_path'] = output_path
            
            results.append(result)
            
            # Guardar en base de datos si está disponible
            if self.db:
                try:
                    pod_id = self.db.save_pod_result(result)
                    logger.debug(f"Resultado guardado en BD (ID: {pod_id})")
                except Exception as e:
                    logger.error(f"Error guardando en BD: {e}")
            
            # Mostrar resultado
            try:
                self._print_classification_result(result)
            except Exception as e:
                logger.debug(f"Error al imprimir resultado: {e}")
        
        return results[0] if len(results) == 1 else results
    
    def process_directory(self, input_dir: str = None) -> List[Dict[str, Any]]:
        """
        Procesa todos los archivos POD en un directorio
        
        Args:
            input_dir: Directorio de entrada (usa config por defecto si no se especifica)
            
        Returns:
            Lista de resultados de clasificación
        """
        if input_dir is None:
            input_dir = self.config['paths']['input_dir']
        
        logger.info(f"\nProcesando directorio: {input_dir}")
        
        # Obtener archivos
        files = get_files_from_directory(input_dir, self.config['supported_formats'])
        
        if not files:
            logger.warning(f"No se encontraron archivos en {input_dir}")
            return []
        
        logger.info(f"Encontrados {len(files)} archivo(s) para procesar\n")
        
        # Procesar cada archivo
        all_results = []
        
        for idx, file_path in enumerate(files, 1):
            logger.info(f"[{idx}/{len(files)}] " + "=" * 60)
            
            try:
                result = self.process_single_file(file_path)
                if result:
                    all_results.append(result)
            except Exception as e:
                logger.error(f"Error procesando {file_path}: {e}")
                continue
        
        logger.info("\n" + "=" * 80)
        logger.info("PROCESAMIENTO COMPLETADO")
        logger.info("=" * 80)
        
        # Generar reportes
        if all_results:
            self._generate_reports(all_results)
        
        return all_results
    
    def _create_annotated_image(self, page_data: Dict[str, Any], 
                               result: Dict[str, Any],
                               zones: Dict[str, Any]) -> Any:
        """
        Crea una imagen anotada con todas las detecciones
        
        Args:
            page_data: Datos de la página
            result: Resultado de clasificación
            zones: Zonas extraídas
            
        Returns:
            Imagen anotada
        """
        from detectors.signature_detector import SignatureDetector
        from detectors.stamp_detector import StampDetector
        from detectors.annotation_detector import AnnotationDetector
        from utils import get_zone_coordinates
        
        # Copiar imagen original
        annotated = page_data['original_image'].copy()
        
        # Dibujar zonas de firma (6, 7, 8)
        for zone_name in ['zone_6', 'zone_7', 'zone_8']:
            if zone_name in self.config['zones']:
                zone_coords = get_zone_coordinates(annotated, self.config['zones'][zone_name])
                annotated = draw_zone(annotated, zone_coords, zone_name.upper(), (255, 200, 0))
        
        # Dibujar firmas detectadas
        if result['details']['signatures']:
            sig_detector = SignatureDetector(self.config)
            annotated = sig_detector.draw_signatures(annotated, result['details']['signatures'])
        
        # Dibujar sellos detectados
        if result['details']['stamps']:
            stamp_detector = StampDetector(self.config)
            annotated = stamp_detector.draw_stamps(annotated, result['details']['stamps'])
        
        # Dibujar anotaciones
        if result['details']['annotations']['has_annotations']:
            ann_detector = AnnotationDetector(self.config)
            annotated = ann_detector.draw_annotations(annotated, result['details']['annotations'])
        
        # Agregar información de clasificación en la imagen
        classification = result['classification']
        confidence = result['confidence']
        is_valid = result['is_valid']
        
        # Color del título según validez
        title_color = (0, 255, 0) if is_valid else (0, 0, 255)
        
        # Agregar texto en la parte superior
        cv2.putText(annotated, f"CLASIFICACION: {classification}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, title_color, 3)
        cv2.putText(annotated, f"Confianza: {confidence:.1%} | Valido: {'SI' if is_valid else 'NO'}", 
                   (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, title_color, 2)
        
        return annotated
    
    def _print_classification_result(self, result: Dict[str, Any]) -> None:
        """
        Imprime el resultado de clasificación de forma legible
        
        Args:
            result: Resultado de clasificación
        """
        print("\n" + "=" * 60)
        print(f"RESULTADO DE CLASIFICACIÓN")
        print("=" * 60)
        print(f"Archivo: {result['source_file']}")
        print(f"Página: {result['page_number']}")
        print(f"\nClasificación: {result['classification']}")
        print(f"Código: {result['classification_code']}")
        print(f"Confianza: {result['confidence']:.1%}")
        print(f"Válido: {'[OK] SI' if result['is_valid'] else '[X] NO'}")
        
        if result['issues']:
            print(f"\nDetalles:")
            for issue in result['issues']:
                print(f"  - {issue}")
        
        if result['recommendations']:
            print(f"\nRecomendaciones:")
            for rec in result['recommendations']:
                print(f"  > {rec}")
        
        print("=" * 60)
    
    def _generate_reports(self, results: List[Dict[str, Any]]) -> None:
        """
        Genera reportes en Excel y CSV
        
        Args:
            results: Lista de resultados
        """
        logger.info("\nGenerando reportes...")
        
        # Preparar datos para el reporte
        report_data = []
        
        for result in results:
            row = {
                'Archivo': result['document_info']['filename'],
                'Ruta': result['document_info']['filepath'],
                'Página': result['page_number'],
                'Clasificación': result['classification'],
                'Código': result['classification_code'],
                'Válido': 'SÍ' if result['is_valid'] else 'NO',
                'Confianza': f"{result['confidence']:.1%}",
                'Firmas_Detectadas': len(result['details'].get('signatures', [])),
                'Sellos_Detectados': len(result['details'].get('stamps', [])),
                'Tiene_Anotaciones': 'SÍ' if result['details']['annotations']['has_annotations'] else 'NO',
                'Sentimiento_Anotaciones': result['details']['annotations'].get('sentiment', 'N/A'),
                'Legible': 'SÍ' if result['details']['legibility']['is_legible'] else 'NO',
                'Calidad_Texto': f"{result['details']['legibility']['text_quality']:.2f}",
                'Campos_Detectados': ', '.join(result['details']['legibility']['fields_detected']),
                'Campos_Faltantes': ', '.join(result['details']['legibility']['fields_missing']),
                'Problemas': ' | '.join(result['issues']),
                'Recomendaciones': ' | '.join(result['recommendations']),
                'Tamaño_MB': result['document_info']['size_mb'],
            }
            report_data.append(row)
        
        # Crear DataFrame
        df = pd.DataFrame(report_data)
        
        # Generar timestamp
        timestamp = generate_timestamp()
        report_dir = os.path.join(self.config['paths']['output_dir'], 'reportes')
        
        # Guardar Excel
        if self.config['output']['generate_excel_report']:
            excel_path = os.path.join(report_dir, f'reporte_pods_{timestamp}.xlsx')
            df.to_excel(excel_path, index=False, sheet_name='Resultados')
            logger.info(f"Reporte Excel generado: {excel_path}")
        
        # Guardar CSV
        if self.config['output']['generate_csv_report']:
            csv_path = os.path.join(report_dir, f'reporte_pods_{timestamp}.csv')
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            logger.info(f"Reporte CSV generado: {csv_path}")
        
        # Generar resumen
        summary = self.classifier.get_classification_summary(results)
        self._print_summary(summary)
        
        # Guardar resumen
        summary_path = os.path.join(report_dir, f'resumen_{timestamp}.txt')
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("RESUMEN DE VALIDACIÓN DE PODs\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Total de documentos procesados: {summary['total_documents']}\n")
            f.write(f"Documentos válidos: {summary['valid_documents']}\n")
            f.write(f"Documentos inválidos: {summary['invalid_documents']}\n")
            f.write(f"Tasa de validación: {summary['validation_rate']:.1f}%\n\n")
            f.write("Distribución por clasificación:\n")
            for classification, count in summary['by_classification'].items():
                f.write(f"  {classification}: {count}\n")
        
        logger.info(f"Resumen guardado: {summary_path}")
    
    def _print_summary(self, summary: Dict[str, Any]) -> None:
        """
        Imprime el resumen de procesamiento
        
        Args:
            summary: Diccionario con resumen
        """
        print("\n" + "=" * 80)
        print("RESUMEN DE PROCESAMIENTO")
        print("=" * 80)
        print(f"\nTotal de documentos: {summary['total_documents']}")
        print(f"Documentos válidos: {summary['valid_documents']} ✓")
        print(f"Documentos inválidos: {summary['invalid_documents']} ✗")
        print(f"Tasa de validación: {summary['validation_rate']:.1f}%")
        
        print(f"\nDistribución por clasificación:")
        for classification, count in summary['by_classification'].items():
            percentage = (count / summary['total_documents'] * 100) if summary['total_documents'] > 0 else 0
            print(f"  {classification:20s}: {count:3d} ({percentage:5.1f}%)")
        
        if summary['issues_summary']:
            print(f"\nProblemas más comunes:")
            for item in summary['issues_summary'][:5]:
                print(f"  • {item['issue'][:70]}: {item['count']} veces")
        
        print("=" * 80)


def main():
    """
    Función principal
    """
    parser = argparse.ArgumentParser(
        description='Sistema de Validación de PODs (Proof of Delivery)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py                              # Procesar directorio por defecto
  python main.py --input documentos/entrada   # Procesar directorio específico
  python main.py --file documento.pdf         # Procesar un solo archivo
  python main.py --interactive                # Modo interactivo
        """
    )
    
    parser.add_argument('--input', '-i', type=str, 
                       help='Directorio de entrada con documentos POD')
    parser.add_argument('--file', '-f', type=str,
                       help='Procesar un solo archivo')
    parser.add_argument('--output', '-o', type=str,
                       help='Directorio de salida para resultados')
    parser.add_argument('--config', '-c', type=str, default='config/settings.yaml',
                       help='Ruta al archivo de configuración')
    parser.add_argument('--interactive', action='store_true',
                       help='Modo interactivo con visualización')
    parser.add_argument('--no-annotated', action='store_true',
                       help='No guardar imágenes anotadas')
    
    args = parser.parse_args()
    
    # Inicializar sistema
    system = PODValidationSystem(args.config)
    
    # Procesar según argumentos
    if args.file:
        # Procesar un solo archivo
        system.process_single_file(args.file, save_annotated=not args.no_annotated)
    
    elif args.interactive:
        # Modo interactivo
        print("\nModo interactivo no implementado aún")
        print("Use: python main.py --input <directorio> o --file <archivo>")
    
    else:
        # Procesar directorio
        input_dir = args.input if args.input else None
        system.process_directory(input_dir)


if __name__ == "__main__":
    main()

