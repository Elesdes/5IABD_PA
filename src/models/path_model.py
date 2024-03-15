from dataclasses import dataclass

import os
from datetime import datetime


@dataclass
class PathModel:
    log_dir_path: str = "logs"
    log_path: str = os.path.join(
        "logs", f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
    )
    data_dir_path: str = "data"
    model_dir_path: str = f"{data_dir_path}/models"
