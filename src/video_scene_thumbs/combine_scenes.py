from PIL import Image
from pathlib import Path
from typing import List, Tuple
import math


def combine_thumbnails(
    image_paths: List[str],
    output_path: str = "combined_scenes.png",
    max_width: int = 1920,
    padding: int = 10,
    bg_color: Tuple[int, int, int] = (0, 0, 0),
) -> str:
    """
    Combine multiple thumbnails into a single image in a grid layout

    Args:
        image_paths: List of paths to thumbnail images
        output_path: Path for the output combined image
        max_width: Maximum width of the output image
        padding: Padding between images and border
        bg_color: Background color as RGB tuple

    Returns:
        Path to the generated combined image
    """
    if not image_paths:
        print("No images to combine")
        return ""

    # Open all images first to get maximum dimensions
    images = []
    max_width_thumb = 0
    max_height_thumb = 0

    for img_path in image_paths:
        try:
            img = Image.open(img_path)
            images.append(img)
            max_width_thumb = max(max_width_thumb, img.width)
            max_height_thumb = max(max_height_thumb, img.height)
        except Exception as e:
            print(f"Error opening {img_path}: {e}")

    if not images:
        return ""

    # Calculate grid dimensions
    num_images = len(images)
    max_columns = max(1, (max_width - padding) // (max_width_thumb + padding))
    num_columns = min(num_images, max_columns)
    num_rows = math.ceil(num_images / num_columns)

    # Calculate canvas size
    canvas_width = (max_width_thumb * num_columns) + (padding * (num_columns + 1))
    canvas_height = (max_height_thumb * num_rows) + (padding * (num_rows + 1))

    # Create new image with background color
    combined = Image.new("RGB", (canvas_width, canvas_height), bg_color)

    # Place each thumbnail
    for idx, img in enumerate(images):
        try:
            row = idx // num_columns
            col = idx % num_columns
            x = padding + col * (max_width_thumb + padding)
            y = padding + row * (max_height_thumb + padding)

            # Center the image in its cell if it's smaller than the maximum dimensions
            x_offset = (max_width_thumb - img.width) // 2
            y_offset = (max_height_thumb - img.height) // 2
            combined.paste(img, (x + x_offset, y + y_offset))
        except Exception as e:
            print(f"Error processing image {idx}: {e}")

    # Save combined image
    combined.save(output_path)
    print(f"Combined image saved to: {output_path}")
    return output_path


def main():
    """Combine all thumbnails in the thumbnails directory"""
    base_dir = Path("thumbnails")
    if not base_dir.exists():
        print("Thumbnails directory not found")
        return

    # Process each video subdirectory
    for video_dir in base_dir.iterdir():
        if video_dir.is_dir():
            print(f"\nProcessing directory: {video_dir}")

            # Get all PNG files in this video's directory
            image_paths = sorted(str(p) for p in video_dir.glob("scene_*.png"))

            if not image_paths:
                print("No thumbnail images found")
                continue

            print(f"Found {len(image_paths)} thumbnails")
            output_path = str(video_dir / "combined_scenes.png")
            combine_thumbnails(image_paths, output_path=output_path)


if __name__ == "__main__":
    main()
