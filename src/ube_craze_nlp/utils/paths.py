"""Centralized path management for the Ube Craze NLP project."""

from pathlib import Path

# Resolve the absolute root directory of the project
ROOT_DIR = Path(__file__).resolve().parents[3]

# Data Directories
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
FINAL_DATA_DIR = DATA_DIR / "final"

# Reference and Outputs Directories
REFERENCES_DIR = ROOT_DIR / "references"
OUTPUTS_DIR = ROOT_DIR / "outputs"
NOTEBOOKS_DIR = ROOT_DIR / "notebooks"

# Config Files
LINKS_FILE = ROOT_DIR / "links.txt"


def ensure_dirs():
    """Ensure all required directories exist in the local workspace."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    FINAL_DATA_DIR.mkdir(parents=True, exist_ok=True)
    REFERENCES_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    NOTEBOOKS_DIR.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    # Test path resolution and print
    print(f"Project Root: {ROOT_DIR}")
    print(f"Data Dir: {DATA_DIR}")
    print(f"Outputs Dir: {OUTPUTS_DIR}")
    ensure_dirs()
    print("All directories verified/created.")
