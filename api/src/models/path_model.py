from dataclasses import dataclass

import os
from datetime import datetime
from pathlib import Path

@dataclass
class PathModel:
    api_dir_path = Path(__file__).resolve().parent.parent.parent
    log_dir_path: str = os.path.join(api_dir_path, "logs")
    log_path: str = os.path.join(
        log_dir_path, f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
    )
    data_dir_path: str = os.path.join(api_dir_path, "data")
    model_dir_path: str = os.path.join(data_dir_path, "models")
