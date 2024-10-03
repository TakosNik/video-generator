# video-generator

This is a video generator using the **MoviePy** Python library. The program creates a seamless looping video from an animated picture or video clip, combines it with a random playlist of songs, and renders the final output. The process includes previewing the video before rendering and allows user confirmation to generate the final video.

## Features:
- Loops a video from the **videos** folder for a specified duration (e.g., 3 hours).
- Creates a random music playlist from the **songs** folder and syncs it with the video.
- Smooth crossfade transitions between video loops.
- GPU-accelerated rendering using NVIDIA’s `h264_nvenc` encoder for faster processing.
- A preview feature allows you to see the video before rendering.
- A confirmation window pops up after the preview to ask if the user wants to generate the final video.

## How It Works:
1. The user adds songs in the `songs` folder (in `.mp3` format).
2. The user places the video to be looped in the `videos` folder.
3. The program creates a random playlist and loops the video with crossfade transitions.
4. When the program is executed, a preview of the final video is shown.
5. The user presses the **Esc** key to close the preview, and a pop-up window appears asking whether to render the video.
6. If the user presses **Yes**, the program starts rendering the video.
7. The final video is saved in the `output` folder.

## Prerequisites:
Before running this program, ensure that you have the following installed on your system:
- **Python 3.x**
- **MoviePy**: Install via `pip3 install moviepy`.
- **FFmpeg** with **NVIDIA GPU support**: You must have the `h264_nvenc` encoder available in your FFmpeg installation. Verify this by running:
  ```bash
  ffmpeg -encoders | grep nvenc

## Setup Instructions:

1. Clone or download the project files into a directory.

2. Install the required Python packages:
   ```bash
   pip3 install moviepy
3. Ensure that FFmpeg is installed and properly configured on your system:
   Verify that FFmpeg is available in /usr/bin/ffmpeg and includes GPU support (h264_nvenc).



## How to Use:

1. **Add Songs and Video**:
   - Place the songs (in `.mp3` format) inside the `songs` folder.
   - Add the video file (e.g., `.mp4` format) inside the `videos` folder.

2. **Run the Program**: Execute the `main.py` script from the terminal:
   ```bash
   python3 main.py

3. **Preview**:

- A preview window will open, showing the final video with the audio playlist.
- Press the **Esc** key to close the preview.

4. **Confirmation**:

- A pop-up window will ask if you want to render the video.
- Press **Yes** to start rendering or **No** to cancel.

5. **Rendering**:

- If you choose to render, the program will create the final video and save it in the `output` folder.


