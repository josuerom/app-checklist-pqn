@echo off
echo.
echo ======================================
echo   App Checklist Proquinal
echo   Sistema de Alistamiento de Equipos
echo ======================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado
    pause
    exit /b 1
)

echo [OK] Python encontrado

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo [INFO] Creando entorno virtual...
    cd ..
    python -m venv venv
)

REM Activar entorno virtual
echo [INFO] Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo [INFO] Instalando dependencias...
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

REM Verificar .env
if not exist ".env" (
    echo [AVISO] Archivo .env no encontrado
    echo [INFO] Copiando .env.example a .env...
    copy .env.example .env
    echo [AVISO] Por favor, edita el archivo .env con tus configuraciones
)

REM Crear directorios
echo [INFO] Creando directorios necesarios...
if not exist "output" mkdir output
if not exist "logs" mkdir logs
if not exist "templates_excel" mkdir templates_excel

echo.
echo ======================================
echo   TODO LISTO!
echo ======================================
echo.
echo [INFO] Iniciando servidor...
echo [INFO] Aplicacion disponible en: http://localhost:9015
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

REM Ejecutar aplicación
python app.py