import os
import glob
from typing import Literal


def get_models_list() -> Literal[str]:
    _files = glob.glob("app/models/*/*")
    files = ["/".join(file.split("/")[2:]) for file in _files]
    return files
