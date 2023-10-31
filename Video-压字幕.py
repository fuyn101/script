import os
import subprocess

input_folder = input("请输入输入文件夹路径: ")
output_folder = "./output/"  # 输出文件夹路径，您可以自定义

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for mp4_file in os.listdir(input_folder):
    if mp4_file.endswith(".mp4"):
        mp4_path = os.path.join(input_folder, mp4_file)
        srt_file = os.path.splitext(mp4_file)[0] + ".srt"
        srt_path = os.path.join(input_folder, srt_file)
        
        if os.path.exists(srt_path):
            output_file = os.path.splitext(mp4_file)[0] + "_output.mp4"
            output_path = os.path.join(output_folder, output_file)
            
            ffmpeg_command = [
                "ffmpeg",
                "-i", mp4_path,
                "-vf", f"subtitles={srt_path}",
                "-y", output_path
            ]
            
            subprocess.run(ffmpeg_command)
            print(f"合并完成: {mp4_file} + {srt_file} -> {output_file}")
        else:
            print(f"找不到对应的字幕文件: {srt_file}")
import os
import subprocess

input_folder = "./"  # 输入文件夹路径，当前路径为"./"
output_folder = "./output/"  # 输出文件夹路径，您可以自定义

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for mp4_file in os.listdir(input_folder):
    if mp4_file.endswith(".mp4"):
        mp4_path = os.path.join(input_folder, mp4_file)
        srt_file = os.path.splitext(mp4_file)[0] + ".srt"
        srt_path = os.path.join(input_folder, srt_file)
        
        if os.path.exists(srt_path):
            output_file = os.path.splitext(mp4_file)[0] + "_output.mp4"
            output_path = os.path.join(output_folder, output_file)
            
            ffmpeg_command = [
                "ffmpeg",
                "-i", mp4_path,
                "-vf", f"subtitles={srt_path}",
                "-y", output_path
            ]
            
            subprocess.run(ffmpeg_command)
            print(f"合并完成: {mp4_file} + {srt_file} -> {output_file}")
        else:
            print(f"找不到对应的字幕文件: {srt_file}")
