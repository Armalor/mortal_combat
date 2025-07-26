import sys
from pathlib import Path, PurePath

__root__ = Path(__file__).resolve().parent


def get_pure_path(relative_path) -> str:
    if hasattr(sys, '_MEIPASS'):
        path = PurePath(sys._MEIPASS, relative_path).__str__()
    else:
        path = PurePath(__root__,  relative_path).__str__()

    return path
