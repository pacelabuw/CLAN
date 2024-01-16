import os
from pathlib import Path

from .constants import INPUT_DIR, OUTPUT_DIR


def setup_filesystem() -> None:
    """Ensure input/output dirs exist, prompt user to add input files if input dir created."""
    input_dir = Path.cwd() / INPUT_DIR
    output_dir = Path.cwd() / OUTPUT_DIR

    if not output_dir.exists():
        os.mkdir(output_dir)
    if not input_dir.exists():
        os.mkdir(input_dir)
        raise Exception("Input dir created.")


def get_cha_files() -> list[str]:
    "Get all cha files in the input folder."
    files = [file for file in os.listdir(INPUT_DIR) if file.lower().endswith(".cha")]
    print(f"Found {len(files)} cha files to swap\n")
    return files
