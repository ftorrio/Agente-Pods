# -*- coding: utf-8 -*-
"""
Interfaz Web para el Sistema de Validación de PODs
Usando Streamlit para una experiencia moderna e interactiva
"""

import streamlit as st
import pandas as pd
import os
import sys
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64

# Agregar el directorio src al path
sys.path.insert(0, os.path.dirname(__file__))

from main import PODValidationSystem
from utils import load_config, get_files_from_directory
from cloud_storage import CloudStorageReader, KNOWN_PODS_IES161108I36

# Importar datos de demo
try:
    from demo_data import get_demo_results, get_demo_statistics
    DEMO_AVAILABLE = True
except ImportError:
    DEMO_AVAILABLE = False


# Configuración de la página
st.set_page_config(
    page_title="Sistema de Validación de PODs",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .valid-pod {
        background-color: #d4edda;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
    .invalid-pod {
        background-color: #f8d7da;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #dc3545;
    }
    .warning-pod {
        background-color: #fff3cd;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
    }
    h1 {
        color: #1e3a8a;
    }
    h2 {
        color: #2563eb;
    }
    </style>
""", unsafe_allow_html=True)


def init_session_state():
    """
    Inicializa el estado de la sesión
    """
    if 'results' not in st.session_state:
        st.session_state.results = []
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'system' not in st.session_state:
        st.session_state.system = None
    if 'cloud_filenames' not in st.session_state:
        st.session_state.cloud_filenames = []
    if 'cloud_folder' not in st.session_state:
        st.session_state.cloud_folder = 'IES161108I36'
    if 'alerts' not in st.session_state:
        st.session_state.alerts = []


def get_config():
    """
    Carga la configuración
    """
    return load_config()


def create_metrics_dashboard(results):
    """
    Crea el dashboard de métricas
    """
    if not results:
        st.info("📊 No hay resultados para mostrar. Procesa algunos PODs para ver las estadísticas.")
        return
    
    # Calcular métricas
    total = len(results)
    valid = sum(1 for r in results if r['is_valid'])
    invalid = total - valid
    percentage = (valid / total * 100) if total > 0 else 0
    
    # Contar por clasificación
    ok_count = sum(1 for r in results if r['classification_code'] == 'OK')
    annotations_count = sum(1 for r in results if r['classification_code'] == 'CON_ANOTACIONES')
    no_ack_count = sum(1 for r in results if r['classification_code'] == 'SIN_ACUSE')
    illegible_count = sum(1 for r in results if r['classification_code'] == 'POCO_LEGIBLE')
    incorrect_count = sum(1 for r in results if r['classification_code'] == 'INCORRECTO')
    
    # Primera fila de métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Total PODs",
            value=total,
            help="Número total de documentos procesados"
        )
    
    with col2:
        st.metric(
            label="✅ Válidos",
            value=valid,
            delta=f"{percentage:.1f}%",
            delta_color="normal",
            help="Documentos que pasaron la validación"
        )
    
    with col3:
        st.metric(
            label="❌ Con Defectos",
            value=invalid,
            delta=f"{100-percentage:.1f}%",
            delta_color="inverse",
            help="Documentos con problemas"
        )
    
    with col4:
        st.metric(
            label="📈 Tasa de Validación",
            value=f"{percentage:.1f}%",
            help="Porcentaje de documentos válidos"
        )
    
    st.divider()
    
    # Segunda fila de métricas - Distribución por clasificación
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("✅ OK", ok_count)
    
    with col2:
        st.metric("📝 Con Anotaciones", annotations_count)
    
    with col3:
        st.metric("⚠️ Sin Acuse", no_ack_count)
    
    with col4:
        st.metric("❌ Poco Legible", illegible_count)
    
    with col5:
        st.metric("❌ Incorrecto", incorrect_count)


def create_charts(results):
    """
    Crea gráficos visuales
    """
    if not results:
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de distribución por clasificación
        classification_counts = {}
        for r in results:
            code = r['classification_code']
            classification_counts[code] = classification_counts.get(code, 0) + 1
        
        fig = px.pie(
            values=list(classification_counts.values()),
            names=list(classification_counts.keys()),
            title="Distribución por Clasificación",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Gráfico de válidos vs inválidos
        valid_count = sum(1 for r in results if r['is_valid'])
        invalid_count = len(results) - valid_count
        
        fig = go.Figure(data=[
            go.Bar(
                x=['Válidos', 'Con Defectos'],
                y=[valid_count, invalid_count],
                marker_color=['#28a745', '#dc3545'],
                text=[valid_count, invalid_count],
                textposition='auto'
            )
        ])
        fig.update_layout(
            title="Estado de Validación",
            yaxis_title="Cantidad de PODs",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)


def create_results_table(results):
    """
    Crea la tabla de resultados
    """
    if not results:
        st.info("📋 No hay resultados para mostrar.")
        return
    
    # Preparar datos para la tabla
    table_data = []
    for r in results:
        filename = os.path.basename(r['source_file'])
        table_data.append({
            'Archivo': filename,
            'Clasificación': r['classification'],
            'Estado': '✓ Válido' if r['is_valid'] else '✗ Defecto',
            'Confianza': f"{r['confidence']:.0%}",
            'Firmas': len(r['details'].get('signatures', [])),
            'Sellos': len(r['details'].get('stamps', [])),
            'Anotaciones': 'Sí' if r['details']['annotations']['has_annotations'] else 'No',
            'Sentimiento': r['details']['annotations'].get('sentiment', 'N/A'),
        })
    
    df = pd.DataFrame(table_data)
    
    # Mostrar tabla con filtros
    st.subheader("📋 Tabla de Resultados Detallados")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_classification = st.multiselect(
            "Filtrar por Clasificación:",
            options=df['Clasificación'].unique(),
            default=df['Clasificación'].unique()
        )
    
    with col2:
        filter_state = st.multiselect(
            "Filtrar por Estado:",
            options=df['Estado'].unique(),
            default=df['Estado'].unique()
        )
    
    with col3:
        search_term = st.text_input("🔍 Buscar archivo:", "")
    
    # Aplicar filtros
    filtered_df = df[
        (df['Clasificación'].isin(filter_classification)) &
        (df['Estado'].isin(filter_state))
    ]
    
    if search_term:
        filtered_df = filtered_df[filtered_df['Archivo'].str.contains(search_term, case=False)]
    
    # Mostrar tabla
    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=400,
        hide_index=True
    )
    
    # Botón para descargar CSV
    csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Descargar tabla como CSV",
        data=csv,
        file_name=f"resultados_pods_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
    )


def show_pod_details(result):
    """
    Muestra detalles de un POD específico
    """
    filename = os.path.basename(result['source_file'])
    
    # Encabezado con color según validez
    if result['is_valid']:
        st.markdown(f"<div class='valid-pod'><h3>📄 {filename}</h3></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='invalid-pod'><h3>📄 {filename}</h3></div>", unsafe_allow_html=True)
    
    # Información general
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Clasificación", result['classification'])
    
    with col2:
        state = "✓ Válido" if result['is_valid'] else "✗ Con Defectos"
        st.metric("Estado", state)
    
    with col3:
        st.metric("Confianza", f"{result['confidence']:.1%}")
    
    # Detalles en tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["✍️ Firmas", "🔖 Sellos", "📝 Anotaciones", "📖 Legibilidad", "⚠️ Problemas"])
    
    with tab1:
        signatures = result['details'].get('signatures', [])
        if signatures:
            st.write(f"**Detectadas {len(signatures)} firma(s):**")
            for i, sig in enumerate(signatures, 1):
                st.write(f"- **Firma {i}:** Región `{sig['region']}`, Confianza: `{sig['confidence']:.2f}`")
        else:
            st.info("No se detectaron firmas")
    
    with tab2:
        stamps = result['details'].get('stamps', [])
        if stamps:
            st.write(f"**Detectados {len(stamps)} sello(s):**")
            for i, stamp in enumerate(stamps, 1):
                valid = "✓ Válido" if stamp['is_valid'] else "✗ Inválido"
                st.write(f"- **Sello {i}:** Tipo `{stamp['type']}`, Estado: `{valid}`")
        else:
            st.info("No se detectaron sellos")
    
    with tab3:
        annotations = result['details'].get('annotations', {})
        if annotations.get('has_annotations'):
            st.write(f"**Cantidad:** {annotations['annotation_count']}")
            st.write(f"**Sentimiento:** {annotations['sentiment']}")
            if annotations.get('text_content'):
                st.write("**Texto extraído:**")
                for text in annotations['text_content']:
                    st.write(f"- {text}")
        else:
            st.info("No se detectaron anotaciones")
    
    with tab4:
        legibility = result['details'].get('legibility', {})
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Calidad del Texto", f"{legibility.get('text_quality', 0):.2f}")
            st.metric("Confianza OCR", f"{legibility.get('ocr_confidence', 0):.1f}")
        with col2:
            st.write("**Campos detectados:**")
            fields = legibility.get('fields_detected', [])
            if fields:
                st.write(", ".join(fields))
            else:
                st.write("Ninguno")
            
            st.write("**Campos faltantes:**")
            missing = legibility.get('fields_missing', [])
            if missing:
                st.write(", ".join(missing))
            else:
                st.write("Ninguno")
    
    with tab5:
        issues = result.get('issues', [])
        recommendations = result.get('recommendations', [])
        
        if issues:
            st.write("**Problemas detectados:**")
            for issue in issues:
                st.warning(f"⚠️ {issue}")
        else:
            st.success("✅ No se detectaron problemas")
        
        if recommendations:
            st.write("**Recomendaciones:**")
            for rec in recommendations:
                st.info(f"💡 {rec}")
    
    # Mostrar imagen anotada si existe
    if result.get('annotated_image_path') and os.path.exists(result['annotated_image_path']):
        st.divider()
        st.subheader("🖼️ Imagen Anotada")
        st.image(result['annotated_image_path'], use_column_width=True)


def main():
    """
    Función principal de la aplicación web
    """
    # Inicializar estado
    init_session_state()
    
    # Encabezado
    st.title("🔍 Sistema de Validación de PODs")
    st.markdown("**Proof of Delivery** - Análisis Automático de Documentos")
    
    # Botón de Demo (si está disponible y no hay resultados)
    if DEMO_AVAILABLE and not st.session_state.results:
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("🎬 Ver Demo Interactiva", type="primary", use_container_width=True):
                st.session_state.results = get_demo_results()
                st.success("✅ Demo cargada con 5 PODs de ejemplo")
                st.rerun()
    
    # Panel de Alertas (si hay)
    if st.session_state.alerts:
        with st.expander(f"🔔 ALERTAS ACTIVAS ({len(st.session_state.alerts)})", expanded=True):
            for alert in st.session_state.alerts[-5:]:  # Últimas 5
                if alert['priority'] == 'HIGH':
                    st.error(f"{alert['type']} **{alert['title']}**\n\n{alert['message']}")
                elif alert['priority'] == 'MEDIUM':
                    st.warning(f"{alert['type']} **{alert['title']}**\n\n{alert['message']}")
                else:
                    st.info(f"{alert['type']} **{alert['title']}**\n\n{alert['message']}")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Control")
        
        # Cargar configuración
        config = get_config()
        
        # Selector de fuente de datos
        st.subheader("📂 Fuente de Datos")
        data_source = st.radio(
            "Selecciona la fuente:",
            ["💻 Archivos Locales", "☁️ Google Cloud Storage"],
            index=0,
            key="data_source_selector",
            help="Elige de dónde cargar los PODs"
        )
        
        files = []
        
        if data_source == "💻 Archivos Locales":
            # Selector de directorio local
            default_dir = config['paths']['input_dir'] if config else "documentos/entrada"
            input_dir = st.text_input(
                "📁 Directorio de PODs:",
                value=default_dir,
                help="Ruta al directorio con los documentos POD"
            )
            
            # Verificar si hay archivos
            if os.path.exists(input_dir):
                files = get_files_from_directory(input_dir, config['supported_formats'])
                st.info(f"📊 {len(files)} archivo(s) encontrado(s)")
            else:
                st.error("❌ El directorio no existe")
        
        else:  # Google Cloud Storage
            st.text_input(
                "🌐 URL Base:",
                value="https://storage.cloud.google.com/dea-documents-das/pod",
                disabled=True,
                help="URL base del bucket"
            )
            
            folder = st.text_input(
                "📁 Carpeta/Prefijo:",
                value="IES161108I36",
                help="Nombre de la carpeta en el bucket (ej: IES161108I36)"
            )
            
            # Límite por defecto
            max_files = 10
            
            # Verificar si hay credenciales (local o Streamlit Cloud)
            credentials_path = os.path.join('config', 'credentials.json')
            has_credentials = os.path.exists(credentials_path)
            
            # Verificar también si hay secretos en Streamlit Cloud
            streamlit_secrets_available = False
            try:
                if hasattr(st, 'secrets') and 'gcp_service_account' in st.secrets:
                    streamlit_secrets_available = True
                    has_credentials = True
            except:
                pass
            
            if has_credentials:
                st.success("✅ Credenciales encontradas - Listado automático habilitado")
                
                # Filtro por fechas
                st.markdown("**📅 Filtrar por Fecha de Creación:**")
                
                col_date1, col_date2 = st.columns(2)
                
                with col_date1:
                    from datetime import datetime, timedelta
                    # Por defecto: SOLO HOY
                    default_start = datetime.now()
                    start_date = st.date_input(
                        "Desde:",
                        value=default_start,
                        help="Fecha inicial - RECOMENDADO: seleccionar UN SOLO DÍA"
                    )
                
                with col_date2:
                    # Por defecto: SOLO HOY
                    end_date = st.date_input(
                        "Hasta:",
                        value=datetime.now(),
                        help="Fecha final - RECOMENDADO: mismo día que 'Desde'"
                    )
                
                # Advertencia si el rango es mayor a 1 día
                days_diff = (end_date - start_date).days
                if days_diff > 7:
                    st.error(f"⚠️ ADVERTENCIA: Rango de {days_diff} días puede tener CIENTOS de PODs")
                    st.warning("💡 RECOMENDACIÓN: Selecciona UN SOLO DÍA para evitar descargas masivas")
                elif days_diff > 1:
                    st.warning(f"⚠️ Rango de {days_diff} días - Verifica el límite de archivos")
                
                # Límite de archivos a procesar - MÁS RESTRICTIVO
                max_files = st.number_input(
                    "🔢 Límite máximo de archivos:",
                    min_value=1,
                    max_value=100,
                    value=10,
                    step=5,
                    help="⚠️ IMPORTANTE: Empezar con 10-20 archivos. Puedes aumentar después"
                )
                
                st.info(f"📊 Se procesarán máximo {max_files} PODs del {start_date} al {end_date}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("🔄 Listar PODs por Fecha"):
                        with st.spinner("Listando archivos en la nube..."):
                            from cloud_auth import AuthenticatedCloudReader
                            
                            # Usar credenciales de Streamlit secrets o archivo local
                            if hasattr(st, 'secrets') and 'gcp_service_account' in st.secrets:
                                creds_dict = dict(st.secrets['gcp_service_account'])
                                reader = AuthenticatedCloudReader(credentials_dict=creds_dict)
                            else:
                                reader = AuthenticatedCloudReader(credentials_path)
                            
                            # Convertir fechas a string
                            start_str = start_date.strftime('%Y-%m-%d')
                            end_str = end_date.strftime('%Y-%m-%d')
                            
                            bucket_files = reader.list_blobs_in_folder(
                                'dea-documents-das',
                                f'pod/{folder}/',
                                start_date=start_str,
                                end_date=end_str
                            )
                            if bucket_files:
                                # Limitar al número especificado
                                total_found = len(bucket_files)
                                bucket_files = bucket_files[:max_files]
                                st.session_state.cloud_filenames = bucket_files
                                
                                if total_found > max_files:
                                    st.warning(f"⚠️ Se encontraron {total_found} archivos, mostrando solo los primeros {max_files}")
                                else:
                                    st.success(f"✅ Encontrados {len(bucket_files)} archivos del {start_str} al {end_str}")
                            else:
                                st.warning(f"No se encontraron archivos entre {start_str} y {end_str}")
                
                with col2:
                    if st.button("🗑️ Limpiar Lista"):
                        st.session_state.cloud_filenames = []
                        st.rerun()
                
                # Mostrar advertencia si hay demasiados archivos
                if 'cloud_filenames' in st.session_state and len(st.session_state.cloud_filenames) > max_files:
                    st.error(f"⚠️ PELIGRO: Lista tiene {len(st.session_state.cloud_filenames)} archivos")
                    st.error(f"⚠️ Se procesarán SOLO los primeros {max_files}")
                    st.warning("💡 Haz clic en 'Limpiar Lista' y vuelve a listar con límite menor")
                
                # Mostrar lista editable
                if 'cloud_filenames' in st.session_state and st.session_state.cloud_filenames:
                    filenames_text = "\n".join(st.session_state.cloud_filenames)
                else:
                    filenames_text = "QC8261_1024008261.jpg\nQM2015_1033002015.jpg\nQP7957_1036007957.jpg\nQP7960_1036007960.jpg\nQP7959_1036007959.jpg"
                
                file_list = st.text_area(
                    "📋 Archivos a procesar:",
                    value=filenames_text,
                    height=200,
                    help="Lista de archivos. Puedes editar, agregar o quitar archivos"
                )
            else:
                st.warning("⚠️ Sin credenciales - Modo manual")
                st.info("💡 Coloca credentials.json en config/ para listado automático")
                
                file_list = st.text_area(
                    "📋 Lista de archivos (manual):",
                    value="\n".join([
                        "QC8261_1024008261.jpg",
                        "QM2015_1033002015.jpg",
                        "QP7957_1036007957.jpg",
                        "QP7960_1036007960.jpg",
                        "QP7959_1036007959.jpg"
                    ]),
                    height=150,
                    help="Ingresa los nombres manualmente, uno por línea"
                )
            
            if file_list.strip():
                filenames = [f.strip() for f in file_list.split('\n') if f.strip()]
                
                # APLICAR LÍMITE ESTRICTO
                if len(filenames) > max_files:
                    st.error(f"🛑 LISTA TIENE {len(filenames)} ARCHIVOS - SE USARÁN SOLO {max_files}")
                    filenames = filenames[:max_files]
                
                st.success(f"✅ {len(filenames)} archivo(s) en la lista (se descargarán al procesar)")
                
                # Guardar en session_state
                st.session_state.cloud_folder = folder
                st.session_state.cloud_filenames = filenames
                
                # Indicador de que hay archivos cloud
                files = filenames
            else:
                st.warning("⚠️ Agrega nombres de archivos para procesar")
                files = []
        
        st.divider()
        
        # Botón de procesamiento
        if st.button("▶️ Procesar PODs", type="primary", disabled=len(files) == 0):
            # Limpiar resultados anteriores automáticamente
            st.session_state.results = []
            st.session_state.processing = True
            
            # Crear sistema
            st.session_state.system = PODValidationSystem()
            
            # Barra de progreso
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Determinar lista de archivos a procesar
            files_to_process = []
            
            if data_source == "☁️ Google Cloud Storage":
                # Descargar archivos desde la nube
                status_text.text("☁️ Descargando PODs desde Google Cloud Storage...")
                
                # Verificar si hay credenciales
                credentials_path = os.path.join('config', 'credentials.json')
                
                # OBTENER LISTA DE ARCHIVOS DE SESSION_STATE
                filenames = st.session_state.get('cloud_filenames', [])
                folder = st.session_state.get('cloud_folder', 'IES161108I36')
                
                # ⚠️ APLICAR LÍMITE MÁXIMO DE SEGURIDAD (50 archivos)
                LIMITE_SEGURIDAD = 50
                if len(filenames) > LIMITE_SEGURIDAD:
                    status_text.text(f"⚠️ LÍMITE DE SEGURIDAD: {LIMITE_SEGURIDAD} archivos máximo")
                    st.error(f"🛑 Se encontraron {len(filenames)} archivos - PROCESANDO SOLO {LIMITE_SEGURIDAD}")
                    filenames = filenames[:LIMITE_SEGURIDAD]
                
                # Crear cliente autenticado
                if hasattr(st, 'secrets') and 'gcp_service_account' in st.secrets:
                    # Usar secretos de Streamlit Cloud
                    from cloud_auth import AuthenticatedCloudReader
                    creds_dict = dict(st.secrets['gcp_service_account'])
                    cloud_reader = AuthenticatedCloudReader(credentials_dict=creds_dict)
                elif os.path.exists(credentials_path):
                    # Usar archivo local
                    from cloud_auth import AuthenticatedCloudReader
                    cloud_reader = AuthenticatedCloudReader(credentials_path)
                else:
                    cloud_reader = CloudStorageReader()
                
                # Crear directorio temporal
                import tempfile
                temp_dir = tempfile.mkdtemp(prefix="pods_web_")
                
                failed_downloads = []
                
                for idx, filename in enumerate(filenames, 1):
                    progress_bar.progress((idx - 0.5) / len(filenames) / 2)  # 0-50% para descarga
                    status_text.text(f"📥 Descargando {idx}/{len(filenames)}: {filename}")
                    
                    # Usar método según tipo de reader
                    if hasattr(cloud_reader, 'download_file_from_cloud'):
                        if isinstance(cloud_reader, CloudStorageReader):
                            local_path = cloud_reader.download_file_from_cloud(folder, filename)
                        else:  # AuthenticatedCloudReader
                            local_path = cloud_reader.download_file_from_cloud(folder, filename, temp_dir)
                    else:
                        local_path = None
                    
                    if local_path:
                        files_to_process.append(local_path)
                    else:
                        failed_downloads.append(filename)
                        st.warning(f"⚠️ No se pudo descargar: {filename}")
                
                # Mostrar resumen de descarga
                if failed_downloads:
                    st.error(f"❌ {len(failed_downloads)} archivos NO descargados de {len(filenames)}")
                    with st.expander("🔍 Ver archivos que fallaron"):
                        for failed_file in failed_downloads:
                            st.text(f"  • {failed_file}")
                
                if files_to_process:
                    st.success(f"✅ Descargados exitosamente: {len(files_to_process)}/{len(filenames)} archivos")
                else:
                    st.error("❌ No se pudo descargar ningún archivo")
            else:
                # Usar archivos locales
                files_to_process = files
            
            # Procesar archivos
            for idx, file_path in enumerate(files_to_process, 1):
                if data_source == "☁️ Google Cloud Storage":
                    progress_bar.progress(0.5 + (idx / len(files_to_process) / 2))  # 50-100%
                else:
                    progress_bar.progress(idx / len(files_to_process))
                
                status_text.text(f"⚙️ Procesando {idx}/{len(files_to_process)}: {os.path.basename(file_path)}")
                
                try:
                    result = st.session_state.system.process_single_file(file_path, save_annotated=True)
                    if result:
                        st.session_state.results.append(result)
                        
                        # Generar alertas si hay sistema de notificaciones
                        if hasattr(st.session_state.system.classifier, 'notification_system') and st.session_state.system.classifier.notification_system:
                            alerts = st.session_state.system.classifier.notification_system.check_and_alert(result)
                            if alerts:
                                st.session_state.alerts.extend(alerts)
                except Exception as e:
                    st.error(f"❌ Error procesando {os.path.basename(file_path)}: {str(e)}")
            
            progress_bar.progress(1.0)
            status_text.text("✅ Procesamiento completado")
            st.session_state.processing = False
            
            # Guardar alertas si hay
            if st.session_state.alerts:
                try:
                    import json
                    os.makedirs('resultados', exist_ok=True)
                    with open('resultados/alertas.json', 'w', encoding='utf-8') as f:
                        json.dump(st.session_state.alerts, f, indent=2, ensure_ascii=False, default=str)
                except Exception as e:
                    st.warning(f"No se pudieron guardar alertas: {e}")
            
            st.success(f"🎉 Se procesaron {len(st.session_state.results)} documento(s)")
            
            # Mostrar resumen de alertas
            if st.session_state.alerts:
                urgentes = sum(1 for a in st.session_state.alerts if a.get('priority') == 'HIGH')
                if urgentes > 0:
                    st.error(f"🔴 {urgentes} alerta(s) URGENTE(S) generada(s)")
            
            st.rerun()
        
        # Botón para limpiar resultados
        if st.button("🗑️ Limpiar Resultados"):
            st.session_state.results = []
            st.rerun()
        
        st.divider()
        
        # Enlaces rápidos
        st.subheader("🔗 Accesos Rápidos")
        
        if st.button("📊 Abrir Reportes"):
            reports_dir = os.path.join(config['paths']['output_dir'], 'reportes')
            if os.path.exists(reports_dir):
                # Solo funciona en Windows local
                if os.name == 'nt':
                    os.startfile(reports_dir)
                    st.success(f"📂 Carpeta abierta: {reports_dir}")
                else:
                    st.info(f"📂 Reportes ubicados en: {reports_dir}")
            else:
                st.warning("No hay reportes generados aún")
        
        if st.button("🖼️ Ver Imágenes"):
            images_dir = os.path.join(config['paths']['output_dir'], 'imagenes_anotadas')
            if os.path.exists(images_dir):
                # Solo funciona en Windows local
                if os.name == 'nt':
                    os.startfile(images_dir)
                    st.success(f"📂 Carpeta abierta: {images_dir}")
                else:
                    st.info(f"📂 Imágenes ubicadas en: {images_dir}")
            else:
                st.warning("No hay imágenes anotadas aún")
        
        st.divider()
        
        # Información
        st.markdown("### ℹ️ Información")
        st.markdown("""
        **Clasificaciones:**
        - ✅ OK: Válido
        - 📝 Con Anotaciones
        - ⚠️ Sin Acuse
        - ❌ Poco Legible
        - ❌ Incorrecto
        """)
    
    # Contenido principal
    if st.session_state.results:
        # Dashboard de métricas
        st.header("📊 Dashboard de Métricas")
        create_metrics_dashboard(st.session_state.results)
        
        st.divider()
        
        # Gráficos
        st.header("📈 Visualizaciones")
        create_charts(st.session_state.results)
        
        st.divider()
        
        # Tabla de resultados
        create_results_table(st.session_state.results)
        
        st.divider()
        
        # Vista de detalles individuales
        st.header("🔍 Vista Detallada")
        
        # Selector de POD
        pod_names = [os.path.basename(r['source_file']) for r in st.session_state.results]
        selected_pod = st.selectbox(
            "Selecciona un POD para ver detalles:",
            options=pod_names
        )
        
        if selected_pod:
            result = next(r for r in st.session_state.results if os.path.basename(r['source_file']) == selected_pod)
            show_pod_details(result)
    
    else:
        # Mensaje inicial
        st.info("""
        👋 **Bienvenido al Sistema de Validación de PODs**
        
        Para comenzar:
        1. Coloca tus archivos POD en la carpeta `documentos/entrada/`
        2. Verifica el directorio en el panel lateral
        3. Haz clic en **▶️ Procesar PODs**
        4. Revisa los resultados y estadísticas
        
        **Formatos soportados:** PDF, GIF, PNG, JPG, TIFF, BMP
        """)
        
        # Mostrar ejemplo visual
        st.markdown("### 📋 ¿Qué verás después de procesar?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Dashboard de Métricas:**
            - Total de PODs procesados
            - Cantidad de válidos e inválidos
            - Tasa de validación
            - Distribución por clasificación
            """)
        
        with col2:
            st.markdown("""
            **Tabla Interactiva:**
            - Lista completa de PODs
            - Filtros por clasificación y estado
            - Búsqueda por nombre
            - Descarga como CSV
            """)


if __name__ == "__main__":
    main()

