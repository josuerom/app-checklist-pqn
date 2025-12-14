#!/bin/bash

echo "🚀 Iniciando App Checklist PQN..."
echo ""

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 no está instalado${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python encontrado${NC}"

# Verificar entorno virtual
if [ ! -d "venv" ]; then
    echo -e "${BLUE}📦 Creando entorno virtual...${NC}"
    cd ..
    python3 -m venv venv
fi

# Activar entorno virtual
echo -e "${BLUE}🔧 Activando entorno virtual...${NC}"
source venv/bin/activate

# Instalar dependencias
echo -e "${BLUE}📥 Instalando dependencias...${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Verificar .env
if [ ! -f ".env" ]; then
    echo -e "${RED}⚠️  Archivo .env no encontrado${NC}"
    echo -e "${BLUE}📝 Copiando .env.example a .env...${NC}"
    cp .env.example .env
    echo -e "${RED}⚠️  Por favor, edita el archivo .env con tus configuraciones${NC}"
fi

# Crear directorios
echo -e "${BLUE}📁 Creando directorios necesarios...${NC}"
mkdir -p output logs templates_excel

echo ""
echo -e "${GREEN}✨ ¡Todo listo!${NC}"
echo ""
echo -e "${BLUE}🌐 Iniciando servidor...${NC}"
echo -e "${BLUE}📍 La aplicación estará disponible en: http://localhost:9015${NC}"
echo ""

# Ejecutar aplicación
python app.py