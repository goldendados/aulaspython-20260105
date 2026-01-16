import sys
import os

# Adiciona o diretório raiz ao path para importar app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Exporta a aplicação para o Vercel
application = app

