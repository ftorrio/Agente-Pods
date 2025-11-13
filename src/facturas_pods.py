# -*- coding: utf-8 -*-
"""
Página de Facturas con PODs
Muestra facturas de BigQuery con links a sus PODs en Google Cloud Storage
"""

import streamlit as st
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import os
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Facturas con PODs - Ingetek",
    page_icon="📄",
    layout="wide"
)

# Logo de Ingetek
logo_path = "assets/logo-ingetek.png"
if os.path.exists(logo_path):
    import base64
    with open(logo_path, "rb") as img_file:
        img_data = base64.b64encode(img_file.read()).decode()
    st.markdown(f"""
        <div style="padding: 10px 0px;">
            <a href="https://www.ingetek.com" target="_blank">
                <img src="data:image/png;base64,{img_data}" width="150">
            </a>
        </div>
    """, unsafe_allow_html=True)

st.title("📄 Facturas con PODs")
st.markdown("**Consulta de facturas con acceso directo a documentos POD**")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # Filtros
    st.subheader("📅 Filtros")
    
    col1, col2 = st.columns(2)
    with col1:
        fecha_desde = st.date_input("Desde:", value=pd.Timestamp.now() - pd.Timedelta(days=30))
    with col2:
        fecha_hasta = st.date_input("Hasta:", value=pd.Timestamp.now())
    
    cliente_filter = st.text_input("🏢 Filtrar por Cliente:", "")
    proyecto_filter = st.text_input("📋 Filtrar por Proyecto:", "")
    
    limite = st.number_input("🔢 Límite de registros:", min_value=10, max_value=10000, value=100, step=50)
    
    consultar = st.button("🔍 Consultar Facturas", type="primary")


def get_bigquery_client():
    """Obtiene cliente de BigQuery autenticado"""
    try:
        # Obtener directorio base del proyecto
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Verificar rutas posibles (config y credential)
        credentials_paths = [
            os.path.join(base_dir, 'config', 'credentials.json'),
            os.path.join(base_dir, 'credential', 'deasol-prj-sandbox-99ab62bedd16 (1).json'),
            'config/credentials.json',
            'credential/deasol-prj-sandbox-99ab62bedd16 (1).json'
        ]
        
        credentials_file = None
        for path in credentials_paths:
            if os.path.exists(path):
                credentials_file = path
                st.sidebar.info(f"📁 Usando: {os.path.basename(path)}")
                break
        
        # Intentar desde secretos de Streamlit Cloud
        if hasattr(st, 'secrets') and 'gcp_service_account' in st.secrets:
            credentials = service_account.Credentials.from_service_account_info(
                dict(st.secrets['gcp_service_account'])
            )
            client = bigquery.Client(credentials=credentials, project=st.secrets['gcp_service_account']['project_id'])
            st.sidebar.success("✅ Conectado a BigQuery (Streamlit Secrets)")
            return client
        # Intentar desde archivo local
        elif credentials_file:
            credentials = service_account.Credentials.from_service_account_file(credentials_file)
            # Usar proyecto del archivo de credenciales
            import json
            with open(credentials_file, 'r') as f:
                creds_data = json.load(f)
                project_id = creds_data.get('project_id', 'deasol-prj-sandbox')  # Usar sandbox por defecto
            
            client = bigquery.Client(credentials=credentials, project=project_id)
            st.sidebar.success(f"✅ Conectado a BigQuery (archivo local)")
            return client
        else:
            st.sidebar.error("❌ No se encontraron credenciales de BigQuery")
            st.sidebar.info(f"Buscado en: {credentials_paths}")
            return None
    except Exception as e:
        st.sidebar.error(f"❌ Error conectando a BigQuery: {e}")
        st.sidebar.exception(e)
        return None


