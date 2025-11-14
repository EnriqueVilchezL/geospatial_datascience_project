"""Aplicación principal de análisis geoespacial de Crocodilia.

Sistema académico profesional para visualización y análisis de datos de biodiversidad.
"""

try:
    import os
    import sys

    import geopandas as gpd
    import polars as pl
    import streamlit as st

    # Ensure repo root is on PYTHONPATH
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if ROOT not in sys.path:
        sys.path.append(ROOT)
    DATA_DIR = os.path.join(ROOT, "data")

    from components import (
        render_empty_state,
        render_footer,
        render_header,
        render_metrics_dashboard,
        render_section_header,
    )
    from config import COUNTRY_DATA_SOURCE, CROCODILE_DATA_SOURCE
    from styles import get_custom_css
    from translations import (
        ANALYTICS_TOP_SPECIES_DESCRIPTION,
        ANALYTICS_TOP_SPECIES_TITLE,
        DISTRIBUTION_CHOROPLETH_DESCRIPTION,
        DISTRIBUTION_CHOROPLETH_TITLE,
        DISTRIBUTION_POINTS_DESCRIPTION,
        DISTRIBUTION_POINTS_TITLE,
        FILTER_SPECIES_HELP,
        FILTER_SPECIES_LABEL,
        FILTER_TOP_N_HELP,
        FILTER_TOP_N_LABEL,
        MSG_NO_DATA,
        OVERVIEW_DESCRIPTION,
        OVERVIEW_TITLE,
        SIDEBAR_FILTERS_TITLE,
        TAB_ANALYTICS,
        TAB_DATA_TABLE,
        TAB_DISTRIBUTION,
        TAB_OVERVIEW,
        TABLE_DESCRIPTION,
        TABLE_RECORDS_LABEL,
        TABLE_TITLE,
    )
    from visualization import (
        create_top_species_chart,
        render_choropleth_map,
        render_point_map,
    )

    # ------------------------------------------------------------
    # CONFIGURATION
    # ------------------------------------------------------------
    st.set_page_config(
        page_title="Sistema de Análisis Geoespacial de Crocodilia",
        page_icon="🐊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Aplicar CSS personalizado
    st.markdown(body=get_custom_css(), unsafe_allow_html=True)


    # ------------------------------------------------------------
    # DATA LOADING FUNCTIONS
    # ------------------------------------------------------------
    @st.cache_data(show_spinner=False)
    def load_crocodiles_data() -> gpd.GeoDataFrame:
        """Cargar datos de ocurrencia de cocodrilos desde Parquet."""
        data = pl.read_parquet(source=os.path.join(DATA_DIR, CROCODILE_DATA_SOURCE)).head(500)
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
        gdf = gpd.read_file(filename=os.path.join(DATA_DIR, COUNTRY_DATA_SOURCE))
        if gdf.crs is None:
            gdf = gdf.set_crs(crs="EPSG:4326")
        elif gdf.crs.to_string() != "EPSG:4326":
            gdf = gdf.to_crs(crs="EPSG:4326")
        return gdf


    # ------------------------------------------------------------
    # DATA CLEANING FUNCTIONS
    # ------------------------------------------------------------
    def clean_crocodile_data(data: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """Limpiar datos brutos de ocurrencias de cocodrilos."""
        cleaned = data.dropna(subset=["species", "decimalLatitude", "decimalLongitude"]).copy()
        cleaned.rename(columns={"species": "Especie"}, inplace=True)
        return cleaned


    @st.cache_data(show_spinner=False)
    def load_and_clean_data() -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
        """Cargar y limpiar datos de cocodrilos (cached).

        Returns:
            Tupla con (datos_limpios, datos_sin_limpiar).
        """
        raw_data = load_crocodiles_data()
        cleaned_data = clean_crocodile_data(data=raw_data)
        return cleaned_data, raw_data


    @st.cache_data(show_spinner=False)
    def get_species_options(_data: gpd.GeoDataFrame) -> list[str]:
        """Obtener lista única de especies (cached, con underscore para evitar hashing)."""
        return sorted(_data["Especie"].unique().tolist())


    # ------------------------------------------------------------
    # MAIN APP LOGIC
    # ------------------------------------------------------------
    def main() -> None:
        """Aplicación principal con diseño académico profesional."""
        
        # Renderizar header
        render_header()

        # Cargar datos
        with st.spinner("Cargando datos..."):
            data, raw_data = load_and_clean_data()
            countries = load_country_data()

        # Sidebar con filtros
        with st.sidebar:
            st.markdown(f"### {SIDEBAR_FILTERS_TITLE}")

            species_options = get_species_options(_data=data)
            selected_species = st.multiselect(
                label=FILTER_SPECIES_LABEL,
                options=species_options,
                help=FILTER_SPECIES_HELP,
            )

            top_n = st.slider(
                label=FILTER_TOP_N_LABEL,
                min_value=5,
                max_value=20,
                value=10,
                help=FILTER_TOP_N_HELP,
            )

        # Aplicar filtros
        filtered_data = data[data["Especie"].isin(selected_species)] if selected_species else data

        # Validar datos
        if len(filtered_data) == 0:
            render_empty_state(
                title="Sin datos",
                message=MSG_NO_DATA,
            )
            return

        # Dashboard de métricas
        render_metrics_dashboard(
            data=filtered_data,
            raw_data=raw_data,
            country_data=countries,
        )

        # Tabs principales
        tab1, tab2, tab3, tab4 = st.tabs(
            [
                TAB_OVERVIEW,
                TAB_DISTRIBUTION,
                TAB_ANALYTICS,
                TAB_DATA_TABLE,
            ],
        )

        with tab1:
            render_section_header(
                title=OVERVIEW_TITLE,
                description=OVERVIEW_DESCRIPTION,
            )

            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    label="Total de Registros",
                    value=f"{len(filtered_data):,}",
                )
            with col2:
                st.metric(
                    label="Especies Únicas",
                    value=filtered_data["Especie"].nunique(),
                )

        with tab2:
            render_section_header(
                title=DISTRIBUTION_POINTS_TITLE,
                description=DISTRIBUTION_POINTS_DESCRIPTION,
            )
            render_point_map(data=filtered_data)

            st.markdown("---")

            render_section_header(
                title=DISTRIBUTION_CHOROPLETH_TITLE,
                description=DISTRIBUTION_CHOROPLETH_DESCRIPTION,
            )
            render_choropleth_map(
                data=filtered_data,
                country_data=countries,
            )

        with tab3:
            render_section_header(
                title=ANALYTICS_TOP_SPECIES_TITLE,
                description=ANALYTICS_TOP_SPECIES_DESCRIPTION,
            )
            create_top_species_chart(
                data=filtered_data,
                top_n=top_n,
            )

        with tab4:
            render_section_header(
                title=TABLE_TITLE,
                description=TABLE_DESCRIPTION,
            )

            num_records = st.slider(
                label=TABLE_RECORDS_LABEL,
                min_value=10,
                max_value=1000,
                value=100,
                step=10,
            )

            display_data = filtered_data.drop(columns=["geometry"]).head(num_records)
            st.dataframe(
                data=display_data,
                hide_index=True,
                width="stretch",
            )

        # Footer
        render_footer()

except Exception as e:
    print(f"Failed to initialize the application: {e}")

# ------------------------------------------------------------
# RUN APP
# ------------------------------------------------------------
if __name__ == "__main__":
    main()
