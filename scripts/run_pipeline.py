"""Pipeline runner — executes notebooks 02, 03, and 04 sequentially without Jupyter."""

import logging
import subprocess
import sys
from pathlib import Path

# Configure logging format
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def run_notebook(notebook_path: Path):
    logger.info("=" * 60)
    logger.info(f"Executing: {notebook_path.name}")
    logger.info("=" * 60)

    try:
        subprocess.run(
            [
                "jupyter",
                "nbconvert",
                "--to",
                "notebook",
                "--execute",
                "--ExecutePreprocessor.timeout=600",
                str(notebook_path),
            ],
            check=True,
        )
        logger.info(f"Finished: {notebook_path.name}\n")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing {notebook_path.name}: {e}")
        raise


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
