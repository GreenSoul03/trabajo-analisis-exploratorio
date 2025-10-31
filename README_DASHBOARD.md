# Dashboard Interactivo de Análisis de Ingresos Docentes

## Descripción del Proyecto

Este proyecto presenta un **dashboard interactivo** desarrollado con Streamlit para el análisis exploratorio de datos (EDA) sobre los registros de acceso de docentes a la plataforma educativa de la Universidad de Córdoba durante el período de **agosto a diciembre de 2024**.

El dashboard permite explorar de forma visual e interactiva los patrones de uso, comportamientos de docentes por departamento, tendencias temporales y niveles de actividad en la plataforma.

---

## Integrantes

- **Jose Aviles**
- **Valeria Perez**
- **David Cano**

### Profesor
**Larry Pacheco**

### Programa Académico
**Diplomado en Aprendizaje Automático - Módulo 1**

### Institución
**Universidad de Córdoba** - Facultad de Ingeniería - Ingeniería de Sistemas

---

## Conjunto de Datos

### Información General
- **Archivo:** `loggedin_2024_2_docentes.csv`
- **Total de registros:** 22,529 (antes de limpieza) → 22,198 (después de limpieza)
- **Período:** 12 de agosto - 21 de diciembre de 2024
- **Docentes únicos:** 603
- **Departamentos:** 27

### Columnas del Dataset

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `logid` | int64 | ID único del registro de acceso |
| `eventname` | object | Tipo de evento (siempre `\core\event\user_loggedin`) |
| `timecreated` | int64 | Timestamp Unix del acceso |
| `origin` | object | Origen del acceso (web, mobile, cli) |
| `userid` | object | ID único del docente |
| `department` | object | Departamento al que pertenece el docente |
| `roleteacher` | object | Rol del usuario (siempre `editingteacher`) |

---

## Características Principales del Dashboard

###  Sección 1: Datos Generales
- **KPIs principales** en tarjetas destacadas con gradientes dinámicos
- **Filtros globales** en sidebar (multiselect de meses y programas)
- **Navegación por tabs**:
  -  **Por Programa**: Gráfico interactivo + tabla con gradientes
  -  **Por Mes**: Tendencias temporales + métricas
  -  **Estadísticas**: Estadísticas descriptivas completas

###  Sección 2: Análisis General
Organizada en **4 tabs** para reducir scroll:

1. **Top Programas**
   - Slider dinámico para seleccionar cantidad (5-27 programas)
   - Gráfico de barras horizontal con gradientes por intensidad
   - Tabla completa colapsable en expander

2. **Análisis Temporal**
   - Select slider para navegar entre meses
   - Gráfico de área con tendencia diaria
   - Distribución por día de la semana
   - Código de colores por hora del día

3. **Top Profesores**
   - Slider para seleccionar top N profesores (10-100)
   - Gráfico de dispersión interactivo
   - Clasificación por cuartiles (Muy Activos, Activos, Moderados, Poco Activos)
   - Top 10 del mes seleccionado en expander

4. **Horarios**
   - Mapa de calor de ingresos por hora
   - Código de colores según intensidad:
     - 🟢 Verde: Horario activo (9:00-18:00)
     - 🟠 Naranja: Horario moderado (6:00-9:00, 18:00-22:00)
     - 🔴 Rojo: Horario bajo (22:00-6:00)

###  Sección 3: Análisis por Programa Seleccionado
Análisis detallado de un programa específico con **4 tabs**:

1. **Profesores**
   - Ranking de profesores del programa
   - Gráfico de barras con gradientes
   - Tabla completa en expander

2. **Ingresos por Mes**
   - Gráfico de barras con tendencia
   - Métricas mensuales
   - Comparativa entre meses

3. **Análisis Temporal**
   - Select slider para navegar entre meses
   - Ingresos por día del mes
   - Distribución horaria

4. **Dispersión**
   - Boxplot interactivo con puntos individuales
   - Estadísticas completas (Q1, Q2, Q3, IQR, desviación estándar)
   - Identificación de outliers

---

## Instalación y Ejecución

### Requisitos Previos

El dashboard requiere las siguientes dependencias:

```bash
pip install streamlit pandas plotly numpy matplotlib
```

**Dependencias instaladas:**
-  **streamlit**: Framework del dashboard
-  **pandas**: Manipulación de datos
-  **plotly**: Visualizaciones interactivas
-  **numpy**: Cálculos numéricos
-  **matplotlib**: Para background_gradient en tablas

### Ejecutar el Dashboard

```bash
# Desde el directorio del proyecto
streamlit run dashboard_docentes.py
```

