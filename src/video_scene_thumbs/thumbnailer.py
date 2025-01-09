import cv2
import numpy as np
from PIL import Image
import os
from pathlib import Path
from typing import Tuple, List
from scenedetect import detect, ContentDetector, AdaptiveDetector
from .combine_scenes import combine_thumbnails


def create_thumbnail(frame: np.ndarray, target_width: int = 320) -> Image.Image:
    """
    Convert OpenCV frame to PIL Image and resize it maintaining aspect ratio

    Args:
        frame: OpenCV frame in BGR format
        target_width: Desired width of thumbnail

    Returns:
        PIL Image object of the resized thumbnail
    """
    height, width = frame.shape[:2]
    aspect_ratio = width / height
    target_height = int(target_width / aspect_ratio)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(frame_rgb)
    return pil_image.resize((target_width, target_height), Image.Resampling.LANCZOS)


def save_frame_thumbnail(
    cap: cv2.VideoCapture, frame_num: int, output_dir: Path, scene_num: int
) -> str:
    """Helper function to save a single frame as thumbnail"""
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    ret, frame = cap.read()
    if ret:
        thumb = create_thumbnail(frame)
        output_path = output_dir / f"scene_{scene_num:03d}.png"
        thumb.save(output_path)
        print(f"Saved thumbnail: {output_path}")
        return str(output_path)
    return ""


def process_video(
    video_path: str, output_dir: str = "thumbnails", combine_output: bool = True
) -> List[str]:
    """
    Detect scenes in video and save thumbnails as PNG files

    Args:
        video_path: Path to input video file
        output_dir: Base directory for thumbnails
        combine_output: Whether to combine thumbnails into a single image

    Returns:
        List of paths to generated thumbnail files
    """
    print(f"\nProcessing video: {video_path}")

    if not os.path.exists(video_path):
        print(f"Error: Video file not found: {video_path}")
        return []

    # Create temporary directory for individual thumbnails
    import tempfile

    temp_dir = Path(tempfile.mkdtemp())

    try:
        # Open video capture first to check if video is valid
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video file: {video_path}")
            return []

        # Print video information
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = total_frames / fps if fps > 0 else 0
        print(
            f"Video info: {width}x{height} @ {fps:.2f}fps, "
            f"{total_frames} frames, {duration:.2f} seconds"
        )

        # Detect scene changes with more sensitive settings
        print("\nDetecting scenes...")
        detector = ContentDetector(
            threshold=20.0,  # Lower threshold means more sensitive detection
            min_scene_len=15,  # Minimum number of frames between scenes
        )
        scenes = detect(video_path, detector)
        print(f"Found {len(scenes)} scenes")

        generated_files = []

        # Always save the first frame
        first_frame = save_frame_thumbnail(cap, 0, temp_dir, 1)
        if first_frame:
            generated_files.append(first_frame)

        # Save middle frame if video is longer than 5 seconds
        if duration > 5 and total_frames > 0:
            mid_frame = save_frame_thumbnail(cap, total_frames // 2, temp_dir, 2)
            if mid_frame:
                generated_files.append(mid_frame)

        # Process detected scenes (starting from scene 3 since we already have first and middle frames)
        scene_num = len(generated_files) + 1
        for scene in scenes:
            frame_num = scene[0].frame_num
            # Skip if this frame is too close to already saved frames
            if not any(
                abs(frame_num - int(cap.get(cv2.CAP_PROP_POS_FRAMES))) < 15
                for _ in generated_files
            ):
                result = save_frame_thumbnail(cap, frame_num, temp_dir, scene_num)
                if result:
                    generated_files.append(result)
                    scene_num += 1

        cap.release()

        if generated_files:
            print(f"\nSuccessfully generated {len(generated_files)} thumbnails")
            if combine_output:
                # Create output directory if it doesn't exist
                output_dir = Path(output_dir)
                output_dir.mkdir(parents=True, exist_ok=True)

                # Use video name for the combined image
                video_name = Path(video_path).stem
                combined_output = str(output_dir / f"{video_name}.png")
                combine_thumbnails(generated_files, output_path=combined_output)
                return [combined_output]
        else:
            print("\nWarning: Failed to generate any thumbnails!")

    finally:
        # Clean up temporary files
        import shutil

        shutil.rmtree(temp_dir, ignore_errors=True)

    return []


if __name__ == "__main__":
    # Example usage
    video_path = "input_video.mp4"
    process_video(video_path)
