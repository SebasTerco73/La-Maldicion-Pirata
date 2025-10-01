import os
import sys

# Añadir el directorio src al path de Python
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, 'src'))

# Cambiar al directorio del proyecto para que los recursos se puedan encontrar
os.chdir(project_root)

# Importar y ejecutar el juego
from main import main

if __name__ == "__main__":
    main()