El dashboard se abrirá automáticamente en tu navegador predeterminado en `http://localhost:8501`

---

## Componentes Avanzados de Streamlit Implementados

### 1. **Multiselect** (Filtros Globales en Sidebar)
```python
st.multiselect("Meses", options=meses_disponibles, default=meses_disponibles)
st.multiselect("Programas", options=programas, default=programas)
```
**Beneficio**: Permite filtrar múltiples meses y programas simultáneamente

### 2. **Tabs** (Organización del Contenido)
- **Sección 1 (Datos Generales)**: 3 tabs
- **Sección 2 (Análisis General)**: 4 tabs
- **Sección 3 (Análisis por Programa)**: 4 tabs

**Beneficio**: Reduce significativamente el scroll vertical y organiza el contenido lógicamente

### 3. **Sliders** (Control Dinámico)
```python
st.slider("Mostrar Top N programas:", 5, 27, 15)
st.slider("Mostrar Top N profesores:", 10, 100, 50, step=10)
st.slider("Mostrar Top N profesores:", 5, 30, 15) # Para heatmap
```
**Beneficio**: Permite al usuario controlar cuánta información ver sin recargar

### 4. **Select Slider** (Navegación Temporal)
```python
st.select_slider("Seleccione un mes:", options=['Todos'] + meses)
```
**Beneficio**: Interfaz intuitiva para navegar entre meses cronológicamente

### 5. **Expanders** (Contenido Colapsable)
```python
with st.expander(" Ver Tabla Completa"):
    st.dataframe(...)

with st.expander(" Ver Top 100"):
    st.dataframe(...)

with st.expander(" Ver Clasificación"):
    st.write(...)
```
**Beneficio**: Oculta información secundaria, reduciendo el desorden visual

### 6. **Dividers** (Separadores Visuales)
```python
st.divider()  # Reemplaza st.markdown("---")
```
**Beneficio**: Sintaxis más limpia y semántica

### 7. **Label Visibility** (Selectbox Sin Etiqueta)
```python
st.selectbox("...", programas, label_visibility="collapsed")
```
**Beneficio**: Reduce espacio vertical eliminando etiquetas redundantes

### 8. **Containers con Context Manager** (Sidebar Organizado)
```python
with st.sidebar:
    st.markdown("###  Navegación")
    seccion = st.radio(...)

    with st.expander(" Info del Dashboard"):
        st.markdown(...)
```
**Beneficio**: Código más limpio y organizado

---

## Características Innovadoras

###  Diseño Sofisticado y Compacto

**Gradientes Dinámicos:**
- Tarjetas de métricas con gradientes personalizados
- Paleta de colores moderna (Viridis, Turbo, degradados personalizados)
- Animaciones CSS con efectos hover

**Reducción de Espacios:**
- Métricas más compactas: Padding reducido de 1.5rem a 1rem
- Títulos más pequeños: Iconos de 2.5rem a 1.8rem
- Márgenes optimizados: `margin=dict(l=10, r=10, t=40, b=40)`
- Alturas dinámicas: `height=max(400, n * 25)` según cantidad de datos

**Uso Eficiente del Espacio Horizontal:**
```python
# Antes: Una columna completa
st.markdown("### Top 10 Profesores")
for profesor in top_10:
    st.metric(...)

# Después: Dos columnas compactas
col1, col2 = st.columns([3, 1])
with col1:
    # Gráfico principal
with col2:
    # Top 5 resumido
    with st.expander("Ver Top 10"):
        # Lista completa colapsada
```

###  Visualizaciones Interactivas

**Gráficos Plotly:**
- Totalmente interactivos (zoom, pan, hover)
- Mapas de calor para análisis temporal por profesor
- Boxplots con dispersión para análisis estadístico
- Gráficos de área para tendencias temporales
- Barras con gradientes según intensidad de datos

**Gráficos Más Compactos:**
```python
# Alturas reducidas y dinámicas
height=max(400, top_n * 30)  # Según cantidad de datos
height=300  # Para gráficos en columnas

# Márgenes optimizados
margin=dict(l=10, r=10, t=40, b=40)
```

**Elementos Visuales Optimizados:**
- Texto más pequeño: Font size 9-10 en heatmaps
- Colorbars sin escala: `showscale=False` cuando no es esencial
- Ticks reducidos: `dtick=2` para horas (cada 2 horas)
- Marcadores más pequeños: `size=6` en lugar de 8-10

###  Filtros Dinámicos

**Filtros Globales Inteligentes:**
- Aplicación automática a todas las secciones
- Variable `df_filtrado_global`: Dataset pre-filtrado disponible en todas las secciones
- Sin filtros en Sección 3: El programa se selecciona directamente

