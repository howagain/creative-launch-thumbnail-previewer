from PIL import Image, ImageDraw, ImageFont
import os


def create_icon(size=512):
    # Create a new image with a dark background
    img = Image.new("RGB", (size, size), "#2C2C2C")
    draw = ImageDraw.Draw(img)

    # Draw a film strip design
    margin = size // 8
    strip_height = size // 4

    # Draw three rectangles representing film frames
    for i in range(3):
        y = margin + (i * (strip_height + margin))
        draw.rectangle(
            [margin, y, size - margin, y + strip_height],
            outline="white",
            width=size // 50,
        )

    # Save in different sizes for iconset
    if not os.path.exists("app_icon.iconset"):
        os.makedirs("app_icon.iconset")

    # Generate different sizes
    sizes = [16, 32, 64, 128, 256, 512]
    for s in sizes:
        resized = img.resize((s, s), Image.Resampling.LANCZOS)
        resized.save(f"app_icon.iconset/icon_{s}x{s}.png")
        # Generate retina versions
        if s * 2 <= 512:
            resized = img.resize((s * 2, s * 2), Image.Resampling.LANCZOS)
            resized.save(f"app_icon.iconset/icon_{s}x{s}@2x.png")

    return img


if __name__ == "__main__":
    # Create the icon
    create_icon()

    # Convert to icns using iconutil (macOS command)
    os.system("iconutil -c icns app_icon.iconset")
    print("Icon generated: app_icon.icns")
