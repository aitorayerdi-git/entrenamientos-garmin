# Cómo actualizar los informes

## Informe inmediato

1. En Garmin Connect, abre **Actividades > Todas las actividades**.
2. Exporta la lista completa como CSV.
3. Guarda el archivo sin modificar en `datos garmin/inmediato`.
4. Haz doble clic en `ACTUALIZAR_INFORMES.cmd`.
5. Al terminar se abrirá `index.html`; si ya estaba abierto, recarga Chrome.

El actualizador busca automáticamente el CSV más reciente dentro de `datos garmin`, procesa sus actividades y regenera los gráficos. Los CSV originales no se modifican ni se eliminan.

## Informe detallado

1. Solicita la exportación completa en Garmin Data Management.
2. Guarda el ZIP original en `datos garmin/completo`.
3. No lo descomprimas ni modifiques.
4. Ejecutaremos el importador detallado cuando su estructura real esté disponible.

Esta actualización será menos frecuente y su fecha de cobertura se mostrará separada de la del informe inmediato.

## Por qué no hay todavía un botón web de actualización

Un HTML abierto directamente desde el disco no puede explorar carpetas ni ejecutar el importador de Python sin autorización, debido a las restricciones de seguridad del navegador.

El archivo `ACTUALIZAR_INFORMES.cmd` ofrece ahora el flujo más sencillo y fiable: guardar el CSV y hacer doble clic. Una evolución posterior puede ejecutar la web mediante un pequeño servidor local. En ese caso, el botón **Actualizar** podría buscar el CSV nuevo, validarlo, regenerar los datos y mostrar el resultado del proceso desde la propia web.

Otra alternativa sería seleccionar manualmente el CSV con un botón del navegador. Es una solución sin servidor, pero habría que seleccionar el archivo en cada actualización y la persistencia local resulta menos fiable. Por eso no es la opción recomendada para el proyecto definitivo.