**Selector de mes** con actualización automática de todos los gráficos
**Selector de programa** para análisis detallado
Filtros que se aplican en cascada a todas las visualizaciones

###  Métricas Avanzadas

**Tablas con Background Gradient:**
```python
st.dataframe(
    df.style.background_gradient(cmap='Blues', subset=['Total Ingresos']),
    use_container_width=True,
    height=300  # Altura fija compacta
)
```

**Estadísticas:**
- KPIs principales en tarjetas destacadas
- Estadísticas descriptivas (Q1, Q2, Q3, IQR, desviación estándar)
- Clasificación de profesores por cuartiles
- Porcentajes de participación por programa
- Comparativas temporales entre meses

---

## Visualizaciones Incluidas

1. **Gráfico de barras horizontal** - Top programas por ingresos (con slider dinámico)
2. **Gráfico de barras con línea de tendencia** - Ingresos mensuales
3. **Gráfico de área** - Tendencia diaria
4. **Gráfico de barras coloreado** - Distribución horaria con código de colores
5. **Gráfico de dispersión** - Top profesores (con slider de cantidad)
6. **Mapa de calor (heatmap)** - Profesores × Meses
7. **Boxplot con puntos** - Dispersión de ingresos con estadísticas completas
8. **Métricas destacadas** - KPIs principales con gradientes

---

## Estructura del Dashboard

```
dashboard_docentes.py
├── Configuración de página (icono, layout, tema)
├── Estilos CSS personalizados
│   ├── Gradientes dinámicos
│   ├── Animaciones hover
│   └── Diseño compacto
├── Funciones auxiliares
│   ├── cargar_datos() - Carga y preprocesa el CSV (con caching)
│   ├── crear_metrica_card() - Tarjetas de métricas personalizadas
│   └── formato_numero() - Formateo de números
├── Sidebar de navegación
│   ├── Filtros globales (multiselect)
│   ├── Selección de sección (radio)
│   └── Información del dashboard (expander)
├── Sección 1: Datos Generales
│   ├── KPIs principales (4 columnas)
│   └── Tabs (3)
│       ├── Por Programa
│       ├── Por Mes
│       └── Estadísticas
├── Sección 2: Análisis General
│   └── Tabs (4)
│       ├── Top Programas (con slider)
│       ├── Análisis Temporal (con select slider)
│       ├── Top Profesores (con slider y clasificación)
│       └── Horarios (mapa de calor)
├── Sección 3: Análisis por Programa
│   ├── Selector de programa
│   └── Tabs (4)
│       ├── Profesores (ranking)
│       ├── Ingresos por Mes
│       ├── Análisis Temporal (con select slider)
│       └── Dispersión (boxplot con estadísticas)
└── Footer informativo
```

---

## Mejoras Implementadas

###  Estructura Mejorada

**Antes (Lineal):**
```
 Sección 1
├── KPIs
├── Gráfico grande
├── Tabla grande
├── Más gráficos
├── Más tablas
└── Estadísticas

(Scroll infinito ↓↓↓)
```

**Después (Compacta con Tabs):**
```
 Sección 1
├── KPIs (4 columnas)
└── Tabs
    ├──  Por Programa (gráfico + top 5)
    ├──  Por Mes (gráfico + métricas)
    └──  Estadísticas (4 columnas compactas)

(Navegación horizontal con tabs ↔)
```

###  Resultados Obtenidos

**Reducción de Scroll:**
- **Antes**: ~15-20 pantallas completas de scroll
- **Después**: ~3-5 pantallas con navegación por tabs
- **Reducción**: ~75% menos scroll vertical

**Información Visible:**
- **Antes**: Todo expandido, información abrumadora
- **Después**: Información principal visible, detalles en expanders
- **Mejora**: Experiencia más enfocada y profesional

**Interactividad:**
- **Antes**: Selectores básicos estáticos
- **Después**:
  - Multiselect para filtros múltiples
  - Sliders para control de cantidad de datos
  - Select sliders para navegación temporal
  - Tabs para organización
  - Expanders para detalles opcionales

**Uso del Espacio:**
- **Antes**: Mayoría de elementos a ancho completo
- **Después**:
  - Columnas [3,1] para gráfico + métricas
  - Columnas [2,1] para análisis + estadísticas
  - Columnas dinámicas según datos disponibles

###  Mejoras de Rendimiento

**Caching Optimizado:**
```python
@st.cache_data
def cargar_datos():
    # Carga datos una sola vez
    return df
```

