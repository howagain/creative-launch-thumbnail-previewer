import sys
import os
import logging
from pathlib import Path
from video_scene_thumbs.ui import main


# Set up logging
def setup_logging():
    # Get the user's home directory for logs
    home = Path.home()
    log_dir = home / "Library/Logs/Video Scene Thumbnailer"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "app.log"

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler(sys.stdout)],
    )

    # Log system info
    logging.info(f"Python version: {sys.version}")
    logging.info(f"Executable path: {sys.executable}")
    logging.info(f"Working directory: {os.getcwd()}")
    return log_file


if __name__ == "__main__":
    try:
        log_file = setup_logging()
        logging.info("Starting application...")
        main()
    except Exception as e:
        logging.exception("Application crashed:")
        with open(log_file, "a") as f:
            f.write(f"\nError: {str(e)}\n")