def generar_url_pod(nombre_archivo):
    """
    Genera URL del POD en Google Cloud Storage
    
    Lógica: 
    1. Tomar NombreArchivoPOD (ej: "QC8261_1024008261.jpg" o "QB14620_1023014620.jpg")
    2. Extraer caracteres ANTES del primer _ (ej: "QC8261" o "QB14620")
    3. Buscar archivo en GCS que empiece con ese patrón
    4. Construir URL: https://storage.cloud.google.com/dea-documents-das/pod/IES161108I36/QC8261_1024008261.jpg
    
    Ejemplo:
    NombreArchivoPOD: "QC8261_1024008261.jpg"
    Prefijo antes de _: "QC8261"
    URL: https://storage.cloud.google.com/dea-documents-das/pod/IES161108I36/QC8261_1024008261.jpg
    """
    if not nombre_archivo or pd.isna(nombre_archivo):
        return None
    
    try:
        # Limpiar nombre
        nombre = str(nombre_archivo).strip()
        
        # Extraer prefijo antes del primer _ (ej: "QC8261" de "QC8261_1024008261.jpg")
        if '_' in nombre:
            prefijo = nombre.split('_')[0]  # "QC8261"
            # El nombre completo ya lo tienes, usarlo directamente
            nombre_archivo_completo = nombre
        else:
            # Si no tiene _, usar el nombre tal cual
            prefijo = nombre
            nombre_archivo_completo = nombre
        
        # Construir URL completa
        base_url = "https://storage.cloud.google.com/dea-documents-das/pod/IES161108I36"
        url_completa = f"{base_url}/{nombre_archivo_completo}"
        
        return url_completa
        
    except Exception as e:
        return None


def ejecutar_query_facturas(fecha_desde, fecha_hasta, cliente='', proyecto='', limite=100):
    """
    Ejecuta la query de facturas con PODs
    Usando tabla del proyecto deasol-prj-sandbox
    """
    
    # Query simplificada - campos específicos solicitados
    query = f"""
    SELECT
        ROW_NUMBER() OVER (ORDER BY fechaFactura DESC) AS consecutivo,
        ClaProyecto,
        NomProyecto,
        NombreArchivoPOD,
        fechaFactura,
        Remision,
        kilos_reales,
        KilosDeRemision,
        nombreRazonSocial,
        idfacturaAlfanumerico,
        -- Campos adicionales útiles
        impFactura,
        valorEstatus
    FROM `deasol-prj-sandbox.status_03_gold_layer_comercial.Factura_Remision`
    WHERE CAST(fechaFactura AS DATE) BETWEEN '{fecha_desde}' AND '{fecha_hasta}'
        {'AND nombreRazonSocial LIKE "%' + cliente + '%"' if cliente else ''}
        {'AND NomProyecto LIKE "%' + proyecto + '%"' if proyecto else ''}
    ORDER BY fechaFactura DESC
    LIMIT {limite}
    """
    
    return query


