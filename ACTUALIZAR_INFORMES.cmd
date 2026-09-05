@echo off
cd /d "%~dp0"
echo Actualizando informes con el CSV mas reciente...
python generar_muestra.py
if errorlevel 1 goto error
python generar_zonas.py
if errorlevel 1 goto error
echo.
echo Informes actualizados correctamente.
echo Abriendo pagina principal...
start "" "%~dp0index.html"
pause
exit /b 0
:error
echo.
echo No se pudieron actualizar los informes. Comprueba que Python esta instalado
echo y que existe al menos un CSV en la carpeta datos garmin.
pause
exit /b 1
