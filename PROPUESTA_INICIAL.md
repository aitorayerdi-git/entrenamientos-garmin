# Propuesta inicial del panel de entrenamientos

## Enfoque

La primera versión será una aplicación web local y adaptable a móvil y ordenador. Leerá los datos exportados de Garmin, normalizará las columnas y presentará un panel interactivo. El diseño se hará de forma que actualizar los datos no obligue a rehacer la web.

## Informe versión 1

### Resumen

- Actividades totales y días activos.
- Tiempo, distancia, desnivel positivo y calorías acumuladas.
- Promedios por sesión y por semana.
- Comparación de los últimos 7, 28 y 90 días con el periodo anterior equivalente.

### Evolución temporal

- Barras semanales de duración, distancia y carga.
- Línea mensual de volumen y frecuencia de entrenamiento.
- Calendario de actividad para detectar continuidad y descansos.

### Intensidad y rendimiento

- Distribución por deporte y por zona de frecuencia cardiaca.
- Ritmo o velocidad frente a frecuencia cardiaca.
- Evolución de ritmo, potencia, cadencia y desnivel, si Garmin los proporciona.
- Mejores registros por distancia o duración, con cautela ante actividades incompletas.

### Exploración

- Filtros por fechas, deporte y rango de duración.
- Tabla ordenable con todas las sesiones.
- Vista detallada de una actividad seleccionada.

## Flujo previsto de actualización

1. Descargar las actividades desde Garmin Connect.
2. Copiar el archivo sin modificar a la carpeta de datos del proyecto.
3. Ejecutar un importador que valide y transforme los datos.
4. Abrir o actualizar la web para ver el nuevo informe.

Cuando veamos el archivo real decidiremos si el importador leerá Excel directamente o si generará un archivo JSON/CSV optimizado para la web. Esta segunda opción suele ofrecer una experiencia más estable en una web local.

## Datos que necesitaremos comprobar

- Formato exacto de exportación: XLSX, CSV u otro.
- Nombres y unidades de las columnas.
- Deportes incluidos.
- Existencia de frecuencia cardiaca, zonas, potencia, cadencia, desnivel y carga.
- Tratamiento de valores vacíos, pausas y actividades duplicadas.
- Si el archivo contiene solo el resumen de cada actividad o también muestras durante la sesión.

## Criterios técnicos iniciales

- Todo se almacenará dentro de `entrenamientos`.
- Los archivos originales se conservarán separados de los datos procesados.
- La importación será repetible y evitará duplicados.
- La interfaz indicará la fecha de la última actualización.
- Los cálculos y definiciones de cada indicador quedarán documentados.

