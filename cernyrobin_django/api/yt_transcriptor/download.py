from pytube import YouTube
from yt_dlp import YoutubeDL
from moviepy.video.io.VideoFileClip import VideoFileClip
from colorama import Fore
import os

def download_and_convert_audio_old(youtube_url, output_dir, name, output_format="wav", temp_format="mp4"):
    print(f"{Fore.YELLOW}Downloading video from {youtube_url}...{Fore.RESET}")

    video_path = os.path.join(output_dir, f"temp_video.{temp_format}")
    audio_path = os.path.join(output_dir, f"{name}.{output_format}")

    youtube = YouTube(youtube_url)
    video = youtube.streams.filter().first()
    video.download(output_path=output_dir, filename=f"temp_video.{temp_format}")
    
    print(f"{Fore.YELLOW}Converting video to audio ({output_format})...{Fore.RESET}")

    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(audio_path)
    
    print(f"{Fore.GREEN}Successfully downloaded and converted video to audio.{Fore.RESET}")
    
    video_clip.close()
    audio_clip.close()
    os.remove(video_path)

    return audio_path

def download_and_convert_audio(youtube_url, output_dir, name, output_format="wav", temp_format="mp4"):
    print(f"{Fore.YELLOW}Downloading video from {youtube_url}...{Fore.RESET}")

    # video_path = os.path.join(output_dir, f"temp_video.{temp_format}")
    audio_path = os.path.join(output_dir, f"{name}.{output_format}")

    # youtube = YouTube(youtube_url)
    # video = youtube.streams.filter().first()
    # video.download(output_path=output_dir, filename=f"temp_video.{temp_format}")´
    ffmpeg_path = "/usr/bin/ffmpeg"

    if not os.path.exists(ffmpeg_path):
        ffmpeg_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "ffmpeg.exe")

        if not os.path.exists(ffmpeg_path):
            print("FFMPEG NOT FOUND!")
    
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, name),
    }

    if os.path.exists(ffmpeg_path):
        options['ffmpeg_location'] = ffmpeg_path

    with YoutubeDL(options) as ydl:
        ydl.download([youtube_url])
    
    # print(f"{Fore.YELLOW}Converting video to audio ({output_format})...{Fore.RESET}")

    # video_clip = VideoFileClip(video_path)
    # audio_clip = video_clip.audio
    # audio_clip.write_audiofile(audio_path)
    
    print(f"{Fore.GREEN}Successfully downloaded and converted video to audio.{Fore.RESET}")
    
    # video_clip.close()
    # audio_clip.close()
    # os.remove(video_path)

    return audio_path
