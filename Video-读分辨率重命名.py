import os
import subprocess
import re

RESOLUTION_MAP = {
    "640x480": "480p",
    "1920x1080": "1080p",
    "3840x2160": "4k"
    # 添加更多分辨率映射
    # "widthxheight": "label",
}

def get_video_resolution(filename):
    try:
        cmd = ['ffmpeg', '-i', filename]
        result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = result.communicate()

        # 解析输出以获取分辨率信息
        output = stdout.decode('utf-8')
        match = re.search(r"(\d{3,4}x\d{3,4})", output)
        if match:
            resolution = match.group(1)
            return RESOLUTION_MAP.get(resolution, resolution)
        return None
    except Exception as e:
        print("Error:", e)
        return None

def rename_videos_in_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):  # 支持的视频文件扩展名
                video_file = os.path.join(root, file)
                resolution = get_video_resolution(video_file)
                
                if resolution:
                    base_name = os.path.splitext(file)[0]
                    extension = os.path.splitext(file)[1]
                    new_file_name = f"{base_name} [{resolution}]{extension}"
                    new_file_path = os.path.join(root, new_file_name)
                    
                    os.rename(video_file, new_file_path)
                    print(f"Renamed '{video_file}' to '{new_file_path}'")
                else:
                    print(f"Unable to determine the resolution of '{video_file}'")

if __name__ == "__main__":
    folder_path = "D:\影视\电视剧\The Big Bang Theory"  # 更改为你的文件夹路径
    rename_videos_in_folder(folder_path)
