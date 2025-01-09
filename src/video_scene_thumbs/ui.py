import streamlit as st
from pathlib import Path
import os
from video_scene_thumbs.thumbnailer import process_video


def main():
    st.set_page_config(page_title="Video Scene Thumbnailer", layout="wide")
    st.title("Video Scene Thumbnailer")

    # Folder path input
    folder_path = st.text_input(
        "Enter or paste folder path", placeholder="e.g., /path/to/your/videos"
    )

    if folder_path:
        folder = Path(folder_path)
        if not folder.exists():
            st.error("Folder not found!")
            return

        # Find all video files in the folder
        video_extensions = {".mp4", ".avi", ".mov", ".mkv", ".webm"}
        video_files = [
            f for f in folder.iterdir() if f.suffix.lower() in video_extensions
        ]

        if not video_files:
            st.warning("No video files found in the folder!")
            return

        st.info(f"Found {len(video_files)} video files")

        # Process each video file
        for video_path in video_files:
            with st.spinner(f"Processing {video_path.name}..."):
                try:
                    # Create thumbnails directory in the same folder
                    output_dir = video_path.parent / "thumbnails"
                    result = process_video(str(video_path), str(output_dir))

                    if result:
                        # Display the generated thumbnail
                        st.success(f"Generated thumbnail for {video_path.name}")
                        st.image(result[0], caption=f"Scenes from {video_path.name}")
                    else:
                        st.error(f"Failed to process {video_path.name}")

                except Exception as e:
                    st.error(f"Error processing {video_path.name}: {str(e)}")

    # Instructions
    with st.expander("Instructions"):
        st.markdown(
            """
            1. Enter the path to a folder containing videos
            2. Wait for processing to complete
            3. Thumbnails will be saved in a 'thumbnails' folder next to your videos
            4. Preview of combined scenes will appear below each processed video
            """
        )


if __name__ == "__main__":
    main()
