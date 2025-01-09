# Creative Launch Thumbnail Previewer

A simple tool to generate scene thumbnails from videos (Work in Progress).

## Current Status

This project is under active development. The core functionality for scene detection and thumbnail generation is being worked on, with a Streamlit-based interface in development.

## Planned Features

- Automatic scene change detection in videos
- Thumbnail generation for key scenes
- Combined preview image for each video
- Support for common video formats (.mp4, .avi, .mov, .mkv, .webm)
- Streamlit-based user interface

## Development Setup

1. **Install UV Package Manager**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install Python**
   ```bash
   uv python install 3.11
   ```

3. **Clone the Repository**
   ```bash
   git clone https://github.com/howagain/creative-launch-thumbnail-previewer.git
   cd creative-launch-thumbnail-previewer
   ```

4. **Set Up Development Environment**
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -e .
   ```

5. **Run the Application**
   ```bash
   streamlit run src/video_scene_thumbs/streamlit_app.py
   ```

## Requirements

- Python 3.11 (UV will install this automatically)
- Dependencies are managed through pyproject.toml:
  - opencv-python
  - numpy
  - Pillow
  - scenedetect
  - streamlit

## Contributing

This project is in early development. If you're interested in contributing:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Roadmap

- [ ] Complete core scene detection functionality
- [ ] Implement thumbnail generation
- [ ] Polish Streamlit interface
- [ ] Create installable application
- [ ] Add support for batch processing 