"""Utilidades de visualización para mapas y gráficos.

Funciones optimizadas para renderizar visualizaciones interactivas de alta calidad.
"""

import folium
import geopandas as gpd
import plotly.express as px
import streamlit as st
from branca.colormap import LinearColormap
from folium.plugins import FastMarkerCluster
from streamlit_folium import st_folium

from translations import (
    HELP_BAR_CHART,
    HELP_CHOROPLETH,
    HELP_POINT_MAP,
)


def create_point_map(data: gpd.GeoDataFrame) -> folium.Map:
    """Crea un mapa interactivo con puntos de ocurrencia usando FastMarkerCluster.

    Args:
        data: GeoDataFrame con columnas 'decimalLatitude', 'decimalLongitude', 'species'.

    Returns:
        Mapa de Folium con puntos agrupados.
    """
    center_lat = data["decimalLatitude"].mean()
    center_lon = data["decimalLongitude"].mean()

    point_map = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=2,
        tiles="CartoDB positron",
    )

    # Preparar datos para FastMarkerCluster
    callback = """\
    function (row) {
        var marker = L.marker(new L.LatLng(row[0], row[1]));
        marker.bindPopup("<b>Especie:</b> " + row[2]);
        return marker;
    }
    """

    locations = [
        [row.decimalLatitude, row.decimalLongitude, row.Especie] for row in data.itertuples()
    ]

    FastMarkerCluster(
        data=locations,
        callback=callback,
    ).add_to(point_map)

    return point_map


def create_choropleth_map(
    data: gpd.GeoDataFrame,
    country_data: gpd.GeoDataFrame,
) -> folium.Map:
    """Crea un mapa coroplético mostrando riqueza de especies por país.

    Args:
        data: GeoDataFrame con datos de ocurrencia de especies.
        country_data: GeoDataFrame con polígonos de países.

    Returns:
        Mapa de Folium con colores por número de especies.
    """
    # Spatial join para asignar país a cada punto
    joined = gpd.sjoin(
        data,
        country_data,
        how="inner",
        predicate="within",
    )

    # Contar especies únicas por país
    species_by_country = (
        joined.groupby("ADMIN")["Especie"].nunique().reset_index(name="num_species")
    )

    # Merge con geometrías de países
    country_data_merged = country_data.merge(
        right=species_by_country,
        on="ADMIN",
        how="left",
    )
    country_data_merged["num_species"] = country_data_merged["num_species"].fillna(0)

    # Crear mapa base
    choropleth_map = folium.Map(
        location=[0, 0],
        zoom_start=2,
        tiles="CartoDB positron",
    )

    # Crear escala de colores
    min_species = country_data_merged["num_species"].min()
    max_species = country_data_merged["num_species"].max()

    colormap = LinearColormap(
        colors=["#fee5d9", "#fcae91", "#fb6a4a", "#de2d26", "#a50f15"],
        vmin=min_species,
        vmax=max_species,
        caption="Número de especies",
    )

    # Agregar capa coroplética
    folium.GeoJson(
        data=country_data_merged,
        style_function=lambda feature: {
            "fillColor": colormap(feature["properties"]["num_species"])
            if feature["properties"]["num_species"] > 0
            else "#f0f0f0",
            "color": "#333333",
            "weight": 0.5,
            "fillOpacity": 0.7,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["ADMIN", "num_species"],
            aliases=["País:", "Especies:"],
            localize=True,
        ),
    ).add_to(choropleth_map)

    colormap.add_to(choropleth_map)

    return choropleth_map


def create_top_species_chart(
    data: gpd.GeoDataFrame,
    top_n: int = 10,
) -> None:
    """Crea un gráfico de barras con las especies más comunes.

    Args:
        data: GeoDataFrame con columna 'species'.
        top_n: Número de especies principales a mostrar.
    """
    species_counts = data["Especie"].value_counts().reset_index()
    species_counts.columns = ["Especie", "Número de registros"]
    top_species = species_counts.head(top_n)

    fig = px.bar(
        data_frame=top_species,
        x="Número de registros",
        y="Especie",
        orientation="h",
        color="Número de registros",
        color_continuous_scale="Viridis",
        labels={"Número de registros": "Número de registros", "Especie": "Especie"},
    )

    fig.update_layout(
        height=max(400, top_n * 40),
        showlegend=False,
        yaxis={"categoryorder": "total ascending"},
        font={"family": "Inter, sans-serif"},
    )

    st.plotly_chart(
        figure_or_data=fig,
        width="stretch",
    )

    st.caption(HELP_BAR_CHART)


def render_point_map(data: gpd.GeoDataFrame) -> None:
    """Renderiza el mapa de puntos con wrapper HTML profesional.

    Args:
        data: GeoDataFrame con datos de ocurrencia.
    """
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    point_map = create_point_map(data=data)
    st_folium(
        fig=point_map,
        width="stretch",
        height=600,
    )
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption(HELP_POINT_MAP)


def render_choropleth_map(
    data: gpd.GeoDataFrame,
    country_data: gpd.GeoDataFrame,
) -> None:
    """Renderiza el mapa coroplético con wrapper HTML profesional.

    Args:
        data: GeoDataFrame con datos de ocurrencia.
        country_data: GeoDataFrame con polígonos de países.
    """
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    m = create_choropleth_map(
        data=data,
        country_data=country_data,
    )
    st_folium(
        fig=m,
        width="stretch",
        height=600,
    )
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption(HELP_CHOROPLETH)
