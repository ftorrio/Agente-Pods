# Sistema de Validación de PODs (Proof of Delivery)

## Descripción
Sistema automatizado para la validación e inspección visual de documentos POD (Pruebas de Entrega) en formatos PDF, GIF, PNG, JPG, etc.

## Características

El sistema clasifica automáticamente los PODs en las siguientes categorías:

### 1. Poco Legible ❌
Documentos donde los campos de **Factura, Cliente, Pedido, Productos y Firmas** no son completamente distinguibles.

### 2. Sin Acuse ⚠️
El documento digitalizado es solo la remisión, sin ninguna anotación a mano, firma o sello.

### 3. Incorrecto ❌
El documento no fue totalmente digitalizado (cortado o parcialmente digitalizado).

### 4. Con Anotaciones 📝
El documento cuenta con anotaciones o comentarios escritos a mano. Se analiza si la anotación confirma la recepción del producto o hace referencia a una posible reclamación.

### 5. OK ✅
El documento es válido si contiene alguno de estos elementos:
- **Firma y nombre del cliente** (mano alzada) en zonas 6, 7 u 8
- **Sello del cliente** (válido)
  - ⚠️ NO son válidos: Sello de Deacero o Ingetek

## Estructura del Proyecto

```
Pods_DAS/
├── documentos/              # Carpeta para los PODs a procesar
│   ├── entrada/            # PODs sin procesar
│   ├── procesados/         # PODs ya clasificados
│   └── ejemplos/           # Documentos de ejemplo
├── src/                    # Código fuente
│   ├── main.py            # Aplicación principal
│   ├── processor.py       # Procesador de documentos
│   ├── classifier.py      # Clasificador de PODs
│   ├── detectors/         # Detectores especializados
│   │   ├── signature_detector.py
│   │   ├── stamp_detector.py
│   │   ├── legibility_analyzer.py
│   │   └── annotation_detector.py
│   └── utils.py           # Utilidades
├── resultados/            # Reportes y resultados
├── config/                # Configuraciones
│   └── settings.yaml
├── requirements.txt       # Dependencias
└── README.md             # Este archivo
```

## Instalación

### Requisitos Previos
- Python 3.8 o superior
- Tesseract OCR instalado en el sistema

### Windows
```bash
# Instalar Tesseract OCR
# Descargar desde: https://github.com/UB-Mannheim/tesseract/wiki

# Instalar dependencias de Python
pip install -r requirements.txt
```

### Linux/Mac
```bash
# Instalar Tesseract OCR
sudo apt-get install tesseract-ocr  # Ubuntu/Debian
# brew install tesseract              # Mac

# Instalar dependencias de Python
pip install -r requirements.txt
```

## Uso

### 🌐 Interfaz Web (Recomendado - Más Moderna)

**Windows:**
```bash
run_web.bat
```

**Linux/Mac:**
```bash
chmod +x run_web.sh
./run_web.sh
```

Se abrirá en tu navegador en: `http://localhost:8501`

**Características:**
- ✅ Dashboard interactivo con métricas en tiempo real
- ✅ Gráficos visuales (torta, barras)
- ✅ Tabla con filtros avanzados
- ✅ Vista detallada con pestañas
- ✅ Exportación a CSV
- ✅ Responsive (funciona en cualquier dispositivo)

### 🖥️ Interfaz Gráfica de Escritorio

**Windows:**
```bash
run_gui.bat
```

**Linux/Mac:**
```bash
chmod +x run_gui.sh
./run_gui.sh
```

O directamente:
```bash
venv\Scripts\activate    # Windows
source venv/bin/activate # Linux/Mac
python src/gui.py
```

**Características:**
- ✅ Aplicación nativa de escritorio
- ✅ Estadísticas en tiempo real
- ✅ Tabla interactiva
- ✅ Log de procesamiento integrado
- ✅ Sin necesidad de navegador

### 💻 Modo Línea de Comandos

#### Modo Básico
```bash
python src/main.py --input documentos/entrada --output resultados
```

#### Procesar un solo documento
```bash
python src/main.py --file ruta/al/documento.pdf
```

#### Modo interactivo con visualización
```bash
python src/main.py --interactive
```

## Configuración

Edita `config/settings.yaml` para ajustar:
- Umbrales de detección
- Zonas de interés para firmas
- Palabras clave para anotaciones
- Sellos válidos/inválidos

## Tecnologías Utilizadas

- **OpenCV**: Procesamiento de imágenes
- **Tesseract OCR**: Reconocimiento de texto
- **pdf2image**: Conversión de PDFs
- **Pillow**: Manipulación de imágenes
- **NumPy**: Operaciones numéricas
- **PyYAML**: Configuración

## Resultados

El sistema genera:
- Clasificación automática de cada POD
- Reporte en Excel/CSV con detalles
- Imágenes anotadas mostrando áreas detectadas
- Log detallado del procesamiento

## Próximas Mejoras

- [ ] Integración con IA para mejorar detección
- [ ] API REST para integración con otros sistemas
- [ ] Dashboard web para visualización
- [ ] Entrenamiento de modelos custom

## Contacto

Para soporte o consultas sobre el proyecto.

