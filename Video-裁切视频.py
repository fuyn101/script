import os
import subprocess

def batch_crop_videos(input_folder, output_folder, start_time):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video_files = [f for f in os.listdir(input_folder) if f.endswith(".mp4")]

    for video_file in video_files:
        input_path = os.path.join(input_folder, video_file)
        output_path = os.path.join(output_folder, video_file)
        crop_video(input_path, output_path, start_time)

def crop_video(input_path, output_path, start_time):
    ffmpeg_cmd = [
        "ffmpeg",
        "-ss", str(start_time),
        "-i", input_path,
        "-c:v", "copy",
        "-c:a", "copy",
        output_path
    ]

    subprocess.run(ffmpeg_cmd)

if __name__ == "__main__":
    input_folder = input("Enter the input folder path: ")
    output_folder = input("Enter the output folder path: ")
    start_time = 29.959  # Start time in seconds

    batch_crop_videos(input_folder, output_folder, start_time)
