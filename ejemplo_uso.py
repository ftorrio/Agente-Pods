# -*- coding: utf-8 -*-
"""
Ejemplo de uso del Sistema de Validación de PODs
Demuestra cómo usar el sistema programáticamente
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import PODValidationSystem


def ejemplo_basico():
    """
    Ejemplo básico: Procesar todos los documentos del directorio por defecto
    """
    print("\n=== EJEMPLO 1: Procesamiento Básico ===\n")
    
    # Inicializar el sistema
    system = PODValidationSystem()
    
    # Procesar todos los documentos en documentos/entrada/
    resultados = system.process_directory()
    
    print(f"\nSe procesaron {len(resultados)} documento(s)")
    

def ejemplo_archivo_individual():
    """
    Ejemplo: Procesar un archivo específico
    """
    print("\n=== EJEMPLO 2: Archivo Individual ===\n")
    
    # Ruta al archivo
    archivo = "documentos/entrada/mi_pod.pdf"
    
    # Verificar que existe
    if not os.path.exists(archivo):
        print(f"NOTA: El archivo {archivo} no existe.")
        print("Coloca un archivo POD en esa ubicación para probar este ejemplo.")
        return
    
    # Inicializar el sistema
    system = PODValidationSystem()
    
    # Procesar el archivo
    resultado = system.process_single_file(archivo)
    
    if resultado:
        print(f"\nResultado:")
        print(f"  Clasificación: {resultado['classification']}")
        print(f"  Válido: {'SÍ' if resultado['is_valid'] else 'NO'}")
        print(f"  Confianza: {resultado['confidence']:.1%}")


def ejemplo_con_analisis_detallado():
    """
    Ejemplo: Acceder a detalles del análisis
    """
    print("\n=== EJEMPLO 3: Análisis Detallado ===\n")
    
    archivo = "documentos/entrada/mi_pod.pdf"
    
    if not os.path.exists(archivo):
        print(f"NOTA: El archivo {archivo} no existe.")
        print("Coloca un archivo POD en esa ubicación para probar este ejemplo.")
        return
    
    system = PODValidationSystem()
    resultado = system.process_single_file(archivo, save_annotated=True)
    
    if resultado:
        print(f"\n--- INFORMACIÓN DETALLADA ---")
        
        # Información de legibilidad
        legibilidad = resultado['details']['legibility']
        print(f"\nLegibilidad:")
        print(f"  Es legible: {'SÍ' if legibilidad['is_legible'] else 'NO'}")
        print(f"  Calidad del texto: {legibilidad['text_quality']:.2f}")
        print(f"  Confianza OCR: {legibilidad['ocr_confidence']:.1f}")
        print(f"  Campos detectados: {', '.join(legibilidad['fields_detected'])}")
        
        # Información de firmas
        firmas = resultado['details']['signatures']
        print(f"\nFirmas:")
        print(f"  Cantidad detectada: {len(firmas)}")
        for i, firma in enumerate(firmas, 1):
            print(f"    Firma {i}: Región {firma['region']}, Confianza {firma['confidence']:.2f}")
        
        # Información de sellos
        sellos = resultado['details']['stamps']
        print(f"\nSellos:")
        print(f"  Cantidad detectada: {len(sellos)}")
        validos = [s for s in sellos if s['is_valid']]
        print(f"  Sellos válidos: {len(validos)}")
        
        # Información de anotaciones
        anotaciones = resultado['details']['annotations']
        print(f"\nAnotaciones:")
        print(f"  Tiene anotaciones: {'SÍ' if anotaciones['has_annotations'] else 'NO'}")
        if anotaciones['has_annotations']:
            print(f"  Sentimiento: {anotaciones['sentiment']}")
            print(f"  Cantidad: {anotaciones['annotation_count']}")


def ejemplo_procesamiento_lote():
    """
    Ejemplo: Procesar un lote de documentos y analizar estadísticas
    """
    print("\n=== EJEMPLO 4: Procesamiento por Lote ===\n")
    
    system = PODValidationSystem()
    resultados = system.process_directory()
    
    if not resultados:
        print("No hay documentos para procesar en documentos/entrada/")
        print("Coloca algunos archivos POD allí para probar este ejemplo.")
        return
    
    # Analizar estadísticas
    print(f"\n--- ESTADÍSTICAS DEL LOTE ---")
    
    total = len(resultados)
    validos = sum(1 for r in resultados if r['is_valid'])
    invalidos = total - validos
    
    print(f"\nTotal procesados: {total}")
    print(f"Válidos: {validos} ({validos/total*100:.1f}%)")
    print(f"Inválidos: {invalidos} ({invalidos/total*100:.1f}%)")
    
    # Agrupar por clasificación
    from collections import Counter
    clasificaciones = Counter(r['classification_code'] for r in resultados)
    
    print(f"\nDistribución:")
    for clasificacion, cantidad in clasificaciones.items():
        print(f"  {clasificacion}: {cantidad}")
    
    # Problemas más comunes
    todos_problemas = []
    for r in resultados:
        todos_problemas.extend(r['issues'])
    
    problema_counts = Counter(todos_problemas)
    print(f"\nProblemas más comunes:")
    for problema, count in problema_counts.most_common(5):
        print(f"  • {problema[:60]}... ({count} veces)")


def ejemplo_configuracion_personalizada():
    """
    Ejemplo: Usar configuración personalizada
    """
    print("\n=== EJEMPLO 5: Configuración Personalizada ===\n")
    
    # Crear archivo de configuración personalizado si no existe
    config_personalizado = "config/mi_config.yaml"
    
    if not os.path.exists(config_personalizado):
        print(f"Para este ejemplo, crea un archivo de configuración personalizado en:")
        print(f"  {config_personalizado}")
        print(f"\nPuedes copiar config/settings.yaml y modificarlo.")
        return
    
    # Usar configuración personalizada
    system = PODValidationSystem(config_path=config_personalizado)
    resultados = system.process_directory()
    
    print(f"Procesados {len(resultados)} documentos con configuración personalizada")


def main():
    """
    Función principal que ejecuta todos los ejemplos
    """
    print("=" * 80)
    print("EJEMPLOS DE USO - Sistema de Validación de PODs")
    print("=" * 80)
    
    # Puedes comentar/descomentar los ejemplos que quieras ejecutar
    
    ejemplo_basico()
    
    # ejemplo_archivo_individual()
    
    # ejemplo_con_analisis_detallado()
    
    # ejemplo_procesamiento_lote()
    
    # ejemplo_configuracion_personalizada()
    
    print("\n" + "=" * 80)
    print("Para más información, consulta GUIA_USO.md")
    print("=" * 80)


if __name__ == "__main__":
    main()

