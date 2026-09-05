# Centro de entrenamiento Garmin

Panel web estático para consultar la evolución anual del entrenamiento y el rendimiento.

## Informes publicados

- Informe inmediato con datos reales agregados.
- Estimación de zonas basada en la frecuencia cardiaca media de cada actividad.
- Demostración del futuro informe detallado con datos ficticios.
- Comparaciones de enero a diciembre mediante una línea por año.

## Abrir localmente

Abre `index.html` con Chrome.

## Actualizar datos

1. Guarda la nueva exportación CSV en `datos garmin/inmediato`.
2. Ejecuta `ACTUALIZAR_INFORMES.cmd`.
3. Revisa los informes generados.
4. Confirma y publica los cambios con Git.

Los archivos CSV, XLSX, FIT, ZIP, GPX y TCX están excluidos del repositorio. Los HTML generados contienen únicamente los datos necesarios para representar los informes públicos.

## GitHub Pages

El sitio está preparado para publicarse desde la rama `main` y la carpeta raíz mediante GitHub Pages.
