# Video Scene Thumbnailer

A simple tool to generate scene thumbnails from videos.

## Installation (Mac)

1. **Download and Install Homebrew**
   Open Terminal (press `Cmd + Space`, type "Terminal" and press Enter) and paste this command:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Required Tools**
   In Terminal, run:
   ```bash
   brew install python@3.11
   brew install tcl-tk
   ```

3. **Install UV Package Manager**
   In Terminal, run:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

4. **Clone and Build the App**
   ```bash
   # Clone the repository
   git clone [your-repo-url]
   cd thumbnail-previewer

   # Make the build script executable
   chmod +x build.sh

   # Build the app
   ./build.sh
   ```

5. **Run the App**
   - The built app will be in the `dist` folder
   - Drag `Video Scene Thumbnailer.app` to your Applications folder
   - Double-click to run

## Usage

1. Launch the app by double-clicking it in Applications
2. Enter the path to a folder containing videos
3. Wait for processing to complete
4. Find the generated thumbnails in a 'thumbnails' folder next to your videos

## Troubleshooting

If the app doesn't start:
1. Open Terminal
2. Check the logs at: `~/Library/Logs/Video Scene Thumbnailer/app.log`
3. Send the log contents to the developer if you need help

## Requirements

- macOS 10.15 or later
- At least 500MB of free disk space
- Internet connection (for initial setup only) 