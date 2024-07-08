import glob
from typing import Literal


def get_models_list(path) -> Literal[list[str]]:
    _files = glob.glob(path)
    files = ["/".join(file.split("models")[::-2]) for file in _files]
    return files
