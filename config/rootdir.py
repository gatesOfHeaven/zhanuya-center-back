
from pathlib import Path


LOG_DIR = Path(__file__).parent.parent / '__logs__'
LOG_DIR.mkdir(parents = True, exist_ok = True)