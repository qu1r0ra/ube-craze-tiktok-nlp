import json
import logging
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

# Configure logging format
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def run_notebook(notebook_path: Path):
    logger.info("=" * 60)
    logger.info(f"Executing: {notebook_path.name}")
    logger.info("=" * 60)

    with open(notebook_path, encoding="utf-8") as f:
        nb = json.load(f)

    code_cells = []
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            source = cell.get("source", [])
            code = "".join(source) if isinstance(source, list) else source
            code_cells.append(code)

    full_code = "\n\n# --- Cell boundary ---\n\n".join(code_cells)

    # Exec global namespace mocking display() to prevent notebook errors in terminal
    global_namespace = {
        "display": lambda x: logger.info(x),
        "__file__": str(notebook_path.absolute()),
    }

    # Execute the concatenated Python code
    exec(full_code, global_namespace)
    logger.info(f"Finished: {notebook_path.name}\n")


def main():
    # Since run_pipeline.py is now in scripts/, the project root is parent.parent
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
