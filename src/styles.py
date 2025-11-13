"""Estilos CSS personalizados para la aplicación de análisis geoespacial.
Diseño académico y profesional siguiendo mejores prácticas de UX.
"""


def get_custom_css() -> str:
    """Retorna el CSS personalizado para la aplicación."""
    return """
    <style>
    /* Forzar tema claro */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Reducir opacidad del overlay de rerun para mejor UX */
    .stApp > div[data-testid="stAppViewContainer"] > div[data-testid="stAppViewBlockContainer"] {
        transition: opacity 0.1s ease-in-out;
    }
    
    /* Hacer el spinner más discreto */
    div[data-testid="stStatusWidget"] {
        opacity: 0.6;
    }
    
    /* Importar fuente profesional */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Variables globales */
    :root {
        --primary-color: #2563eb;
        --secondary-color: #3b82f6;
        --accent-color: #60a5fa;
        --text-primary: #374151;
        --text-secondary: #6b7280;
        --bg-light: #f8fafc;
        --bg-white: #ffffff;
        --border-color: #e2e8f0;
        --success-color: #10b981;
        --warning-color: #f59e0b;
    }

    /* Fuente base */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
        color: white;
        padding: 2rem 2rem 1.5rem 2rem;
        border-radius: 0.75rem;
        margin-bottom: 2rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }

    .main-header h1 {
        font-size: 2rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.025em;
    }

    .main-header p {
        font-size: 1rem;
        opacity: 0.95;
        margin: 0;
        font-weight: 400;
    }

    /* Tarjetas de métricas */
    .metric-card {
        background: var(--bg-white);
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid var(--border-color);
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
    }

    .metric-card:hover {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-color: var(--accent-color);
    }

    .metric-label {
        font-size: 0.875rem;
        color: var(--text-secondary);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }

    .metric-value {
        font-size: 2rem;
        color: var(--secondary-color);
        font-weight: 600;
        margin: 0;
    }

    .metric-delta {
        font-size: 0.875rem;
        color: var(--text-secondary);
        margin-top: 0.25rem;
    }

    /* Sidebar mejorado */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-white);
        border-right: 1px solid var(--border-color);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }

    .sidebar-section {
        background: var(--bg-white);
        padding: 0;
        border-radius: 0;
        margin-bottom: 0;
        border: none;
    }

    .sidebar-section h3 {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0 0 1rem 0;
        padding-bottom: 0;
        border-bottom: none;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Tabs profesionales */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: var(--bg-light);
        padding: 0.5rem;
        border-radius: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        background-color: transparent;
        border-radius: 0.375rem;
        color: var(--text-secondary);
        font-weight: 500;
        padding: 0 1.5rem;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: var(--bg-white);
        color: var(--text-primary);
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--bg-white) !important;
        color: var(--primary-color) !important;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }

    /* Contenedores de mapas */
    .map-container {
        border-radius: 0.5rem;
        overflow: hidden;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        border: 1px solid var(--border-color);
        margin: 1rem 0;
    }

    /* Tablas de datos */
    .dataframe {
        font-size: 0.875rem;
        border-collapse: collapse;
        width: 100%;
    }

    .dataframe thead th {
        background-color: var(--bg-light);
        color: var(--text-primary);
        font-weight: 600;
        padding: 0.75rem;
        text-align: left;
        border-bottom: 2px solid var(--border-color);
    }

    .dataframe tbody td {
        padding: 0.75rem;
        border-bottom: 1px solid var(--border-color);
    }

    .dataframe tbody tr:hover {
        background-color: var(--bg-light);
    }

    /* Footer profesional */
    .app-footer {
        margin-top: 4rem;
        padding: 2rem;
        background-color: var(--bg-light);
        border-top: 1px solid var(--border-color);
        border-radius: 0.5rem;
        text-align: center;
    }

    .app-footer p {
        font-size: 0.875rem;
        color: var(--text-secondary);
        margin: 0.5rem 0;
    }

    .app-footer a {
        color: var(--secondary-color);
        text-decoration: none;
        font-weight: 500;
    }

    .app-footer a:hover {
        text-decoration: underline;
    }

    /* Estados de carga */
    .loading-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem;
        color: var(--text-secondary);
    }

    .loading-state .spinner {
        border: 3px solid var(--border-color);
        border-top: 3px solid var(--secondary-color);
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* Estados vacíos */
    .empty-state {
        text-align: center;
        padding: 3rem;
        color: var(--text-secondary);
    }

    .empty-state h3 {
        font-size: 1.25rem;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }

    /* Botones personalizados */
    .stButton > button {
        background-color: var(--secondary-color);
        color: white;
        border: none;
        border-radius: 0.375rem;
        padding: 0.625rem 1.25rem;
        font-weight: 500;
        transition: background-color 0.2s;
    }

    .stButton > button:hover {
        background-color: var(--primary-color);
    }

    /* Selectbox y multiselect */
    .stSelectbox, .stMultiSelect {
        font-weight: 400;
    }

    /* Mejorar espacio vertical */
    .element-container {
        margin-bottom: 1rem;
    }

    /* Ocultar marca de agua de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Responsividad */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.5rem;
        }

        .metric-value {
            font-size: 1.5rem;
        }

        .metric-card {
            padding: 1rem;
        }
    }
    </style>
    """
