# Análisis Exploratorio de Datos - Plataforma Educativa

## Descripción del Proyecto

Este proyecto realiza un **análisis exploratorio de datos (EDA)** completo sobre los registros de acceso de docentes a una plataforma educativa durante el período de **agosto a diciembre de 2024**.

El objetivo principal es identificar patrones de uso, comportamientos de docentes por departamento, tendencias temporales y niveles de actividad en la plataforma.

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

## Proceso de Análisis

### 1. Carga y Exploración Inicial
```python
df = pd.read_csv('loggedin_2024_2_docentes.csv')
df.info()
df.shape
df.head()
```

**Hallazgos iniciales:**
- 22,529 registros totales
- 7 columnas
- 331 valores nulos en la columna `department`
- 0 filas duplicadas

### 2. Limpieza de Datos

**Acciones realizadas:**

- Eliminación de 331 registros con valores nulos en `department`
- Eliminación de duplicados (0 encontrados)
- Conversión de `timecreated` de timestamp Unix a formato datetime
- Extracción de características temporales: fecha, hora, día de la semana, mes

**Resultado final:** 22,198 registros limpios

### 3. Transformación de Datos

Se crearon nuevas columnas a partir de `timecreated`:

```python
df['datetime'] = pd.to_datetime(df['timecreated'], unit='s')
df['date'] = df['datetime'].dt.date
df['time'] = df['datetime'].dt.time
df['day_of_week'] = df['datetime'].dt.day_name()
df['month'] = df['datetime'].dt.month_name()
```

---

## 📊 Resultados del Análisis

### Estadísticas Generales

| Métrica | Valor |
|---------|-------|
| Promedio de ingresos por docente | 36.81 |
| Mediana de ingresos | 24 |
| Docente más activo | 655 ingresos |
| Docente menos activo | 1 ingreso |
| Día con más ingresos | Martes (4,053) |
| Día con menos ingresos | Domingo (1,537) |
| Mes más activo | Octubre (6,256 ingresos) |

### Clasificación de Docentes por Actividad

| Categoría | Cantidad | Porcentaje |
|-----------|----------|-----------|
| Muy Activos (75-100%) | 152 | 25.2% |
| Activos (50-75%) | 158 | 26.2% |
| Moderados (25-50%) | 148 | 24.5% |
| Poco Activos (0-25%) | 145 | 24.0% |

### Top 5 Departamentos

| Departamento | Ingresos | Docentes |
|--------------|----------|----------|
| Salud Pública | 2,819 | 31 |
| Informática Educativa | 2,687 | 31 |
| Ciencias Administrativas | 2,319 | 42 |
| Idiomas Extranjeros | 1,590 | 63 |
| Ingeniería de Sistemas y Telecomunicaciones | 1,284 | 33 |

### Análisis Temporal

**Por Día de la Semana:**
- Lunes: 3,519 ingresos
- Martes: 4,053 ingresos ⭐ (máximo)
- Miércoles: 3,888 ingresos
- Jueves: 3,496 ingresos
- Viernes: 3,282 ingresos
- Sábado: 2,423 ingresos
- Domingo: 1,537 ingresos ❌ (mínimo)

**Por Mes:**
- Agosto: 1,985 ingresos
- Septiembre: 5,310 ingresos
- Octubre: 6,256 ingresos ⭐ (máximo)
- Noviembre: 5,800 ingresos
- Diciembre: 2,847 ingresos

### Interpretación de "Ingresos"

**Importante:** En este análisis, el término **"ingresos"** se refiere al número de veces que un docente accedió a la plataforma, no a dinero.

- Cada fila en el dataset representa un evento de login
- El evento es siempre `user_loggedin` (usuario que ingresa)
- Se contabiliza desde agosto 12 hasta diciembre 21 de 2024

---

## Visualizaciones Generadas

### Gráfico 1: Top 15 Departamentos
Muestra los departamentos con mayor cantidad de ingresos de docentes. Departamento de Salud Pública lidera con 2,819 accesos.

### Gráfico 2: Top 20 Docentes
Identifica los docentes más activos en la plataforma. El docente más activo registró 655 ingresos.

### Gráfico 3: Ingresos por Día de la Semana
Distribución de accesos a lo largo de la semana. Se observa que los días laborales tienen mayor actividad que los fines de semana.

