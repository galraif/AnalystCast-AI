from pathlib import Path

# Dynamically resolve the root directory of the project
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Data directories
REPORTS_DIR = PROJECT_ROOT / "data"

