# from src.models.config_model import ConfigModel

# CONFIG = ConfigModel()

# A mettre dans le fichier models/path_model.py
# Utiliser des chemins relatifs plutôt que des chemins absolus

DOWNLOAD_PATH: str = "./model/"
SESSION_PATH: str = "erwanduprey/"

# Mettre tout ce qu'il y a en dessous dans un fichier type models/file_model.py,
# faire hériter à ConfigModel, le tout pour gérer la config des fichiers individuellement
FILE_PATH: str = "FINALE.keras"

# 10 MB
MAX_FILE_SIZE = 10 * 1024 * 1024
