"""Pipeline runner — executes notebooks 02, 03, and 04 sequentially without Jupyter CLI."""

import json
import logging
import os
import sys
from pathlib import Path

# Configure logging format
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def mock_display(*args, **kwargs):
    for arg in args:
        print(arg)


def run_notebook(notebook_path: Path):
    logger.info("=" * 60)
    logger.info(f"Executing: {notebook_path.name}")
    logger.info("=" * 60)

    with open(notebook_path, encoding="utf-8") as f:
        nb = json.load(f)

    code_cells = []
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            source = "".join(cell.get("source", []))
            code_cells.append(source)

    full_code = "\n\n# --- NEW CELL ---\n\n".join(code_cells)

    project_root = notebook_path.resolve().parent.parent
    os.chdir(project_root)

    exec_globals = {
        "__name__": "__main__",
        "__file__": str(notebook_path),
        "display": mock_display,
    }

    try:
        exec(full_code, exec_globals)
        logger.info(f"Finished: {notebook_path.name}\n")
    except Exception as e:
        logger.error(f"Error executing {notebook_path.name}: {e}")
        raise


def main():
    root = Path(__file__).resolve().parent.parent
    notebooks = [
        root / "notebooks" / "02_preprocessing.ipynb",
        root / "notebooks" / "03_sentiment_analysis.ipynb",
        root / "notebooks" / "04_visualization.ipynb",
    ]

    for nb in notebooks:
        if not nb.exists():
            logger.error(f"Error: Notebook {nb} does not exist!")
            sys.exit(1)
        run_notebook(nb)

    logger.info("All pipeline steps executed successfully!")


if __name__ == "__main__":
    main()
