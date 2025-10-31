"""
============================================
UNIVERSIDAD DE CÓRDOBA
FACULTAD DE INGENIERÍA
DASHBOARD INTERACTIVO - ANÁLISIS DE INGRESOS DOCENTES
============================================

Dashboard de análisis exploratorio de ingresos de docentes
a la plataforma educativa (Agosto - Diciembre 2024)

Autores: Jose Aviles, Valeria Perez, David Cano
Profesor: Larry Pacheco
============================================
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

# ============================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================
st.set_page_config(
    page_title="Dashboard Docentes - Universidad de Córdoba",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# ESTILOS CSS PERSONALIZADOS
# ============================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        padding: 1.5rem;
        margin-bottom: 2rem;
        border-bottom: 3px solid #3498db;
        animation: fadeIn 0.5s ease-in;
    }

    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }

    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-in;
    }

    .metric-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 12px 20px rgba(0, 0, 0, 0.3);
    }

    .info-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #3498db;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transform: scale(1.05);
    }

    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: bold;
        animation: slideIn 0.4s ease-out;
    }

    .streamlit-expanderHeader {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2c3e50;
        transition: all 0.3s ease;
    }

    .streamlit-expanderHeader:hover {
        color: #667eea;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideIn {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNCIONES AUXILIARES
# ============================================

@st.cache_data
def cargar_datos():
    """Carga y preprocesa los datos del CSV"""
    try:
        df = pd.read_csv('loggedin_2024_2_docentes.csv')

        # Eliminar registros con departamento nulo
        df = df.dropna(subset=['department'])

        # Convertir timestamp a datetime
        df['datetime'] = pd.to_datetime(df['timecreated'], unit='s')
        df['date'] = df['datetime'].dt.date
        df['time'] = df['datetime'].dt.time
        df['day_of_week'] = df['datetime'].dt.day_name()
        df['month'] = df['datetime'].dt.month_name()
        df['hour'] = df['datetime'].dt.hour
        df['day'] = df['datetime'].dt.day

        # Traducir meses a español
        meses_es = {
            'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo',
            'April': 'Abril', 'May': 'Mayo', 'June': 'Junio',
            'July': 'Julio', 'August': 'Agosto', 'September': 'Septiembre',
            'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
        }
        df['mes_es'] = df['month'].map(meses_es)

        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return None

def crear_metrica_card(titulo, valor, icono="▪"):
    """Crea una tarjeta de métrica personalizada compacta"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 8px;
        color: white;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 0.5rem;
    ">
        <div style="font-size: 0.85rem; opacity: 0.95; margin-bottom: 0.5rem; letter-spacing: 0.5px;">{icono} {titulo}</div>
        <div style="font-size: 2rem; font-weight: bold; letter-spacing: -0.5px;">{valor}</div>
    </div>
    """, unsafe_allow_html=True)

def formato_numero(num):
    """Formatea números con separadores de miles"""
    return f"{num:,}".replace(",", ".")

# ============================================
# CARGA DE DATOS
# ============================================
df = cargar_datos()

if df is None:
    st.stop()

# ============================================
# SIDEBAR - NAVEGACIÓN Y FILTROS
# ============================================
with st.sidebar:
    st.markdown("### ▸ Navegación")

    seccion = st.radio(
        "",
        ["▪ Datos Generales", "▪ Análisis General", "▪ Análisis por Programa"],
        index=0,
        label_visibility="collapsed"
    )

    st.divider()

    # Filtros globales
    st.markdown("### ▸ Filtros Globales")

    # Filtro de meses múltiple
    orden_meses = ['Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    meses_disponibles = sorted(df['mes_es'].dropna().unique(),
                               key=lambda x: orden_meses.index(x) if x in orden_meses else 999)

    filtro_meses = st.multiselect(
        "Meses",
        options=meses_disponibles,
        default=meses_disponibles,
        help="Seleccione uno o más meses"
    )

    # Filtro de programas múltiple
    if seccion != "🎓 Análisis por Programa":
        filtro_programas = st.multiselect(
            "Programas",
            options=sorted(df['department'].unique()),
            default=sorted(df['department'].unique()),
            help="Seleccione uno o más programas"
        )
    else:
        filtro_programas = sorted(df['department'].unique())

    # Aplicar filtros
    df_filtrado_global = df.copy()
    if filtro_meses:
        df_filtrado_global = df_filtrado_global[df_filtrado_global['mes_es'].isin(filtro_meses)]
    if filtro_programas:
        df_filtrado_global = df_filtrado_global[df_filtrado_global['department'].isin(filtro_programas)]

    st.divider()

    # Información compacta
    with st.expander("▸ Info del Dashboard"):
        st.markdown(f"""
        **Periodo**: Ago-Dic 2024
        **Registros**: {formato_numero(len(df_filtrado_global))}
        **Profesores**: {formato_numero(df_filtrado_global['userid'].nunique())}
        **Programas**: {formato_numero(df_filtrado_global['department'].nunique())}
        """)

    with st.expander("▸ Equipo"):
        st.markdown("""
        Jose Aviles,
        Valeria Perez,
        David Cano

        **Profesor**: Larry Pacheco
        """)

# ============================================
# HEADER PRINCIPAL
# ============================================
st.markdown('<h1 class="main-header">Dashboard de Análisis de Ingresos Docentes</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1rem; color: #7f8c8d; margin-bottom: 2rem;">Universidad de Córdoba • Plataforma Educativa 2024-2</p>', unsafe_allow_html=True)

# ============================================
# SECCIÓN 1: DATOS GENERALES
# ============================================
if seccion == "▪ Datos Generales":
    st.markdown('<h2 class="sub-header">▸ Información General del Dataset</h2>', unsafe_allow_html=True)

    # KPIs principales en columnas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        crear_metrica_card("Total Registros", formato_numero(len(df_filtrado_global)), "▪")

    with col2:
        crear_metrica_card("Profesores", formato_numero(df_filtrado_global['userid'].nunique()), "▪")

    with col3:
        crear_metrica_card("Programas", formato_numero(df_filtrado_global['department'].nunique()), "▪")

    with col4:
        promedio = df_filtrado_global.groupby('userid').size().mean()
        crear_metrica_card("Avg Ingresos", formato_numero(int(promedio)), "▪")

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs para organizar contenido
    tab1, tab2, tab3 = st.tabs(["▸ Por Programa", "▸ Por Mes", "▸ Estadísticas"])

    with tab1:
        ingresos_programa = df_filtrado_global.groupby('department').size().reset_index(name='Total Ingresos').sort_values('Total Ingresos', ascending=False)

        col1, col2 = st.columns([3, 1])

        with col1:
            # Selector de top N programas
            top_n = st.slider("Mostrar Top N programas:", 5, 27, 15, key='top_prog')

            fig_programas = go.Figure()
            fig_programas.add_trace(go.Bar(
                x=ingresos_programa.head(top_n)['Total Ingresos'],
                y=ingresos_programa.head(top_n)['department'],
                orientation='h',
                marker=dict(
                    color=ingresos_programa.head(top_n)['Total Ingresos'],
                    colorscale='Viridis',
                    showscale=False
                ),
                text=ingresos_programa.head(top_n)['Total Ingresos'],
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Ingresos: %{x}<extra></extra>'
            ))

            fig_programas.update_layout(
                title=f"Top {top_n} Programas por Ingresos",
                xaxis_title="Total de Ingresos",
                yaxis_title="",
                height=max(400, top_n * 25),
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=40, b=40)
            )

            st.plotly_chart(fig_programas, use_container_width=True, config={'displayModeBar': False})

        with col2:
            st.markdown("**Top 5 Programas**")
            for idx, row in ingresos_programa.head(5).iterrows():
                porcentaje = (row['Total Ingresos'] / ingresos_programa['Total Ingresos'].sum() * 100)
                st.metric(
                    label=f"#{list(ingresos_programa.head(5).index).index(idx) + 1}",
                    value=formato_numero(row['Total Ingresos']),
                    delta=f"{porcentaje:.1f}%"
                )

        st.markdown("<br>", unsafe_allow_html=True)

        with st.expander("▸ Ver Tabla Completa"):
            # Agregar columna de porcentaje
            ingresos_programa_tabla = ingresos_programa.copy()
            ingresos_programa_tabla['Porcentaje (%)'] = (ingresos_programa_tabla['Total Ingresos'] / ingresos_programa_tabla['Total Ingresos'].sum() * 100).round(2)

            st.dataframe(
                ingresos_programa_tabla,
                use_container_width=True,
                height=400,
                hide_index=True,
                column_config={
                    "department": st.column_config.TextColumn("Programa", width="large"),
                    "Total Ingresos": st.column_config.NumberColumn("Total Ingresos", format="%d"),
                    "Porcentaje (%)": st.column_config.ProgressColumn("Participación (%)", format="%.2f%%", min_value=0, max_value=100)
                }
            )

    with tab2:
        orden_meses = ['Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        ingresos_mes = df_filtrado_global.groupby('mes_es').size().reindex(orden_meses).fillna(0).astype(int)

        fig_meses = go.Figure()

        fig_meses.add_trace(go.Bar(
            x=ingresos_mes.index,
            y=ingresos_mes.values,
            marker=dict(
                color=ingresos_mes.values,
                colorscale='Blues',
                showscale=False,
                line=dict(color='darkblue', width=1)
            ),
            text=ingresos_mes.values,
            textposition='outside',
            name='Ingresos'
        ))

        fig_meses.add_trace(go.Scatter(
            x=ingresos_mes.index,
            y=ingresos_mes.values,
            mode='lines+markers',
            line=dict(color='red', width=2),
            marker=dict(size=8, color='red'),
            name='Tendencia'
        ))

        fig_meses.update_layout(
            title="Evolución Mensual de Ingresos",
            xaxis_title="Mes",
            yaxis_title="Total de Ingresos",
            height=400,
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=60, b=40),
            yaxis=dict(autorange=True)
        )

        st.plotly_chart(fig_meses, use_container_width=True, config={'displayModeBar': False})

        # Métricas mensuales compactas
        cols = st.columns(len([m for m in orden_meses if ingresos_mes.get(m, 0) > 0]))
        for idx, mes in enumerate([m for m in orden_meses if ingresos_mes.get(m, 0) > 0]):
            with cols[idx]:
                st.metric(
                    label=mes[:3],
                    value=formato_numero(int(ingresos_mes[mes])),
                    delta=f"{(ingresos_mes[mes]/ingresos_mes.sum()*100):.1f}%",
                    delta_color="off"
                )

    with tab3:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Fecha Inicio", str(df_filtrado_global['date'].min()))
            st.metric("Fecha Fin", str(df_filtrado_global['date'].max()))

        with col2:
            dias_totales = (pd.to_datetime(df_filtrado_global['date'].max()) - pd.to_datetime(df_filtrado_global['date'].min())).days
            st.metric("Días Totales", dias_totales)
            ingresos_diarios = df_filtrado_global.groupby('date').size()
            st.metric("Avg Ingresos/Día", f"{ingresos_diarios.mean():.0f}")

        with col3:
            st.metric("Ingreso Diario Máx", ingresos_diarios.max())
            st.metric("Ingreso Diario Mín", ingresos_diarios.min())

        with col4:
            ingresos_por_docente = df_filtrado_global.groupby('userid').size()
            st.metric("Mediana Ing/Prof", f"{ingresos_por_docente.median():.0f}")
            st.metric("Profesor Más Activo", ingresos_por_docente.max())

# ============================================
# SECCIÓN 2: ANÁLISIS GENERAL
# ============================================
elif seccion == "▪ Análisis General":
    st.markdown('<h2 class="sub-header">▸ Análisis General de la Plataforma</h2>', unsafe_allow_html=True)

    # KPIs superiores
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        crear_metrica_card("Total Ingresos", formato_numero(len(df_filtrado_global)), "▪")

    with col2:
        crear_metrica_card("Programas", formato_numero(df_filtrado_global['department'].nunique()), "▪")

    with col3:
        crear_metrica_card("Docentes", formato_numero(df_filtrado_global['userid'].nunique()), "▪")

    with col4:
        promedio = df_filtrado_global.groupby('userid').size().mean()
        crear_metrica_card("Avg/Docente", formato_numero(int(promedio)), "▪")

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs para organizar contenido
    tab1, tab2, tab3, tab4 = st.tabs(["▸ Top Programas", "▸ Análisis Temporal", "▸ Top Profesores", "▸ Horarios"])

    with tab1:
        col1, col2 = st.columns([3, 1])

        with col1:
            top_n_prog = st.slider("Mostrar Top N:", 5, 20, 10, key='top_prog_g')
            top_programas = df_filtrado_global.groupby('department').size().reset_index(name='Ingresos').sort_values('Ingresos', ascending=False).head(top_n_prog)

            fig_top = px.bar(
                top_programas.sort_values('Ingresos'),
                x='Ingresos',
                y='department',
                orientation='h',
                color='Ingresos',
                color_continuous_scale='Viridis',
                text='Ingresos'
            )

            fig_top.update_traces(textposition='outside')
            fig_top.update_layout(
                title=f"Top {top_n_prog} Programas",
                yaxis_title="",
                xaxis_title="Total de Ingresos",
                height=max(400, top_n_prog * 30),
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=40, b=40)
            )

            st.plotly_chart(fig_top, use_container_width=True, config={'displayModeBar': False})

        with col2:
            st.markdown("**Top 5**")
            for idx, row in top_programas.head(5).iterrows():
                st.metric(
                    label=f"#{list(top_programas.head(5).index).index(idx) + 1}",
                    value=formato_numero(row['Ingresos']),
                    delta=f"{(row['Ingresos']/top_programas['Ingresos'].sum()*100):.1f}%"
                )

    with tab2:
        # Selector de mes compacto
        orden_meses_es = ['Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        mes_seleccionado = st.select_slider(
            "Seleccione un mes:",
            options=['Todos'] + sorted(df_filtrado_global['mes_es'].unique(),
                                      key=lambda x: orden_meses_es.index(x) if x in orden_meses_es else 999)
        )

        # Filtrar datos según mes
        if mes_seleccionado == 'Todos':
            df_temp = df_filtrado_global
        else:
            df_temp = df_filtrado_global[df_filtrado_global['mes_es'] == mes_seleccionado]

        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            total_mes = len(df_temp)
            porcentaje = (total_mes / len(df_filtrado_global) * 100) if mes_seleccionado != 'Todos' else 100
            st.metric("Total Ingresos", formato_numero(total_mes), delta=f"{porcentaje:.1f}%")

            docentes_mes = df_temp['userid'].nunique()
            st.metric("Docentes Activos", formato_numero(docentes_mes))

        with col2:
            # Ingresos por día
            ingresos_dia_mes = df_temp.groupby('day').size().reset_index(name='Ingresos').sort_values('day')

            fig_dia = go.Figure()
            fig_dia.add_trace(go.Scatter(
                x=ingresos_dia_mes['day'],
                y=ingresos_dia_mes['Ingresos'],
                mode='lines+markers',
                fill='tozeroy',
                line=dict(color='#667eea', width=2),
                marker=dict(size=6, color='#764ba2'),
                hovertemplate='<b>Día %{x}</b><br>Ingresos: %{y}<extra></extra>'
            ))

            fig_dia.update_layout(
                title=f"Ingresos por Día - {mes_seleccionado}",
                xaxis_title="Día",
                yaxis_title="Ingresos",
                height=300,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=40, b=40)
            )

            st.plotly_chart(fig_dia, use_container_width=True, config={'displayModeBar': False})

        with col3:
            st.markdown("**Top 10 Profesores**")
            top_docentes_mes = df_temp.groupby('userid').size().reset_index(name='Ingresos').sort_values('Ingresos', ascending=False).head(10)

            with st.expander("▸ Ver Top 10"):
                for idx, row in top_docentes_mes.iterrows():
                    st.text(f"#{list(top_docentes_mes.index).index(idx) + 1}: {row['Ingresos']} ingresos")

        st.markdown("<br>", unsafe_allow_html=True)

    with tab3:
        top_n_prof = st.slider("Mostrar Top N profesores:", 10, 100, 50, step=10, key='top_prof')

        top_profesores = df_filtrado_global.groupby('userid').size().reset_index(name='Total Ingresos').sort_values('Total Ingresos', ascending=False).head(top_n_prof)
        top_profesores['Ranking'] = range(1, len(top_profesores) + 1)

        col1, col2 = st.columns([3, 1])

        with col1:
            fig_prof = px.scatter(
                top_profesores,
                x='Ranking',
                y='Total Ingresos',
                size='Total Ingresos',
                color='Total Ingresos',
                color_continuous_scale='Viridis',
                title=f'Top {top_n_prof} Profesores Más Activos'
            )

            fig_prof.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=40, b=40)
            )

            st.plotly_chart(fig_prof, use_container_width=True, config={'displayModeBar': False})

        with col2:
            st.markdown("**Top 5 Profesores**")
            for idx, row in top_profesores.head(5).iterrows():
                st.metric(
                    label=f"Prof #{row['Ranking']}",
                    value=formato_numero(row['Total Ingresos'])
                )

        st.markdown("<br>", unsafe_allow_html=True)

        with st.expander(f"▸ Ver Lista Completa Top {top_n_prof}"):
            top_profesores['ID'] = top_profesores['userid'].apply(lambda x: f"{x[:15]}...")
            top_profesores['Porcentaje (%)'] = (top_profesores['Total Ingresos'] / top_profesores['Total Ingresos'].sum() * 100).round(2)

            st.dataframe(
                top_profesores[['Ranking', 'ID', 'Total Ingresos', 'Porcentaje (%)']],
                use_container_width=True,
                height=400,
                hide_index=True,
                column_config={
                    "Ranking": st.column_config.NumberColumn("Rank", format="#%d", width="small"),
                    "ID": st.column_config.TextColumn("ID Profesor", width="medium"),
                    "Total Ingresos": st.column_config.NumberColumn("Ingresos", format="%d", width="medium"),
                    "Porcentaje (%)": st.column_config.ProgressColumn("Participación (%)", format="%.2f%%", min_value=0, max_value=max(top_profesores['Porcentaje (%)']))
                }
            )

    with tab4:
        mes_hora = st.selectbox(
            "Mes para análisis horario:",
            ['Todos'] + sorted(df_filtrado_global['mes_es'].unique(),
                              key=lambda x: orden_meses_es.index(x) if x in orden_meses_es else 999),
            key='mes_hora'
        )

        df_hora = df_filtrado_global if mes_hora == 'Todos' else df_filtrado_global[df_filtrado_global['mes_es'] == mes_hora]

        ingresos_hora = df_hora.groupby('hour').size().reset_index(name='Ingresos')

        # Crear colores según intensidad
        colores = ['#e74c3c' if h < 6 or h > 22 else '#f39c12' if h < 9 or h > 18 else '#2ecc71'
                   for h in ingresos_hora['hour']]

        fig_hora = go.Figure()
        fig_hora.add_trace(go.Bar(
            x=ingresos_hora['hour'],
            y=ingresos_hora['Ingresos'],
            marker=dict(color=colores, line=dict(color='black', width=1)),
            text=ingresos_hora['Ingresos'],
            textposition='outside',
            hovertemplate='<b>Hora: %{x}:00</b><br>Ingresos: %{y}<extra></extra>'
        ))

        fig_hora.update_layout(
            title=f"Distribución Horaria - {mes_hora}",
            xaxis_title="Hora del Día",
            yaxis_title="Total de Ingresos",
            height=400,
            xaxis=dict(tickmode='linear', tick0=0, dtick=2),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=40, b=40),
            showlegend=False
        )

        st.plotly_chart(fig_hora, use_container_width=True, config={'displayModeBar': False})

        st.markdown("<br>", unsafe_allow_html=True)

        # Leyenda compacta
        col1, col2, col3 = st.columns(3)
        with col1:
            st.success("▪ Activo (9-18h)")
        with col2:
            st.warning("▪ Moderado (6-9h, 18-22h)")
        with col3:
            st.error("▪ Bajo (22-6h)")

# ============================================
# SECCIÓN 3: ANÁLISIS POR PROGRAMA
# ============================================
elif seccion == "▪ Análisis por Programa":
    st.markdown('<h2 class="sub-header">▸ Análisis Detallado por Programa</h2>', unsafe_allow_html=True)

    # Selector de programa
    col1, col2 = st.columns([3, 1])
    with col1:
        programas = sorted(df_filtrado_global['department'].unique())
        programa_seleccionado = st.selectbox("Seleccione un programa:", programas, label_visibility="collapsed")

    with col2:
        st.metric("Total Programas", len(programas))

    st.markdown("<br>", unsafe_allow_html=True)

    # Filtrar datos del programa
    df_programa = df_filtrado_global[df_filtrado_global['department'] == programa_seleccionado]

    # KPIs del programa
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        crear_metrica_card("Registros", formato_numero(len(df_programa)), "▪")

    with col2:
        docentes_programa = df_programa['userid'].nunique()
        crear_metrica_card("Docentes", formato_numero(docentes_programa), "▪")

    with col3:
        promedio_programa = df_programa.groupby('userid').size().mean()
        crear_metrica_card("Avg", formato_numero(int(promedio_programa)), "▪")

    with col4:
        participacion = (len(df_programa) / len(df_filtrado_global) * 100)
        crear_metrica_card("Participación", f"{participacion:.1f}%", "▪")

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs para organizar contenido
    tab1, tab2, tab3, tab4 = st.tabs(["▸ Profesores", "▸ Ingresos por Mes", "▸ Análisis Temporal", "▸ Dispersión"])

    with tab1:
        ingresos_profesores = df_programa.groupby('userid').size().reset_index(name='Total Ingresos').sort_values('Total Ingresos', ascending=False)
        ingresos_profesores['Ranking'] = range(1, len(ingresos_profesores) + 1)

        col1, col2 = st.columns([2, 1])

        with col1:
            fig_prof = go.Figure()

            fig_prof.add_trace(go.Bar(
                x=ingresos_profesores['Ranking'],
                y=ingresos_profesores['Total Ingresos'],
                marker=dict(
                    color=ingresos_profesores['Total Ingresos'],
                    colorscale='Viridis',
                    showscale=False
                ),
                hovertemplate='<b>Profesor #%{x}</b><br>Ingresos: %{y}<extra></extra>'
            ))

            fig_prof.update_layout(
                title="Ranking de Profesores por Ingresos",
                xaxis_title="Ranking",
                yaxis_title="Total de Ingresos",
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=40, b=40)
            )

            st.plotly_chart(fig_prof, use_container_width=True, config={'displayModeBar': False})

        with col2:
            st.markdown("**Top 5 Profesores**")
            for idx, row in ingresos_profesores.head(5).iterrows():
                st.metric(
                    label=f"Prof #{row['Ranking']}",
                    value=formato_numero(row['Total Ingresos'])
                )

        st.markdown("<br>", unsafe_allow_html=True)

        with st.expander("▸ Ver Lista Completa de Profesores"):
            ingresos_profesores['ID'] = ingresos_profesores['userid'].apply(lambda x: f"{x[:15]}...")
            ingresos_profesores['Porcentaje (%)'] = (ingresos_profesores['Total Ingresos'] / ingresos_profesores['Total Ingresos'].sum() * 100).round(2)

            st.dataframe(
                ingresos_profesores[['Ranking', 'ID', 'Total Ingresos', 'Porcentaje (%)']],
                use_container_width=True,
                height=400,
                hide_index=True,
                column_config={
                    "Ranking": st.column_config.NumberColumn("Rank", format="#%d", width="small"),
                    "ID": st.column_config.TextColumn("ID Profesor", width="medium"),
                    "Total Ingresos": st.column_config.NumberColumn("Ingresos", format="%d", width="medium"),
                    "Porcentaje (%)": st.column_config.ProgressColumn("Participación (%)", format="%.2f%%", min_value=0, max_value=max(ingresos_profesores['Porcentaje (%)']))
                }
            )

    with tab2:
        # Crear pivot table
        ingresos_prof_mes = df_programa.groupby(['userid', 'mes_es']).size().reset_index(name='Ingresos')

        # Ordenar meses correctamente
        orden_meses = ['Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        ingresos_prof_mes['mes_es'] = pd.Categorical(ingresos_prof_mes['mes_es'], categories=orden_meses, ordered=True)

        # Selector de top N con validación para evitar errores
        num_profesores = len(ingresos_profesores)
        max_val_heat = min(30, num_profesores)
        default_val_heat = min(15, num_profesores)
        min_val_heat = min(5, num_profesores)

        if max_val_heat > min_val_heat:
            top_n_heat = st.slider("Mostrar Top N profesores:", min_val_heat, max_val_heat, min(default_val_heat, max_val_heat), key='top_heat')
        else:
            top_n_heat = num_profesores
            st.info(f"📊 Mostrando todos los {num_profesores} profesores disponibles")

        # Top N profesores para el heatmap
        top_profs = ingresos_profesores.head(top_n_heat)['userid'].tolist()
        ingresos_prof_mes_filtrado = ingresos_prof_mes[ingresos_prof_mes['userid'].isin(top_profs)]

        pivot_data = ingresos_prof_mes_filtrado.pivot_table(
            index='userid',
            columns='mes_es',
            values='Ingresos',
            fill_value=0
        )

        # Renombrar índices
        pivot_data.index = [f"Prof. {i+1}" for i in range(len(pivot_data))]

        fig_heatmap = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale='Viridis',
            text=pivot_data.values,
            texttemplate='%{text}',
            textfont={"size": 9},
            colorbar=dict(title="Ingresos")
        ))

        fig_heatmap.update_layout(
            title=f"Mapa de Calor: Top {top_n_heat} Profesores × Mes",
            xaxis_title="Mes",
            yaxis_title="Profesor",
            height=max(400, top_n_heat * 20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=40, b=40)
        )

        st.plotly_chart(fig_heatmap, use_container_width=True, config={'displayModeBar': False})

    with tab3:
        # Selector de mes compacto
        mes_prog = st.select_slider(
            "Seleccione el mes:",
            options=['Todos'] + sorted(df_programa['mes_es'].unique(),
                                      key=lambda x: orden_meses.index(x) if x in orden_meses else 999),
            key='mes_programa'
        )

        if mes_prog == 'Todos':
            df_prog_filtrado = df_programa
        else:
            df_prog_filtrado = df_programa[df_programa['mes_es'] == mes_prog]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Ingresos",
                formato_numero(len(df_prog_filtrado)),
                delta=f"{(len(df_prog_filtrado)/len(df_programa)*100):.1f}%" if mes_prog != 'Todos' else "100%"
            )

        with col2:
            docentes_mes = df_prog_filtrado['userid'].nunique()
            st.metric("Docentes Activos", formato_numero(docentes_mes))

        with col3:
            avg_mes = df_prog_filtrado.groupby('userid').size().mean()
            st.metric("Avg/Docente", f"{avg_mes:.1f}")

        st.markdown("<br>", unsafe_allow_html=True)

        # Dos columnas para día y hora
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**▸ Por Día**")
            ingresos_dia_prog = df_prog_filtrado.groupby('day').size().reset_index(name='Ingresos')

            fig_dia_prog = px.area(
                ingresos_dia_prog.sort_values('day'),
                x='day',
                y='Ingresos',
                color_discrete_sequence=['#667eea']
            )

            fig_dia_prog.update_layout(
                xaxis_title="Día",
                yaxis_title="Ingresos",
                height=300,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=40)
            )

            st.plotly_chart(fig_dia_prog, use_container_width=True, config={'displayModeBar': False})

        with col2:
            st.markdown("**▸ Por Hora**")
            ingresos_hora_prog = df_prog_filtrado.groupby('hour').size().reset_index(name='Ingresos')

            fig_hora_prog = px.bar(
                ingresos_hora_prog,
                x='hour',
                y='Ingresos',
                color='Ingresos',
                color_continuous_scale='Turbo'
            )

            fig_hora_prog.update_layout(
                xaxis_title="Hora",
                yaxis_title="Ingresos",
                height=300,
                xaxis=dict(tickmode='linear', tick0=0, dtick=2),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=40),
                showlegend=False
            )

            st.plotly_chart(fig_hora_prog, use_container_width=True, config={'displayModeBar': False})

    with tab4:
        ingresos_por_prof = df_programa.groupby('userid').size().reset_index(name='Ingresos')

        col1, col2 = st.columns([2, 1])

        with col1:
            fig_box = go.Figure()

            fig_box.add_trace(go.Box(
                y=ingresos_por_prof['Ingresos'],
                name='Ingresos',
                boxmean='sd',
                marker=dict(color='#667eea'),
                line=dict(color='#764ba2', width=2)
            ))

            fig_box.add_trace(go.Scatter(
                y=ingresos_por_prof['Ingresos'],
                mode='markers',
                name='Profesores',
                marker=dict(
                    size=6,
                    color=ingresos_por_prof['Ingresos'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Ingresos")
                ),
                x=[0.5] * len(ingresos_por_prof)
            ))

            fig_box.update_layout(
                title="Boxplot con Dispersión de Ingresos",
                yaxis_title="Total de Ingresos",
                height=500,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=40, b=40)
            )

            st.plotly_chart(fig_box, use_container_width=True, config={'displayModeBar': False})

        with col2:
            st.markdown("**▸ Estadísticas**")

            q1 = ingresos_por_prof['Ingresos'].quantile(0.25)
            q2 = ingresos_por_prof['Ingresos'].quantile(0.50)
            q3 = ingresos_por_prof['Ingresos'].quantile(0.75)
            iqr = q3 - q1

            st.metric("Mínimo", formato_numero(int(ingresos_por_prof['Ingresos'].min())))
            st.metric("Q1", formato_numero(int(q1)))
            st.metric("Mediana", formato_numero(int(q2)))
            st.metric("Q3", formato_numero(int(q3)))
            st.metric("Máximo", formato_numero(int(ingresos_por_prof['Ingresos'].max())))
            st.metric("IQR", formato_numero(int(iqr)))
            st.metric("Desv. Est.", formato_numero(int(ingresos_por_prof['Ingresos'].std())))

            # Clasificación de profesores
            muy_activos = (ingresos_por_prof['Ingresos'] >= q3).sum()
            activos = ((ingresos_por_prof['Ingresos'] >= q2) & (ingresos_por_prof['Ingresos'] < q3)).sum()
            moderados = ((ingresos_por_prof['Ingresos'] >= q1) & (ingresos_por_prof['Ingresos'] < q2)).sum()
            poco_activos = (ingresos_por_prof['Ingresos'] < q1).sum()

            st.markdown("<br>", unsafe_allow_html=True)

            with st.expander("▸ Ver Clasificación"):
                st.write(f"**Muy Activos:** {muy_activos}")
                st.write(f"**Activos:** {activos}")
                st.write(f"**Moderados:** {moderados}")
                st.write(f"**Poco Activos:** {poco_activos}")

# ============================================
# FOOTER
# ============================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.markdown("""
<div style='text-align: center; color: #95a5a6; padding: 1.5rem; font-size: 0.9rem;'>
    <p style='margin-bottom: 0.5rem;'><strong>Dashboard de Análisis de Ingresos Docentes</strong></p>
    <p style='margin-bottom: 0.5rem;'>Universidad de Córdoba • Diplomado en Aprendizaje Automático</p>
    <p style='margin-bottom: 0.5rem;'>Desarrollado por: Jose Aviles, Valeria Perez, David Cano</p>
    <p style='margin-bottom: 0;'>Profesor: Larry Pacheco • 2025</p>
</div>
""", unsafe_allow_html=True)
