"""Componentes UI reutilizables para la aplicación Streamlit.
Componentes profesionales siguiendo mejores prácticas de UX.
"""

from datetime import datetime

import geopandas as gpd
import streamlit as st

from translations import HEADER_SUBTITLE, HEADER_TITLE


def render_header() -> None:
    """Renderiza el header principal de la aplicación."""
    st.markdown(
        f"""
        <div class="main-header">
            <h1>{HEADER_TITLE}</h1>
            <p>{HEADER_SUBTITLE}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metrics_dashboard(
    data: gpd.GeoDataFrame,
    raw_data: gpd.GeoDataFrame,
    country_data: gpd.GeoDataFrame,
) -> None:
    """Renderiza el dashboard de métricas principales.

    Args:
        data: GeoDataFrame con los datos limpios de crocodílidos.
        raw_data: GeoDataFrame con los datos sin limpiar (para calcular calidad).
        country_data: GeoDataFrame con los datos de países.
    """
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_metric_card(
            label="Total de Registros",
            value=f"{len(data):,}",
            delta=None,
        )

    with col2:
        unique_species = data["Especie"].nunique()
        render_metric_card(
            label="Especies Únicas",
            value=str(unique_species),
            delta=None,
        )

    with col3:
        # Spatial join para contar países
        joined = gpd.sjoin(
            data,
            country_data,
            how="inner",
            predicate="within",
        )
        unique_countries = joined["ADMIN"].nunique()
        render_metric_card(
            label="Países con Presencia",
            value=str(unique_countries),
            delta=None,
        )

    with col4:
        # Calcular calidad de datos (% de registros originales con coordenadas válidas)
        valid_coords = raw_data.dropna(subset=["decimalLatitude", "decimalLongitude"])
        quality_pct = (len(valid_coords) / len(raw_data)) * 100 if len(raw_data) > 0 else 0
        render_metric_card(
            label="Calidad de Datos",
            value=f"{quality_pct:.1f}%",
            delta="registros con coordenadas",
        )


def render_metric_card(label: str, value: str, delta: str | None) -> None:
    """Renderiza una tarjeta de métrica individual.

    Args:
        label: Etiqueta de la métrica.
        value: Valor principal a mostrar.
        delta: Texto secundario opcional (cambio, descripción, etc.).
    """
    delta_html = f'<div class="metric-delta">{delta}</div>' if delta else ""

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(title: str, description: str) -> None:
    """Renderiza un header de sección con título y descripción.

    Args:
        title: Título de la sección.
        description: Descripción o contexto de la sección.
    """
    st.markdown(f"### {title}")
    st.markdown(
        f"<p style='color: #6b7280; margin-bottom: 1.5rem;'>{description}</p>",
        unsafe_allow_html=True,
    )


def render_sidebar_section(title: str) -> None:
    """Renderiza un header de sección en el sidebar.

    Args:
        title: Título de la sección del sidebar.
    """
    st.markdown(
        f"""
        <div class="sidebar-section">
            <h3>{title}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    """Renderiza el footer con atribuciones y información académica."""
    st.divider()

    st.markdown("#### Fuente de Datos")
    st.markdown(
        "GBIF.org (12 noviembre 2025) Ocurrencias de Crocodilia. "
        "Datos obtenidos de [GBIF.org](https://www.gbif.org)"
    )

    st.markdown("#### Metodología")
    st.markdown(
        "Los datos fueron procesados y convertidos a formato Parquet para optimizar el rendimiento. "
        "Se aplicó limpieza de datos para asegurar la calidad de las coordenadas geográficas y la "
        "información taxonómica."
    )

    st.markdown("#### Licencia")
    st.markdown(
        "Datos disponibles bajo licencia Creative Commons. "
        "Consulte GBIF.org para detalles específicos."
    )

    st.caption("Desarrollado con Streamlit, GeoPandas y Folium | © 2025")


def render_empty_state(title: str, message: str) -> None:
    """Renderiza un estado vacío cuando no hay datos.

    Args:
        title: Título del estado vacío.
        message: Mensaje explicativo.
    """
    st.markdown(
        f"""
        <div class="empty-state">
            <h3>{title}</h3>
            <p>{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_loading_state(message: str) -> None:
    """Renderiza un indicador de carga.

    Args:
        message: Mensaje a mostrar durante la carga.
    """
    st.markdown(
        f"""
        <div class="loading-state">
            <div class="spinner"></div>
            <p style="margin-top: 1rem;">{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
