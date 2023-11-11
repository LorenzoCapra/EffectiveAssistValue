import os
from pathlib import Path 
SRC_DIR = Path(os.path.dirname(os.path.abspath(__file__))).absolute().as_posix() # This is your Project Root
REPO_DIR = Path(SRC_DIR).parent.absolute().as_posix()
DATA_DIR = (Path(SRC_DIR).parent / "data").absolute().as_posix()
