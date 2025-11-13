"""Textos y traducciones en español para la aplicación.
Centraliza todos los strings de la UI para mantener consistencia académica.
"""

# Header
HEADER_TITLE = "Sistema de Análisis Geoespacial de Crocodilia"
HEADER_SUBTITLE = (
    "Plataforma de análisis y visualización de datos de biodiversidad | "
    "GBIF Global Biodiversity Information Facility"
)

# Sidebar
SIDEBAR_FILTERS_TITLE = "Filtros de Datos"
SIDEBAR_VIZ_TITLE = "Opciones de Visualización"
SIDEBAR_EXPORT_TITLE = "Exportación de Datos"

# Filtros
FILTER_SPECIES_LABEL = "Seleccionar especies"
FILTER_SPECIES_HELP = "Filtre por una o más especies de interés. Deje vacío para mostrar todas."
FILTER_TOP_N_LABEL = "Top N especies a mostrar"
FILTER_TOP_N_HELP = "Número de especies más comunes a visualizar en los gráficos"

# Métricas
METRIC_TOTAL_RECORDS = "Total de Registros"
METRIC_SPECIES_COUNT = "Especies Únicas"
METRIC_COUNTRIES_COUNT = "Países con Presencia"
METRIC_DATA_QUALITY = "Calidad de Datos"

# Tabs
TAB_OVERVIEW = "📊 Resumen General"
TAB_DISTRIBUTION = "🗺️ Distribución Geográfica"
TAB_ANALYTICS = "📈 Análisis Estadístico"
TAB_DATA_TABLE = "📋 Tabla de Datos"

# Sección Resumen
OVERVIEW_TITLE = "Resumen del Conjunto de Datos"
OVERVIEW_DESCRIPTION = (
    "Este panel presenta un análisis exploratorio de los datos de ocurrencia de crocodílidos "
    "obtenidos de GBIF (Global Biodiversity Information Facility). Los datos incluyen registros "
    "georreferenciados de observaciones y especímenes a nivel mundial."
)

# Sección Distribución
DISTRIBUTION_POINTS_TITLE = "Mapa de Puntos de Ocurrencia"
DISTRIBUTION_POINTS_DESCRIPTION = (
    "Visualización de todas las ubicaciones geográficas donde se han "
    "registrado observaciones de crocodílidos."
)
DISTRIBUTION_CHOROPLETH_TITLE = "Mapa Coroplético: Riqueza de Especies por País"
DISTRIBUTION_CHOROPLETH_DESCRIPTION = "Número de especies únicas registradas en cada país."

# Sección Analytics
ANALYTICS_TOP_SPECIES_TITLE = "Especies con Mayor Número de Registros"
ANALYTICS_TOP_SPECIES_DESCRIPTION = (
    "Distribución de registros entre las especies más comúnmente observadas."
)

# Tabla de datos
TABLE_TITLE = "Explorador de Datos Completo"
TABLE_DESCRIPTION = (
    "Vista detallada de todos los registros filtrados con información taxonómica y geográfica."
)
TABLE_SEARCH_PLACEHOLDER = "Buscar en la tabla..."
TABLE_RECORDS_LABEL = "Número de registros a mostrar"

# Mensajes de estado
MSG_LOADING_DATA = "Cargando datos desde Parquet..."
MSG_CLEANING_DATA = "Procesando y limpiando datos..."
MSG_GENERATING_MAP = "Generando mapa interactivo..."
MSG_COMPUTING_STATS = "Calculando estadísticas..."
MSG_NO_DATA = "No hay datos disponibles con los filtros seleccionados."
MSG_NO_SPECIES_SELECTED = "Por favor, seleccione al menos una especie para visualizar."

# Footer
FOOTER_DATA_SOURCE = "Fuente de Datos"
FOOTER_GBIF_CITATION = "GBIF.org (12 noviembre 2025) Ocurrencias de Crocodilia. Datos obtenidos de"
FOOTER_GBIF_LINK = "https://www.gbif.org"
FOOTER_METHODOLOGY = "Metodología"
FOOTER_METHODOLOGY_TEXT = """
Los datos fueron procesados y convertidos a formato Parquet para optimizar el rendimiento.
Se aplicó limpieza de datos para asegurar la calidad de las coordenadas geográficas y la
información taxonómica.
"""
FOOTER_CITATION = "Cómo Citar"
FOOTER_CITATION_TEXT = """
Si utiliza estos datos en publicaciones académicas, por favor cite:
GBIF.org (2025). Ocurrencias de Crocodilia. Accedido vía Sistema de Análisis Geoespacial
de Crocodilia el {date}.
"""
FOOTER_LICENSE = "Licencia"
FOOTER_LICENSE_TEXT = (
    "Datos disponibles bajo licencia Creative Commons. Consulte GBIF.org para detalles específicos."
)

# Exportación
EXPORT_FORMAT_LABEL = "Formato de exportación"
EXPORT_BUTTON_CSV = "📥 Descargar CSV"
EXPORT_BUTTON_GEOJSON = "📥 Descargar GeoJSON"
EXPORT_FILENAME_PREFIX = "crocodilia_data"

# Errores
ERROR_LOADING_DATA = (
    "Error al cargar los datos. Por favor, verifique que el archivo Parquet existe."
)
ERROR_PROCESSING = "Error durante el procesamiento de datos."
ERROR_VISUALIZATION = "Error al generar la visualización."

# Ayuda y tooltips
HELP_POINT_MAP = "Haga clic en los puntos para ver información detallada de cada registro."
HELP_CHOROPLETH = "Los colores más oscuros indican mayor diversidad de especies."
HELP_BAR_CHART = "Gráfico interactivo. Haga clic y arrastre para hacer zoom."
