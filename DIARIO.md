# Diario del proyecto de entrenamientos

Este documento registra cronológicamente los avances, decisiones y próximos pasos del proyecto.

## 2026-09-05

### Objetivo acordado

Crear una web HTML para consultar y analizar en detalle los entrenamientos exportados desde Garmin Connect. La solución deberá permitir incorporar nuevas exportaciones periódicamente y mantener todo el proyecto dentro de la carpeta `entrenamientos`.

### Decisiones iniciales

- Empezar con una web local, sencilla de abrir y sin necesidad de servidor.
- Diseñar primero un informe general y ampliarlo después según las necesidades reales.
- Usar como fuente inicial un archivo exportado desde Garmin Connect.
- Guardar en este diario los pasos, decisiones, pruebas y asuntos pendientes.

### Primera propuesta de informe

1. Resumen con número de actividades, tiempo, distancia, desnivel y calorías.
2. Evolución semanal y mensual del volumen de entrenamiento.
3. Distribución por tipo de actividad y zonas de frecuencia cardiaca.
4. Evolución de ritmo o velocidad, frecuencia cardiaca, potencia y cadencia cuando existan.
5. Relación entre carga, duración, intensidad y recuperación.
6. Tabla completa de sesiones con filtros y detalle de cada entrenamiento.
7. Indicadores de consistencia, mejores marcas y tendencias recientes.

### Próximo paso

Obtener una exportación representativa de Garmin Connect para conocer sus columnas, formatos y calidad. Conviene que incluya actividades variadas y, si es posible, varios meses de historial. No es necesario modificar el archivo antes de incorporarlo al proyecto.


### Nueva exportación CSV de Garmin

Se ha recibido `datos garmin/Activities (3).csv`. Contiene 1.220 actividades válidas entre el 5 de mayo de 2019 y el 5 de septiembre de 2026, distribuidas entre 16 tipos de actividad. El archivo usa UTF-8 y todas sus filas tienen 44 campos.

Cada fila está encapsulada como una única celda CSV y existen dos nombres de columna repetidos para cadencia. El importador corregirá automáticamente ambas particularidades y normalizará los decimales, millares y valores ausentes.

### Primera muestra gráfica

Se ha generado `muestra-graficos.html` con las 1.220 actividades. Los gráficos comparan de enero a diciembre los diferentes años mediante líneas de distinto color. La muestra permite filtrar por deporte y elegir horas, distancia, sesiones o desnivel como nivel de entrenamiento; y velocidad, pulso, efecto aeróbico o velocidad por pulso como aproximaciones al rendimiento.

La métrica velocidad por pulso es un indicador exploratorio de eficiencia y debe compararse dentro del mismo deporte y en condiciones similares. El panel incluye esta advertencia para evitar conclusiones incorrectas.

### Separación en dos informes

Se acuerda crear dos niveles de análisis: un informe inmediato basado en los CSV de actividades descargables al momento desde Garmin Connect, y un informe detallado basado en las exportaciones completas de Garmin Data Management. El primero podrá actualizarse con frecuencia; el segundo se actualizará de forma mensual, trimestral o cuando haya una nueva exportación completa.

La especificación de fuentes, métricas, limitaciones y estructura queda documentada en `DOS_INFORMES.md`.

### Zonas estimadas de frecuencia cardiaca media

Se añade `muestra-zonas-fc.html`. Clasifica cada actividad según su frecuencia cardiaca media y compara mensualmente el porcentaje de sesiones en Z1-Z5, con una línea por año. Las zonas usan provisionalmente una FC máxima de 206 ppm, percentil 99 de las máximas registradas, para evitar el valor extremo de 219 ppm. El gráfico advierte que no representa tiempo real en zona.

### Prototipo del informe detallado

Se crea `informe-detallado-demo.html` con datos totalmente ficticios y una advertencia visible. Permite evaluar antes de recibir Garmin Data Management las vistas de VO2 máximo, carga crónica, HRV, frecuencia cardiaca en reposo, relación carga-rendimiento y tiempo real en zonas. Mantiene la comparación anual de enero a diciembre con una línea por año.

### Página principal y actualización de informes

Se crea `index.html` como acceso a los informes inmediato y detallado. El informe inmediato integrado, `informe-inmediato.html`, reúne los gráficos generales y las zonas estimadas de frecuencia cardiaca media.

Se crea `ACTUALIZAR_INFORMES.cmd`. Al ejecutarlo, los generadores localizan el CSV más reciente dentro de `datos garmin`, regeneran ambos componentes del informe inmediato y abren la página principal. El procedimiento y sus alternativas quedan documentados en `COMO_ACTUALIZAR.md`.

### Fechas de actualización y sección de ayuda

Los encabezados del informe inmediato y del informe detallado muestran ahora la fecha de actualización de sus datos. En el inmediato la fecha se obtiene automáticamente del CSV procesado; en el prototipo detallado se identifica como fecha de datos ficticios.

Se crea la sección web `actualizar-informes.html` con procedimientos separados para la actualización frecuente y la exportación completa. Se enlaza desde la página principal y ambos informes.

### Preparación para GitHub Pages

Se decide publicar los informes para compartirlos. Se inicializa un repositorio Git local y se añaden reglas que excluyen `datos garmin` y todos los archivos CSV, XLSX, ZIP, FIT, GPX y TCX. Los HTML agregados sí se publicarán. Se crea `README.md` y se prepara GitHub Pages para servir desde la rama `main`.

### Primera publicación en GitHub

El proyecto se publica en el repositorio público `https://github.com/aitorayerdi-git/entrenamientos-garmin`. La rama principal es `main` y los archivos fuente originales de Garmin permanecen excluidos mediante `.gitignore`. Queda pendiente activar GitHub Pages desde la configuración del repositorio.

### Interacción por años y detalle mensual

El informe inmediato se amplía para mostrar simultáneamente velocidad media, frecuencia cardiaca media, eficiencia velocidad/pulso y efecto aeróbico, eliminando el selector de rendimiento. La leyenda permite activar o desactivar años mediante un clic y conserva un color estable para cada año. Los puntos muestran mes y valor al pasar el cursor, y se añade una tabla con el detalle mensual exacto.
