import os
import sys
from pathlib import Path

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = str(Path(__file__).parents[2])
if PROJECT_DIR not in sys.path:
    sys.path.append(PROJECT_DIR)

from demos.database.app import create_app

"""gunicorn --workers=3 wsgi:app -b 0.0.0.0:9996"""

app = create_app()
