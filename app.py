import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página del dashboard
st.set_page_config(page_title="Dashboard de Admisiones Universitarias", layout="wide")

# Cargar los datos directamente mapeados del archivo CSV de la universidad
@st.cache_data
def load_data():
    data = {
        "Year": [2015, 2015, 2016, 2016, 2017, 2017, 2018, 2018, 2019, 2019, 2020, 2020, 2021, 2021, 2022, 2022, 2023, 2023, 2024, 2024],
        "Term": ["Spring", "Fall", "Spring", "Fall", "Spring", "Fall", "Spring", "Fall", "Spring", "Fall", "Spring", "Fall", "Spring", "Fall", "Spring", "Fall", "Spring", "Fall", "Spring", "Fall"],
        "Applications": [2500, 2500, 2600, 2600, 2700, 2700, 2800, 2800, 3000, 3000, 2900, 2900, 3100, 3100, 3250, 3250, 3350, 3350, 3500, 3500],
        "Admitted": [1500, 1500, 1550, 1550, 1600, 1600, 1650, 1650, 1750, 1750, 1700, 1700, 1800, 1800, 1900, 1900, 2000, 2000, 2100, 2100],
        "Enrolled": [600, 600, 625, 625, 650, 650, 675, 675, 700, 700, 690, 690, 725, 725, 750, 750, 775, 775, 800, 800],
        "Retention Rate (%)": [85, 85, 86, 86, 87, 87, 86, 86, 88, 88, 85, 85, 87, 87, 88, 88, 89, 89, 90, 90],
        "Student Satisfaction (%)": [78, 78, 79, 79, 80, 80, 82, 82, 83, 83, 81, 81, 84, 84, 85, 85, 86, 86, 88, 88],
        "Engineering Enrolled": [200, 200, 210, 210, 225, 225, 235, 235, 250, 250, 240, 240, 260, 260, 275, 275, 285, 285, 300, 300],
        "Business Enrolled": [150, 150, 160, 160, 165, 165, 175, 175, 185, 185, 180, 180, 195, 195, 200, 200, 210, 210, 225, 225],
        "Arts Enrolled": [125, 125, 130, 130, 135, 135, 140, 140, 145, 145, 140, 140, 150, 150, 160, 160, 165, 165, 175, 175],
        "Science Enrolled": [125, 125, 125, 125, 125, 125, 125, 125, 120, 120, 130, 130, 120, 120, 115, 115, 115, 115, 100, 100]
    }
    return pd.DataFrame(data)

df = load_data()

# Encabezado principal del Dashboard
st.title("📊 Dashboard de Analítica de Estudiantes")
st.caption("Desarrollado para la Asignatura de Minería de Datos - Universidad de la Costa")
st.markdown("---")

# --- FILTROS EN LA BARRA LATERAL ---
st.sidebar.header("Filtros Interactivos")

# Filtro de Año
years = sorted(df["Year"].unique())
selected_years = st.sidebar.multiselect("Selecciona el Año", years, default=years)

# Filtro de Periodo Académico (Term)
terms = df["Term"].unique()
selected_terms = st.sidebar.multiselect("Selecciona el Periodo", terms, default=list(terms))

# Aplicar filtros al DataFrame
df_filtered = df[(df["Year"].isin(selected_years)) & (df["Term"].isin(selected_terms))]

# --- SECCIÓN DE METRICAS PRINCIPALES (KPIs) ---
st.subheader("📈 Métricas Clave (KPIs)")
col1, col2, col3, col4 = st.columns(4)

if not df_filtered.empty:
    total_apps = df_filtered["Applications"].sum()
    total_enrolled = df_filtered["Enrolled"].sum()
    avg_retention = df_filtered["Retention Rate (%)"].mean()
    avg_satisfaction = df_filtered["Student Satisfaction (%)"].mean()
    
    col1.metric("Total Aplicaciones", f"{total_apps:,}")
    col2.metric("Total Matriculados", f"{total_enrolled:,}")
    col3.metric("Retención Promedio", f"{avg_retention:.1f}%")
    col4.metric("Satisfacción Promedio", f"{avg_satisfaction:.1f}%")
else:
    st.warning("No hay datos dinámicos para mostrar con los filtros seleccionados.")

st.markdown("---")

# --- GRÁFICOS INTERACTIVOS ---
col_left, col_right = st.columns(2)

with col_left:
    # Gráfico 1: Tendencia de Retención y Satisfacción (Líneas)
    st.subheader("📅 Evolución de Retención y Satisfacción")
    if not df_filtered.empty:
        df_yearly = df_filtered.groupby("Year")[["Retention Rate (%)", "Student Satisfaction (%)"]].mean().reset_index()
        fig_line = px.line(df_yearly, x="Year", y=["Retention Rate (%)", "Student Satisfaction (%)"],
                           labels={"value": "Porcentaje (%)", "Year": "Año", "variable": "Indicador"},
                           markers=True, title="Tendencia de Indicadores Clave en el Tiempo")
        st.plotly_chart(fig_line, use_container_width=True)

with col_right:
    # Gráfico 2: Comparación de Semestres (Barras agrupadas)
    st.subheader("🍂 Spring vs Fall: Embudo de Admisiones")
    if not df_filtered.empty:
        df_term = df_filtered.groupby("Term")[["Applications", "Admitted", "Enrolled"]].sum().reset_index()
        fig_bar = px.bar(df_term, x="Term", y=["Applications", "Admitted", "Enrolled"],
                         barmode="group", title="Volumen de Admisión por Periodo",
                         labels={"value": "Cantidad", "Term": "Periodo", "variable": "Etapa"})
        st.plotly_chart(fig_bar, use_container_width=True)

# Gráfico 3: Distribución por Facultades (Donut Chart)
st.markdown("---")
st.subheader("🏫 Distribución de Matriculados por Facultad")

if not df_filtered.empty:
    dept_totals = {
        "Ingeniería": df_filtered["Engineering Enrolled"].sum(),
        "Negocios": df_filtered["Business Enrolled"].sum(),
        "Artes": df_filtered["Arts Enrolled"].sum(),
        "Ciencias": df_filtered["Science Enrolled"].sum()
    }
    df_dept = pd.DataFrame(list(dept_totals.items()), columns=["Facultad", "Matriculados"])
    
    fig_pie = px.pie(df_dept, values="Matriculados", names="Facultad", hole=0.4,
                     title="Participación de Matrículas por Departamento",
                     color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_pie, use_container_width=True)
