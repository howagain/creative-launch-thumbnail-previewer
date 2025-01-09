import PyInstaller.__main__
import sys
from pathlib import Path

# Get the current directory
current_dir = Path(__file__).parent

# Create the spec file arguments
args = [
    "src/video_scene_thumbs/streamlit_app.py",
    "--name=Video Scene Thumbnailer",
    "--onedir",
    "--windowed",
    f"--add-data={current_dir}/src/video_scene_thumbs:video_scene_thumbs",
    "--icon=app_icon.icns",
    "--collect-all=streamlit",
    "--collect-all=scenedetect",
    "--collect-all=opencv-python",
    "--hidden-import=streamlit.web.boot",
    "--hidden-import=streamlit.runtime.scriptrunner",
    "--hidden-import=streamlit.runtime.caching",
    "--hidden-import=PIL._tkinter_finder",
    "--hidden-import=streamlit.runtime.scriptrunner.magic_funcs",
    "--hidden-import=cv2",
    "--noconfirm",
    "--clean",
]

# Run PyInstaller
PyInstaller.__main__.run(args)
