import folium
import geopandas as gpd
import pandas as pd
import plotly.express as px
import polars as pl
import streamlit as st
from branca.colormap import LinearColormap
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

from config import COUNTRY_DATA_SOURCE, CROCODILE_DATA_SOURCE

# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------
st.set_page_config(
    page_title="Identificador de Cocodrilos",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ------------------------------------------------------------
# DATA LOADING FUNCTIONS
# ------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_crocodiles_data() -> gpd.GeoDataFrame:
    """Cargar datos de ocurrencia de cocodrilos y convertir a GeoDataFrame."""
    # We use Polars for efficient CSV loading
    data = pl.read_csv(
        source=CROCODILE_DATA_SOURCE,
        separator="\t",
        quote_char=None,
        truncate_ragged_lines=True,
    )
    df = data.to_pandas()
    gdf = gpd.GeoDataFrame(
        data=df,
        geometry=gpd.points_from_xy(
            x=df.decimalLongitude,
            y=df.decimalLatitude,
        ),
        crs="EPSG:4326",
    )
    return gdf


@st.cache_data(show_spinner=False)
def load_country_data() -> gpd.GeoDataFrame:
    """Cargar datos geoespaciales de países."""
    gdf = gpd.read_file(COUNTRY_DATA_SOURCE)
    # Asegurarnos de que los datos del país estén en EPSG:4326 para operaciones espaciales
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")
    elif gdf.crs.to_string() != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")
    return gpd.GeoDataFrame(
        data=gdf,
        geometry="geometry",
        crs=gdf.crs,
    )


# ------------------------------------------------------------
# DATA PROCESSING FUNCTIONS
# ------------------------------------------------------------
def clean_crocodile_data(data: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Conservar columnas relevantes y asegurar que la geometría se preserve."""
    columns = [
        "species",
        "acceptedScientificName",
        "decimalLatitude",
        "decimalLongitude",
        "geometry",
    ]
    data = data.loc[:, columns].copy()
    data = data.rename(
        columns={
            "species": "Especie",
            "acceptedScientificName": "Nombre científico",
            "decimalLatitude": "Latitud",
            "decimalLongitude": "Longitud",
        }
    )
    match data:
        case gpd.GeoDataFrame():
            pass
        case _:
            data = gpd.GeoDataFrame(
                data=data,
                geometry=gpd.points_from_xy(
                    x=data["Longitud"],
                    y=data["Latitud"],
                ),
                crs="EPSG:4326",
            )
    data = gpd.GeoDataFrame(
        data=data,
        geometry="geometry",
        crs=data.crs,
    )
    return data


def compute_species_counts(data: pd.DataFrame | gpd.GeoDataFrame, top_n: int = 10) -> pd.DataFrame:
    """Contar las ocurrencias de cocodrilos por especie."""
    counts = (
        data["Especie"]
        .value_counts()
        .reset_index()
        .rename(
            columns={
                "index": "Especie",
                "count": "Registros",
            }
        )
        .head(top_n)
    )
    return counts


# ------------------------------------------------------------
# VISUALIZATION FUNCTIONS
# ------------------------------------------------------------
def plot_species_bar_chart(species_counts: pd.DataFrame) -> None:
    """Crear un gráfico de barras con las ocurrencias por especie."""
    fig = px.bar(
        data_frame=species_counts,
        x="Especie",
        y="Registros",
        color="Registros",
        color_continuous_scale="Viridis",
        title="Top 10 especies de cocodrilos por número de registros",
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font={"size": 12},
    )
    st.plotly_chart(figure_or_data=fig, use_container_width=True)


def create_point_map(data: gpd.GeoDataFrame) -> None:
    """Crear un mapa con puntos de ocurrencia usando clustering para mejorar rendimiento."""
    with st.spinner("Cargando mapa de puntos..."):
        m = folium.Map(location=[10, 10], zoom_start=2, tiles="cartodb positron")
        marker_cluster = MarkerCluster().add_to(m)

        # Añadir marcadores con popups
        for _, row in data.iterrows():
            # Saltar puntos sin geometría
            if row.geometry is None or row.geometry.is_empty:
                continue
            lat = row.geometry.y
            lon = row.geometry.x
            popup_html = (
                f"<b>Especie:</b> {row.get('Especie', 'Desconocida')}<br/>"
                f"<b>Nombre científico:</b> {row.get('Nombre científico', 'Desconocido')}"
            )
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(
                    html=popup_html,
                    max_width=300,
                ),
            ).add_to(marker_cluster)
        folium_static(
            fig=m,
            width=1100,
            height=600,
        )


def create_choropleth_map(data: gpd.GeoDataFrame, countries: gpd.GeoDataFrame) -> None:
    """Crear un mapa coroplético que muestre la diversidad de especies de cocodrilos por país."""
    with st.spinner("Cargando mapa coroplético..."):
        try:
            joined = gpd.sjoin(
                left_df=data,
                right_df=countries,
                predicate="intersects",
            )
        except Exception as e:
            st.error(f"Error al realizar la unión espacial: {e}")
            return

        if joined.empty:
            st.warning("No hay registros de ocurrencias para las especies seleccionadas.")
            return

        species_counts = (
            joined.groupby("NAME")["Especie"].nunique().reset_index(name="Especies únicas")
        )

        # Merge counts with country polygons
        countries_merged = countries.merge(
            right=species_counts,
            on="NAME",
            how="left",
        )
        # Reconstruir como GeoDataFrame para conservar geometría y CRS
        countries = gpd.GeoDataFrame(
            data=countries_merged,
            geometry="geometry",
            crs=countries.crs,
        )
        countries["Especies únicas"] = countries["Especies únicas"].fillna(0)

        countries = gpd.GeoDataFrame(
            data=countries.dropna(subset=["geometry"]),
            geometry="geometry",
            crs=countries.crs,
        )

        m = folium.Map(location=[10, 10], zoom_start=2, tiles="cartodb positron")

        # Build a LinearColormap explicitly using the YlGnBu 9-class ColorBrewer hex palette
        vmin = float(countries["Especies únicas"].min())
        vmax = float(countries["Especies únicas"].max())
        # Evitar problema cuando vmin == vmax
        if vmin == vmax:
            if vmin == 0.0:
                vmin, vmax = 0.0, 1.0
            else:
                vmin, vmax = vmin - 0.5, vmax + 0.5
        colormap = LinearColormap(
            colors=[
                "#ffffd9",
                "#edf8b1",
                "#c7e9b4",
                "#7fcdbb",
                "#41b6c4",
                "#1d91c0",
                "#225ea8",
                "#253494",
                "#081d58",
            ],
            vmin=vmin,
            vmax=vmax,
        )

        folium.GeoJson(
            data=countries,
            style_function=lambda feature: {
                "fillColor": colormap(feature["properties"]["Especies únicas"]),
                "color": "black",
                "weight": 0.4,
                "fillOpacity": 0.7,
            },
            highlight_function=lambda feature: {
                "weight": 2,
                "color": "black",
                "fillOpacity": 0.9,
            },
            tooltip=folium.features.GeoJsonTooltip(
                fields=["NAME", "Especies únicas"],
                aliases=["País:", "Especies únicas:"],
                localize=True,
            ),
        ).add_to(m)

        colormap.caption = "Especies únicas de cocodrilos por país"
        colormap.add_to(m)

        folium_static(
            fig=m,
            width=1100,
            height=600,
        )


# ------------------------------------------------------------
# MAIN APP LOGIC
# ------------------------------------------------------------
def main() -> None:
    st.title("Panel de Identificación de Cocodrilos")

    # Load data
    with st.spinner("Cargando datos de ocurrencia de cocodrilos..."):
        data = load_crocodiles_data()
    st.success("¡Datos de cocodrilos cargados correctamente!")

    with st.spinner("Cargando datos geoespaciales de países..."):
        countries = load_country_data()
    st.success("¡Datos de países cargados correctamente!")

    # Clean and display
    data = clean_crocodile_data(data)
    st.markdown("### Datos de ocurrencia de cocodrilos (desde GBIF)")
    # Sidebar filters
    species_options = sorted(data["Especie"].dropna().unique())
    selected_species = st.sidebar.multiselect(
        label="Filtrar por especie:",
        options=species_options,
    )
    map_type = st.sidebar.selectbox(
        label="Tipo de mapa:",
        options=[
            "Coroplético",
            "Puntos",
        ],
    )

    filtered_data = data[data["Especie"].isin(selected_species)] if selected_species else data
    # Asegurarnos de que `filtered_data` sea un GeoDataFrame
    match filtered_data:
        case gpd.GeoDataFrame():
            pass
        case _:
            filtered_data = gpd.GeoDataFrame(
                data=filtered_data,
                geometry="geometry",
                crs=data.crs,
            )

    st.dataframe(data=filtered_data, hide_index=True, use_container_width=True)

    # Bar chart
    st.markdown("### Top 10 especies de cocodrilos por número de registros")
    species_counts = compute_species_counts(pd.DataFrame(data=filtered_data))
    plot_species_bar_chart(species_counts)

    # Choropleth map
    st.markdown("### Ocurrencias globales de cocodrilos por país")
    if map_type == "Coroplético":
        create_choropleth_map(filtered_data, countries)
    else:
        create_point_map(filtered_data)


# ------------------------------------------------------------
# RUN APP
# ------------------------------------------------------------
if __name__ == "__main__":
    main()
