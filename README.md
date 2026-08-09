 # MeteoCaracas - Sistema de Monitoreo y Consulta del Clima

## Requerimientos Funcionales Implementados

1. **Carga Inicial y Reporte de Cobertura:**
   * Carga la estructura de municipios y localidades desde el archivo `zonas_caracas.json`.
   * Genera un reporte detallado indicando por municipio: total de localidades, cantidad con coordenadas válidas, cantidad sin coordenadas conocidas y el porcentaje de cobertura con coordenadas.

2. **Consulta de Clima en Tiempo Real:**
   * **Por Navegación:** Selección jerárquica de municipio (Chacao, Baruta, El Hatillo, Sucre, Libertador) y localidad que posea coordenadas válidas[cite: 1].
   * **Por Búsqueda Directa:** Coincidencia y filtrado por nombre o fragmento del nombre de la localidad[cite: 1].
   * Muestra: Nombre de municipio y localidad, coordenadas (latitud y longitud), temperatura actual (°C), humedad relativa (%), velocidad del viento (km/h) y código/estado del tiempo[cite: 1].

3. **Reportes y Estadísticas de Sesión:**
   * **Ranking de Temperatura:** Identifica el municipio con la localidad más cálida y la más fría según las consultas realizadas en la sesión[cite: 1].
   * **Cobertura Geográfica:** Listado detallado de las localidades del archivo `zonas_caracas.json` que no poseen coordenadas registradas (`null`), agrupadas por municipio[cite: 1].
   * **Promedio General:** Promedio de temperatura de las localidades consultadas durante la sesión activa[cite: 1].

4. **Análisis e Histórico Climático:**
   * Permite seleccionar una localidad con coordenadas válidas y especificar un rango de tiempo (fecha de inicio y fecha de fin en formato `AAAA-MM-DD`)[cite: 1].
   * Consulta y procesa magnitudes meteorológicas: temperatura (°C), humedad relativa (%), precipitación acumulada (mm) y velocidad del viento (km/h)[cite: 1].
   * Muestra valores promedios de cada magnitud y determina el año más caluroso, el más fresco, el más lluvioso y el de mayor humedad relativa[cite: 1].
   * Genera una gráfica interactiva con `matplotlib` para comparar la evolución de cada magnitud en el período especificado[cite: 1].

---

##  Requisitos Técnicos y Reglas del Proyecto

* **Librerías Permitidas:** Se utilizan exclusivamente librerías autorizadas (`requests`, `matplotlib`) y módulos estándar de Python (`json`, `datetime`)[cite: 1].
* **Tolerancia a Fallos y Validaciones:** Manejo robusto de entradas en menús y fechas mediante bloques `try-except` y la librería `datetime`, previniendo errores de ejecución o fechas inválidas[cite: 1].
* **Documentación:** Todas las funciones y métodos de las clases están documentados formalmente utilizando Docstrings.