### Gráfico 4: Tendencia de Ingresos por Mes
Muestra la evolución temporal. Se observa un pico en octubre con ligera disminución en diciembre (período vacacional).

### Gráfico 5: Distribución de Actividad
Boxplot que visualiza la distribución de ingresos entre docentes, mostrando outliers y la mediana.

### Gráfico 6: Clasificación de Docentes
Gráfico de pastel que divide a los docentes en 4 categorías según su nivel de actividad.

### Gráfico 7: Tendencia Temporal
Gráfico de línea que muestra los ingresos día a día, permitiendo identificar patrones y picos de actividad.

---

## Tecnologías Utilizadas

- **Python 3.x**
- **Pandas:** Manipulación y análisis de datos
- **Matplotlib:** Visualización de gráficos
- **Seaborn:** Visualización estadística avanzada
- **JupyterLab:** Entorno de desarrollo interactivo

---

## Estructura del Código

### 1. Importación de Librerías
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
```

### 2. Carga de Datos
```python
df = pd.read_csv('loggedin_2024_2_docentes.csv')
```

### 3. Exploración Inicial
- Ver estructura y tipo de datos
- Identificar valores nulos
- Detectar duplicados

### 4. Limpieza de Datos
- Eliminar registros con valores nulos
- Convertir tipos de datos
- Crear nuevas características

### 5. Análisis Exploratorio
- Estadísticas descriptivas
- Agrupación por departamento
- Análisis temporal
- Clasificación de docentes

### 6. Visualización
- 7 gráficos diferentes
- Diferentes tipos: barras, líneas, boxplot, pastel

---

## Hallazgos Clave

### Fortalezas Observadas

1. **Distribución equilibrada de actividad:** Los 4 grupos de actividad tienen porcentajes similares (~25% cada uno)
2. **Actividad consistente:** Promedio de 36.81 ingresos por docente indica uso regular
3. **Mejor actividad entre semana:** Martes es el día más activo, coherente con actividades académicas
4. **Octubre como mes pico:** Coincide con el período académico activo

### Áreas de Atención

1. **Baja actividad en fines de semana:** Domingo tiene solo 1,537 ingresos vs 4,053 del martes
2. **Reducción en diciembre:** Posiblemente por vacaciones
3. **Variabilidad entre docentes:** Rango de 1 a 655 ingresos (gran dispersión)
4. **Docentes poco activos:** 24% de docentes con menos de 8 ingresos

---

## Conclusiones

Este análisis exploratorio revela patrones importantes sobre cómo los docentes utilizan la plataforma educativa:

- La plataforma es utilizada de manera **relativamente activa** durante el período académico
- Existe una **correlación clara entre días de semana y actividad**, con picos entre semana
- El **departamento de Salud Pública** lidera en cantidad de accesos
- La **distribución de actividad es heterogénea**, con algunos docentes muy activos y otros con uso mínimo
- El período **octubre-noviembre** fue el más activo

Estos hallazgos pueden ser útiles para:
- Optimizar el diseño de la plataforma
- Identificar docentes que necesitan capacitación
- Planificar mantenimiento en períodos de baja actividad
- Mejorar la experiencia de usuario

---

## Cómo Usar Este Proyecto

### Requisitos
```bash
pip install pandas matplotlib seaborn numpy
```

### Pasos para Ejecutar

1. **Abre JupyterLab**
   ```bash
   jupyter lab
   ```

2. **Sube el archivo CSV**
   - Usa el botón "Upload Files" en la carpeta de la izquierda

3. **Copia el código de exploración**
   - Copia cada bloque de código en celdas separadas
   - Presiona Shift + Enter para ejecutar

4. **Genera los gráficos**
   - Ejecuta el código de visualización
   - Los gráficos aparecerán debajo de cada celda

5. **Exporta los resultados**
   - Los gráficos se pueden guardar como PNG o PDF

---

## Contacto

Para consultas sobre este análisis, contacta a los integrantes del equipo.

---

## Licencia

Este proyecto fue realizado como parte del **Diplomado en Aprendizaje Automático - Módulo 1** en la Universidad de Córdoba.

**Fecha:** 2025
**Institución:** Universidad de Córdoba - Facultad de Ingeniería