def ejecutar_query_facturas_original(fecha_desde, fecha_hasta, cliente='', proyecto='', limite=100):
    """
    Query original completa (para cuando tengas acceso a dfor-prj-prod)
    """
    
    # Query completa original
    query = f"""
    WITH
    -- CTE 1: Datos de Fabricación Detalle
    ITK002FabricacionDet AS (
        SELECT 
            a.idFabricacion, a.claCliente, a.ClaProyecto, a.ClaUbicacion, 
            b.CantidadPedida, b.CantidadPedida*d.PesoTeoricoKgs AS KgsPedidosFabricacion, 
            b.CantidadSurtida, b.CantidadSurtida*d.PesoTeoricoKgs AS KgsSurtidosFabricacion, 
            CAST(a.FechaCaptura AS TIMESTAMP) AS FechaCaptura, 
            CAST(a.fechaBaseFabricacion AS TIMESTAMP) AS fechaBaseFabricacion, 
            CAST(a.FechaPromesaOriginal AS TIMESTAMP) AS FechaPromesaOriginal, 
            CAST(a.FechaPromesaActual AS TIMESTAMP) AS FechaPromesaActual, 
            CAST(a.FechaNecesitaCliente AS TIMESTAMP) AS FechaNecesitaCliente, 
            a.ClaPedidoCliente, 
            CAST(a.FechaPedidoCliente AS TIMESTAMP) AS FechaPedidoCliente, 
            b.ClaArticulo, b.NumeroRenglon, b.PrecioLista, a.claConsignado, b.ClaListaPrecio, b.PrecioEntrega, 
            b.ClaEstatusFabricacion,
            CASE 
                WHEN b.claEstatusFabricacion = 3 THEN 'Cancelada' 
                WHEN b.claEstatusFabricacion = 6 THEN 'Surtido Total' 
                WHEN b.claEstatusFabricacion = 4 THEN 'Pendiente Total' 
                WHEN b.claEstatusFabricacion = 5 THEN 'Surtido Parcial' 
                ELSE 'Otro' 
            END AS NomEstatusFabricacion,
            d.claveArticulo, d.nomArticulo, PrecioUnitario, PrecioConfidencial, 
            a.ClaEstatusFabricacion AS claEstatusFabricacionEnc,
            CASE 
                WHEN a.claEstatusFabricacion = 3 THEN 'Cancelada' 
                WHEN a.claEstatusFabricacion = 6 THEN 'Surtido Total' 
                WHEN a.claEstatusFabricacion = 4 THEN 'Pendiente Total' 
                WHEN a.claEstatusFabricacion = 5 THEN 'Surtido Parcial' 
                ELSE 'Otro' 
            END AS NomEstatusFabricacionEnc
        FROM `dfor-prj-prod.dlabsbd01_kraken_abt.VtaSch_VtaTraFabricacion` a
        INNER JOIN `dfor-prj-prod.dlabsbd01_kraken_abt.VtaSch_VtaTraFabricacionDet` b 
            ON b.idFabricacion = a.idFabricacion
        INNER JOIN `dfor-prj-prod.dlabsbd01_kraken_abt.dbo_TiCatUbicacion` c 
            ON c.claUbicacion = a.claUbicacion AND c.claEmpresa IN (52,59)
        INNER JOIN `dfor-prj-prod.dlabsbd01_kraken_abt.dbo_ArtCatArticulo` d 
            ON d.ClaTipoInventario = 1 AND d.ClaArticulo = b.ClaArticulo
    ),
    
    -- CTE 2: Datos de Fabricación Encabezado
    ITK002FabricacionEnc AS (
        SELECT 
            a.idFabricacion, a.claCliente, a.ClaProyecto, a.ClaUbicacion, 
            SUM(a.KgsPedidosFabricacion) AS KgsPedidosFabricacion, 
            SUM(a.KgsSurtidosFabricacion) AS KgsSurtidosFabricacion, 
            a.FechaCaptura, a.fechaBaseFabricacion, a.FechaPromesaOriginal, a.FechaPromesaActual, 
            a.FechaNecesitaCliente, a.ClaPedidoCliente, a.fechaPedidoCliente, a.claConsignado
        FROM ITK002FabricacionDet a
        GROUP BY 
            a.idFabricacion, a.claCliente, a.ClaProyecto, a.ClaUbicacion, 
            a.FechaCaptura, a.fechaBaseFabricacion, a.FechaPromesaOriginal, a.FechaPromesaActual, 
            a.FechaNecesitaCliente, a.ClaPedidoCliente, a.fechaPedidoCliente, a.claConsignado
    ),
    
    -- CTE 3: Datos de Remisión Base
    ITK001Remision AS (
        SELECT DISTINCT 
            b.idfactura, b.idfacturaalfanumerico, b.cscCfdi AS csc
        FROM `dfor-prj-prod.dlabsbd01_kraken_abt.dbo_VtaCatClienteCuenta` a
        INNER JOIN `dfor-prj-prod.dlabsbd01_kraken_abt.VtaSch_VtaCTraFactura` b 
            ON b.claCliente = a.claClienteCuenta
        INNER JOIN ITK002FabricacionEnc c ON c.idfabricacion = b.idFabricacion
        INNER JOIN `dfor-prj-prod.dlabsbd01_kraken_abt.dbo_TiCatUbicacion` d 
            ON d.claubicacion = c.claUbicacion
        WHERE d.claEmpresa IN (52,59)
    ),
    
    -- CTE 4: Estatus de Facturas
    FacturaEstatus AS (
        SELECT 
            T0.idfactura, T0.idfacturaAlfanumerico, T0.csc,
            CASE 
                WHEN SFC.SatEstatus IS NOT NULL THEN 'Cancelada' 
                WHEN SF.ioestatus IN (1) THEN 'Timbrada' 
                ELSE 'No Timbrada' 
            END AS valorEstatus,
            CASE 
                WHEN SFC.SatEstatus IS NOT NULL THEN SFC.ioestatus 
                ELSE SF.ioestatus 
            END AS ClaEstatus,
            TRIM(SF.rfcEmisor) AS rfcEmisor, 
            TRIM(SF.rfcCliente) AS rfcCliente, 
            SF.UUID
        FROM ITK001Remision T0
        LEFT JOIN `dfor-prj-prod.dlabsbd01_kraken_abt.FESCH_conn_encabezado` SF 
            ON T0.idfacturaAlfanumerico = SF.FolioErp
        LEFT JOIN `dfor-prj-prod.dlabsbd01_kraken_abt.FESCH_conn_cancelados` SFC 
            ON SF.Csc = SFC.csc AND SFC.ioestatus = 3
    ),
    
    -- CTE 5: Detalles de Remisión
    RemisionDetalle AS (
        SELECT 
            *, 
            SUM(ValorDeRemision) OVER (PARTITION BY idfactura) AS TotalValorRemisionesEnFactura
        FROM (
            SELECT 
                fact.idfactura, fact.idfacturaalfanumerico, fact.impfactura, fact.kilossurtidos, 
                mov.idfacturaalfanumerico AS remision, 
                MAX(CAST(fact.FechaFactura AS TIMESTAMP)) AS FechaFactura, 
                fabDet.ClaProyecto, 
                SUM(movdet.pesoembarcado) AS KilosDeRemision, 
                SUM(movdet.pesoembarcado * fabDet.PrecioEntrega) AS ValorDeRemision, 
                fact.claformaPago
            FROM `dfor-prj-prod.dlabsbd01_kraken_abt.OpeSch_OpeTraPlanCargaRemisionEstimacion` est
            LEFT JOIN `dfor-prj-prod.dlabsbd01_kraken_abt.OpeSch_OpeTraMovEntSal` mov 
                ON est.claubicacionventa = mov.claubicacion 
                AND est.idviajeventa = mov.idviaje 
                AND clamotivoEntrada = 1
            LEFT JOIN `dfor-prj-prod.dlabsbd01_kraken_abt.OpeSch_OPETraMovEntSalDet` movdet 
                ON mov.idmoventsal = movdet.idmoventsal 
                AND mov.claubicacion = movdet.claubicacion
            LEFT JOIN `dfor-prj-prod.dlabsbd01_kraken_abt.OpeSch_OpeTraRelFacturaRemisionEstimacionDet` det 
                ON det.remisionalfanumerico = mov.idfacturaalfanumerico 
                AND det.ClaArticulo = movdet.ClaArticulo
            LEFT JOIN `dfor-prj-prod.dlabsbd01_kraken_abt.VtaSch_vtaTraProforma` pro 
                ON det.folioproforma = pro.idproforma
            LEFT JOIN `dfor-prj-prod.dlabsbd01_kraken_abt.VtaSch_VtaCTraFactura` fact 
                ON pro.idfacturanueva = fact.idfactura
            LEFT JOIN ITK002FabricacionDet fabDet 
                ON fabDet.IdFabricacion = movdet.IdFabricacion 
                AND fabDet.NumeroRenglon = movdet.IdFabricacionDet
            WHERE fact.idfactura IS NOT NULL
            GROUP BY 
                fact.idfactura, fact.idfacturaalfanumerico, fact.impfactura, fact.kilossurtidos, 
                mov.idfacturaalfanumerico, fabDet.ClaProyecto, fact.claformaPago
        )
    ),
    
    -- CTE 6: CXC Agregado
    CXC_Agregado AS (
        SELECT
            factura_alfanumerica,
            MAX(nombre_movimiento_cartera) AS nombre_movimiento_cartera,
            MAX(nombre_grupo_movimiento_cartera) AS nombre_grupo_movimiento_cartera,
            MAX(nombre_tipo_movimiento) AS nombre_tipo_movimiento,
            SUM(kilos_reales) AS kilos_reales
        FROM `datahub-deacero.mart_finanzas.cuentas_x_cobrar`
        WHERE nombre_movimiento_cartera = '001 - FACTURAS DE EMBARQUE'
        GROUP BY factura_alfanumerica
    ),
    
    -- CTE 7: Archivo POD 
    FacturaPod AS (
        SELECT 
            clave,
            NombreEnUbicacion
        FROM `dfor-prj-prod.dlabsbd01_kraken_abt.VtaSch_VtaTraPodArchivo`
    )
    
    -- CONSULTA PRINCIPAL
    SELECT
        CAST(b.fechaFactura AS TIMESTAMP) AS fechaFactura, 
        ROW_NUMBER() OVER (ORDER BY b.idfactura) AS consecutivo, 
        b.idfacturaAlfanumerico, b.idFactura, fe.csc, fe.claestatus, fe.valorEstatus, 
        fe.rfcEmisor, fe.rfcCliente, fe.uuid,
        b.claformaPago, fp.NombreFormaPago,
        b.DiasPlazoNormal,
        CAST(b.fechavenceNormal AS TIMESTAMP) AS fechavenceNormal,
        b.diasPlazoConf,
        CAST(b.FechaVenceConf AS TIMESTAMP) AS FechaVenceConf,
        b.impFactura,
        b.kilosSurtidos AS KilosTOTALFactura, 
        '1-Factura Directa' AS Tipo,
        cc.claClienteCuenta, cu.nombreRazonSocial, proy.ClaProyecto, proy.NomProyecto,
        CAST(NULL AS STRING) AS Remision,
        pod.NombreEnUbicacion AS NombreArchivoPOD,
        CXC.nombre_movimiento_cartera,
        CXC.nombre_grupo_movimiento_cartera,
        CXC.nombre_tipo_movimiento,
        CXC.kilos_reales
    FROM `dfor-prj-prod.dlabsbd01_kraken_abt.VtaSch_VtaCTraFactura` b
    INNER JOIN ITK001Remision a ON b.idFactura = a.idfactura
    LEFT JOIN FacturaEstatus fe ON a.idfactura = fe.idfactura
    LEFT JOIN `dfor-prj-prod.deadwh_dwhfinanzas_abt.dbo_DwhVtaCatFormaPago` fp 
        ON b.claformaPago = fp.claFormaPago
    LEFT JOIN `dfor-prj-prod.dlabsbd01_kraken_abt.dbo_VtaCatClienteCuenta` cc 
        ON b.claCliente = cc.claClienteCuenta
    LEFT JOIN `dfor-prj-prod.dlabsbd01_kraken_abt.dbo_VtaCatClienteUnico` cu 
        ON cc.claClienteUnico = cu.claClienteUnico
    LEFT JOIN ITK002FabricacionEnc fab ON b.idFabricacion = fab.idFabricacion
    LEFT JOIN `dfor-prj-prod.dlabsbd01_kraken_abt.VtaSch_VtaTraControlProyecto` proy 
        ON fab.ClaProyecto = proy.claProyecto
    LEFT JOIN CXC_Agregado AS CXC
        ON CXC.factura_alfanumerica = b.idfacturaAlfanumerico
    LEFT JOIN FacturaPod AS pod
        ON b.idFactura = pod.clave
    WHERE b.idfactura NOT IN (SELECT DISTINCT idfactura FROM RemisionDetalle WHERE idfactura IS NOT NULL)
        AND CAST(b.fechaFactura AS DATE) BETWEEN '{fecha_desde}' AND '{fecha_hasta}'
        {'AND cu.nombreRazonSocial LIKE "%' + cliente + '%"' if cliente else ''}
        {'AND proy.NomProyecto LIKE "%' + proyecto + '%"' if proyecto else ''}
    
    UNION ALL
    
    -- 2. Facturas de Remisión/Estimación
    SELECT
        det.FechaFactura, 
        ROW_NUMBER() OVER (ORDER BY det.idfactura) + 500000 AS consecutivo, 
        det.idfacturaalfanumerico, det.idfactura, fe.csc, fe.claestatus, fe.valorEstatus, 
        fe.rfcEmisor, fe.rfcCliente, fe.uuid,
        det.claformaPago, fp.NombreFormaPago,
        CAST(NULL AS INT64) AS DiasPlazoNormal,
        CAST(NULL AS TIMESTAMP) AS fechavenceNormal,
        CAST(NULL AS INT64) AS diasPlazoConf,
        CAST(NULL AS TIMESTAMP) AS FechaVenceConf,
        det.impfactura,
        det.kilossurtidos AS KilosTOTALFactura, 
        '2-Factura Estimación' AS Tipo,
        cc.claClienteCuenta, cu.nombreRazonSocial, proy.ClaProyecto, proy.NomProyecto,
        det.remision AS Remision,
        pod.NombreEnUbicacion AS NombreArchivoPOD,
        CXC.nombre_movimiento_cartera,
        CXC.nombre_grupo_movimiento_cartera,
        CXC.nombre_tipo_movimiento,
        CXC.kilos_reales
    FROM RemisionDetalle det
    LEFT JOIN FacturaEstatus fe ON det.idfactura = fe.idfactura
    LEFT JOIN `dfor-prj-prod.deadwh_dwhfinanzas_abt.dbo_DwhVtaCatFormaPago` fp 
        ON det.claformaPago = fp.claFormaPago
    LEFT JOIN ITK002FabricacionEnc fab ON det.idFactura = fab.idFabricacion
    LEFT JOIN `dfor-prj-prod.dlabsbd01_kraken_abt.dbo_VtaCatClienteCuenta` cc 
        ON fab.claCliente = cc.claClienteCuenta
    LEFT JOIN `dfor-prj-prod.dlabsbd01_kraken_abt.dbo_VtaCatClienteUnico` cu 
        ON cc.claClienteUnico = cu.claClienteUnico
    LEFT JOIN `dfor-prj-prod.dlabsbd01_kraken_abt.VtaSch_VtaTraControlProyecto` proy 
        ON det.ClaProyecto = proy.claProyecto
    LEFT JOIN CXC_Agregado AS CXC
        ON CXC.factura_alfanumerica = det.idfacturaalfanumerico
    LEFT JOIN FacturaPod AS pod
        ON det.idFactura = pod.clave
    WHERE CAST(det.FechaFactura AS DATE) BETWEEN '{fecha_desde}' AND '{fecha_hasta}'
        {'AND cu.nombreRazonSocial LIKE "%' + cliente + '%"' if cliente else ''}
        {'AND proy.NomProyecto LIKE "%' + proyecto + '%"' if proyecto else ''}
    
    ORDER BY idFactura, Remision
    LIMIT {limite}
    """
    
    return query


