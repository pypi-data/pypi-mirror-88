import importlib
from pathlib import Path


def import_all():
    for path in Path(__file__).resolve().parent.glob("*.py"):
        if path.stem != "__init__":
            importlib.import_module(f".{path.stem}", __name__)