**Cálculos Eficientes:**
```python
# Filtrado global una vez
df_filtrado_global = df.copy()
if filtro_meses:
    df_filtrado_global = df_filtrado_global[df_filtrado_global['mes_es'].isin(filtro_meses)]
```

---

## Tecnologías Utilizadas

- **Python 3.x**
- **Streamlit**: Framework del dashboard web
- **Pandas**: Manipulación y análisis de datos
- **Plotly**: Gráficos interactivos avanzados
- **Numpy**: Cálculos numéricos
- **Matplotlib**: Background gradient en tablas
- **CSS personalizado**: Estilos avanzados y animaciones

---

## Componentes Clave Utilizados

1.  `st.multiselect()` - Filtros múltiples
2.  `st.tabs()` - Organización del contenido
3.  `st.slider()` - Control de cantidad de datos
4.  `st.select_slider()` - Navegación temporal
5.  `st.expander()` - Contenido colapsable
6.  `st.divider()` - Separadores limpios
7.  `label_visibility="collapsed"` - Etiquetas ocultas
8.  `st.columns([3,1])` - Layouts eficientes
9.  `with st.sidebar:` - Context manager
10.  `.style.background_gradient()` - Tablas visuales

---

## Notas Importantes

### Interpretación de "Ingresos"

**Importante:** En este análisis, el término **"ingresos"** se refiere al número de veces que un docente accedió a la plataforma, no a dinero.

- Cada fila en el dataset representa un evento de login
- El evento es siempre `user_loggedin` (usuario que ingresa)
- Se contabiliza desde agosto 12 hasta diciembre 21 de 2024

### Consideraciones Técnicas

1. El archivo CSV debe estar en el mismo directorio que `dashboard_docentes.py`
2. Los meses se muestran en español para mejor comprensión
3. Los IDs de profesores se muestran truncados por privacidad
4. Todos los gráficos son completamente interactivos (zoom, pan, hover)
5. El dashboard se actualiza automáticamente al cambiar filtros
6. Los filtros globales del sidebar se aplican a todas las secciones
7. La carga de datos está optimizada con `@st.cache_data`

---

## Solución de Problemas

### Error: No se encuentra el archivo CSV
```bash
# Asegúrate de que loggedin_2024_2_docentes.csv está en el directorio correcto
ls loggedin_2024_2_docentes.csv
```

### Error: Módulo no encontrado
```bash
# Instala todas las dependencias
pip install streamlit pandas plotly numpy matplotlib
```

### El dashboard no se abre automáticamente
```bash
# Abre manualmente en tu navegador
http://localhost:8501
```

### Error: ImportError relacionado con matplotlib
```bash
# Reinstala matplotlib
pip install --upgrade matplotlib
```

---

## Hallazgos Clave del Dashboard

### Patrones de Actividad
- **Día más activo:** Martes (4,053 ingresos)
- **Día menos activo:** Domingo (1,537 ingresos)
- **Mes más activo:** Octubre (6,256 ingresos)
- **Departamento más activo:** Salud Pública (2,819 ingresos, 31 docentes)

### Clasificación de Docentes

| Categoría | Cantidad | Porcentaje |
|-----------|----------|-----------|
| Muy Activos (75-100%) | 152 | 25.2% |
| Activos (50-75%) | 158 | 26.2% |
| Moderados (25-50%) | 148 | 24.5% |
| Poco Activos (0-25%) | 145 | 24.0% |

### Estadísticas Generales

| Métrica | Valor |
|---------|-------|
| Promedio de ingresos por docente | 36.81 |
| Mediana de ingresos | 24 |
| Docente más activo | 655 ingresos |
| Docente menos activo | 1 ingreso |

---

## Conclusión

El dashboard ahora es:

- **Más compacto**: 75% menos scroll vertical
- **Más organizado**: Tabs y expanders para navegación eficiente
- **Más interactivo**: Sliders, multiselect y select sliders
- **Más profesional**: Diseño limpio y moderno con gradientes
- **Más eficiente**: Mejor uso del espacio horizontal
- **Más intuitivo**: Navegación clara con filtros globales
- **Más rápido**: Caching optimizado para carga de datos

El usuario puede ahora explorar los datos de forma mucho más eficiente, con control total sobre qué ver y cómo verlo, sin sentirse abrumado por la cantidad de información.

Este dashboard permite:
- Identificar patrones de uso de la plataforma
- Detectar docentes que necesitan capacitación
- Optimizar recursos según períodos de actividad
- Tomar decisiones basadas en datos

---

## Licencia

© 2025 Universidad de Córdoba - Todos los derechos reservados

Este proyecto fue realizado como parte del **Diplomado en Aprendizaje Automático - Módulo 1** en la Universidad de Córdoba.

---