# Área principal
if consultar or 'df_facturas' not in st.session_state:
    if consultar:
        with st.spinner("🔍 Consultando BigQuery..."):
            client = get_bigquery_client()
            
            if client:
                try:
                    query = ejecutar_query_facturas(
                        fecha_desde, 
                        fecha_hasta, 
                        cliente_filter, 
                        proyecto_filter,
                        limite
                    )
                    
                    # Ejecutar query
                    df = client.query(query).to_dataframe()
                    
                    # Generar URLs de PODs
                    df['URL_POD'] = df['NombreArchivoPOD'].apply(generar_url_pod)
                    
                    st.session_state.df_facturas = df
                    st.success(f"✅ {len(df)} facturas encontradas")
                    
                except Exception as e:
                    st.error(f"❌ Error en consulta: {e}")
                    st.session_state.df_facturas = pd.DataFrame()
            else:
                st.warning("⚠️ No se pudo conectar a BigQuery. Verifica credenciales.")

# Mostrar resultados
if 'df_facturas' in st.session_state and not st.session_state.df_facturas.empty:
    df = st.session_state.df_facturas
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Facturas", f"{len(df):,}")
    
    with col2:
        total_importe = df['impFactura'].sum()
        st.metric("Importe Total", f"${total_importe:,.2f}")
    
    with col3:
        total_kilos = df['KilosTOTALFactura'].sum()
        st.metric("Kilos Totales", f"{total_kilos:,.0f}")
    
    with col4:
        con_pod = df['NombreArchivoPOD'].notna().sum()
        st.metric("Facturas con POD", f"{con_pod} ({con_pod/len(df)*100:.1f}%)")
    
    st.divider()
    
    # Tabla con link a PODs
    st.subheader("📋 Facturas")
    
    # Preparar dataframe para mostrar con los campos correctos
    columnas_mostrar = [
        'consecutivo', 'fechaFactura', 'idfacturaAlfanumerico', 
        'nombreRazonSocial', 'NomProyecto', 'Remision',
        'impFactura', 'kilos_reales', 'KilosDeRemision', 'valorEstatus',
        'NombreArchivoPOD', 'URL_POD'
    ]
    
    # Verificar qué columnas existen
    columnas_disponibles = [col for col in columnas_mostrar if col in df.columns]
    
    df_display = df[columnas_disponibles].copy()
    
    # Renombrar columnas
    nombres_columnas = {
        'consecutivo': 'No.',
        'fechaFactura': 'Fecha',
        'idfacturaAlfanumerico': 'Factura',
        'nombreRazonSocial': 'Cliente',
        'NomProyecto': 'Proyecto',
        'Remision': 'Remisión',
        'impFactura': 'Importe',
        'kilos_reales': 'Kilos Reales',
        'KilosDeRemision': 'Kilos Remisión',
        'valorEstatus': 'Estatus',
        'NombreArchivoPOD': 'Archivo POD',
        'URL_POD': 'Link POD'
    }
    
    df_display.rename(columns=nombres_columnas, inplace=True)
    
    # Formatear fechas y números
    if 'Fecha' in df_display.columns:
        df_display['Fecha'] = pd.to_datetime(df_display['Fecha']).dt.strftime('%Y-%m-%d')
    
    if 'Importe' in df_display.columns:
        df_display['Importe'] = df_display['Importe'].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "")
    
    if 'Kilos Reales' in df_display.columns:
        df_display['Kilos Reales'] = df_display['Kilos Reales'].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else "")
    
    if 'Kilos Remisión' in df_display.columns:
        df_display['Kilos Remisión'] = df_display['Kilos Remisión'].apply(lambda x: f"{x:,.0f}" if pd.notna(x) else "")
    
    # Mostrar tabla con links clickeables
    st.dataframe(
        df_display,
        column_config={
            "Link POD": st.column_config.LinkColumn(
                "Ver POD",
                help="Clic para ver el documento POD",
                display_text="📄 Ver"
            )
        },
        hide_index=True,
        use_container_width=True,
        height=600
    )
    
    # Descargar resultados
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Descargar Excel/CSV",
        data=csv,
        file_name=f"facturas_pods_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

else:
    st.info("👆 Configura los filtros en el panel lateral y haz clic en 'Consultar Facturas'")
    
    st.markdown("""
    ### 📖 Instrucciones
    
    Esta página muestra:
    - Facturas directas y de estimación
    - Link directo a documentos POD en Google Cloud Storage
    - Filtros por fecha, cliente y proyecto
    
    **Para comenzar:**
    1. Ajusta las fechas en el panel lateral
    2. Opcionalmente filtra por cliente o proyecto
    3. Haz clic en "🔍 Consultar Facturas"
    4. Haz clic en "📄 Ver" para abrir el POD
    """)

