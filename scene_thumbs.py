import cv2
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from scenedetect import detect, ContentDetector
from PIL import Image
import io
import os


def create_thumbnail(frame, size=(320, 180)):
    """
    Convert OpenCV frame to PIL Image and resize it

    # Note: OpenCV uses BGR format while PIL uses RGB
    # We need to convert between these color spaces
    """
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(frame_rgb)
    return pil_image.resize(size)


def process_video(video_path, output_pdf):
    """
    Detect scenes in video and save thumbnails to PDF

    # ContentDetector is used to detect significant changes between frames
    # that likely indicate scene changes
    """
    # Detect scene changes
    scenes = detect(video_path, ContentDetector())

    # Open video capture
    cap = cv2.VideoCapture(video_path)

    # Create PDF
    c = canvas.Canvas(output_pdf, pagesize=letter)
    width, height = letter

    # Layout settings
    thumb_width = width / 2
    thumb_height = (thumb_width * 9) / 16  # Maintain 16:9 aspect ratio
    x_positions = [width * 0.1, width * 0.5]
    y_position = height - thumb_height - 50
    items_per_page = 6

    for i, scene in enumerate(scenes):
        # Get frame at scene start
        cap.set(cv2.CAP_PROP_POS_FRAMES, scene[0].frame_num)
        ret, frame = cap.read()

        if ret:
            # Create thumbnail
            thumb = create_thumbnail(frame)

            # Save thumbnail to bytes buffer
            img_buffer = io.BytesIO()
            thumb.save(img_buffer, format="PNG")

            # Add new page if needed
            if i > 0 and i % items_per_page == 0:
                c.showPage()
                y_position = height - thumb_height - 50

            # Calculate position
            x_pos = x_positions[i % 2]

            # Draw thumbnail
            c.drawImage(
                img_buffer, x_pos, y_position, width=thumb_width, height=thumb_height
            )

            # Add scene number
            c.setFont("Helvetica", 12)
            c.drawString(x_pos, y_position - 20, f"Scene {i+1}")

            # Update y position if we've drawn two thumbnails in a row
            if i % 2 == 1:
                y_position -= thumb_height + 50

    cap.release()
    c.save()


if __name__ == "__main__":
    # Example usage
    video_path = "input_video.mp4"
    output_pdf = "scene_thumbnails.pdf"

    if os.path.exists(video_path):
        process_video(video_path, output_pdf)
        print(f"PDF created successfully: {output_pdf}")
    else:
        print(f"Error: Video file not found: {video_path}")
