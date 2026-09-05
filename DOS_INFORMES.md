# Arquitectura de los informes Garmin

## 1. Informe inmediato

### Objetivo

Consultar rápidamente la evolución del entrenamiento y el rendimiento con los datos que Garmin Connect permite descargar en el momento.

### Fuente

- CSV de `Garmin Connect > Actividades > Todas las actividades > Exportar CSV`.
- Actualización prevista: semanal, quincenal o cuando se desee.
- El archivo puede contener todo el historial; el importador detectará actividades ya incorporadas.

### Análisis

- Volumen por mes: sesiones, horas, distancia y desnivel.
- Comparación anual de enero a diciembre, con una línea por año.
- Frecuencia cardiaca media y máxima.
- Ritmo o velocidad media.
- Efecto aeróbico.
- Cadencia, longitud de zancada y potencia cuando existan.
- Eficiencia aproximada: velocidad o ritmo respecto al pulso.
- Comparación de carga y rendimiento por deporte.
- Tabla y filtros de actividades.

### Limitaciones

- El CSV contiene resúmenes, no la evolución dentro de cada sesión.
- El terreno, el clima y el desnivel pueden distorsionar las comparaciones de velocidad.
- No incluye actualmente VO2 máximo, HRV, sueño ni pulso en reposo.

## 2. Informe detallado

### Objetivo

Relacionar entrenamiento, adaptación fisiológica, recuperación y rendimiento a medio y largo plazo.

### Fuente

- ZIP completo de Garmin Data Management.
- Archivos FIT originales de actividades y bienestar.
- Informes adicionales de VO2 máximo, peso u otras métricas si Garmin los entrega por separado.
- Actualización prevista: mensual, trimestral o cuando se solicite una nueva exportación completa.

### Análisis adicional

- Evolución de VO2 máximo.
- HRV y frecuencia cardiaca en reposo.
- Sueño, estrés y Body Battery cuando estén disponibles.
- Tiempo real en zonas de frecuencia cardiaca y potencia.
- Carga aguda y crónica.
- Distribución de intensidad.
- Desacoplamiento cardiaco durante sesiones largas.
- Potencia normalizada, FTP y potencia relativa cuando existan.
- Umbral de lactato y métricas avanzadas de carrera.
- Relación entre carga, recuperación y cambios de rendimiento.

## Organización de archivos

```text
datos garmin/
  inmediato/    CSV descargados desde la lista de actividades
  completo/     ZIP de Garmin Data Management y exportaciones FIT
  auxiliares/   VO2 máximo, peso u otros informes CSV
```

Los archivos originales no se editarán. El sistema generará datos normalizados en una carpeta separada y conservará la fecha y procedencia de cada importación.

## Presentación web

La web tendrá dos accesos:

1. **Seguimiento inmediato**, con la fecha del último CSV importado.
2. **Análisis detallado**, con la fecha de la última exportación completa.

Cuando una métrica del informe detallado esté desactualizada, se mostrará su fecha de cobertura para no mezclarla accidentalmente con información reciente del informe inmediato.
