import os
import random
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips, concatenate_videoclips, CompositeVideoClip
import tkinter as tk
from tkinter import messagebox
from moviepy.config import change_settings

# Ensure MoviePy uses system's FFmpeg for GPU acceleration
change_settings({"FFMPEG_BINARY": "/usr/bin/ffmpeg"})

def create_video_loop(video_path, loop_duration, fade_duration):
    """
    Loop the input video with smooth crossfade transitions between each loop.
    
    :param video_path: Path to the input video file (e.g., 5 to 50 seconds video).
    :param loop_duration: Total duration to loop the video (e.g., 3 hours).
    :param fade_duration: Duration of the crossfade effect (in seconds).
    :return: The final video clip that has been looped with crossfade transitions.
    """
    clip = VideoFileClip(video_path)
    clip_duration = clip.duration

    # Calculate how many loops are needed to match the target duration
    loops = int(loop_duration // (clip_duration - fade_duration))

    clips = []
    for i in range(loops):
        # Offset the starting time of each clip
        offset = i * (clip_duration - fade_duration)
        
        # Crossfade in and out, making the transitions smooth between clips
        faded_clip = clip.crossfadein(fade_duration).crossfadeout(fade_duration).set_start(offset)
        clips.append(faded_clip)

    # Overlay the clips into one composite video with smooth transitions
    final_clip = CompositeVideoClip(clips)

    return final_clip


def create_music_playlist(songs_folder, playlist_duration):
    """
    Create a random playlist of songs from the provided folder and concatenate them.
    
    :param songs_folder: Folder where the songs are located.
    :param playlist_duration: Target duration for the playlist in seconds (e.g., 50 minutes).
    :return: A concatenated AudioFileClip of the chosen songs.
    """
    songs = [os.path.join(songs_folder, f) for f in os.listdir(songs_folder) if f.endswith('.mp3')]
    
    if not songs:
        raise ValueError("No songs found in the folder!")

    random.shuffle(songs)  # Randomize the order of songs
    playlist = []
    total_duration = 0

    for song in songs:
        audio = AudioFileClip(song)
        total_duration += audio.duration
        playlist.append(audio)

        if total_duration >= playlist_duration:
            break
    
    # Concatenate all selected songs into one long audio track
    final_audio = concatenate_audioclips(playlist)
    
    return final_audio


def combine_video_audio(video_clip, audio_clip):
    """
    Combine the looped video and the audio into one final video clip.
    
    :param video_clip: The looped video clip.
    :param audio_clip: The concatenated audio playlist.
    :return: The final combined video with audio.
    """
    return video_clip.set_audio(audio_clip)


def ask_render_confirmation():
    """
    Open a pop-up window with Yes/No options to ask if the user wants to render the video.
    
    :return: True if the user clicks 'Yes', False if 'No'
    """
    window = tk.Tk()
    window.withdraw()  # Hide the main window

    result = messagebox.askyesno("Render Confirmation", "Do you want to generate the video?")
    window.destroy()

    return result


def preview_and_render(final_video, output_path):
    """
    Show a preview of the final video and ask the user if they want to render it.
    Also show a progress bar during rendering, using hardware acceleration.
    
    :param final_video: The final video clip to preview and potentially render.
    :param output_path: Path to save the rendered video file.
    """
    print("Showing a preview of the video...")
    final_video.preview()  # This shows a quick preview
    
    if ask_render_confirmation():
        print("Rendering the video... This may take a while.")
        
        # Render the video using hardware-accelerated encoding (NVIDIA GPU)
        final_video.write_videofile(
            output_path,
            codec="h264_nvenc",  # Use NVIDIA encoder for acceleration
            preset="fast",       # Adjust preset for speed (options: fast, medium, slow)
            fps=30,              # Set FPS for YouTube
            threads=16           # Adjust thread count for better performance
        )
        
        print(f"Video has been generated and saved at {output_path}")
    else:
        print("Video generation canceled.")


def generate_lofi_video(video_folder, songs_folder, output_folder):
    """
    Main function to generate a 3-hour lofi video by looping a variable-length video
    and creating a music playlist from songs in the specified folder.
    
    :param video_folder: Folder containing the video to be looped.
    :param songs_folder: Folder containing the songs for the audio playlist.
    :param output_folder: Folder to save the generated video.
    """
    # Define constants
    video_duration = 3 * 60 * 60  # 3 hours in seconds
    playlist_duration = 50 * 60   # 50 minutes in seconds
    fade_duration = 6             # Crossfade duration for smoother transitions
    
    # Paths
    video_path = os.path.join(video_folder, 'animated_picture.mp4')
    output_path = os.path.join(output_folder, 'lofi_video.mp4')

    # Load and process the video loop
    print("Processing video loop...")
    video_clip = create_video_loop(video_path, video_duration, fade_duration)
    
    # Load and process the music playlist
    print("Creating music playlist...")
    audio_clip = create_music_playlist(songs_folder, playlist_duration)
    
    # Combine video and audio
    print("Combining video and audio...")
    final_video = combine_video_audio(video_clip, audio_clip)
    
    # Preview and render the video
    preview_and_render(final_video, output_path)


if __name__ == "__main__":
    # Define your folder paths
    video_folder = "videos"  # Folder where the video is stored
    songs_folder = "songs"  # Folder where your songs are stored
    output_folder = "output"  # Folder to save the final video

    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Generate the lofi video
    generate_lofi_video(video_folder, songs_folder, output_folder)
