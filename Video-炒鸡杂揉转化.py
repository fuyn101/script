import os
import re
import subprocess


def create_output_folder(output_folder, suffix):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder + suffix


def extract_file_parts(filename):
    file_parts = re.match(r"^(.*?) - (s\d+e\d+)(.*)\.\w+$", filename, re.I)
    if file_parts:
        show_name = file_parts.group(1)
        episode_info = file_parts.group(2).upper()
        remaining_info = file_parts.group(3)
    else:
        show_name = "Unknown Show"
        episode_info = "Unknown Episode"
        remaining_info = os.path.splitext(filename)[0]
    return show_name, episode_info, remaining_info


def process_video(input_file, output_file, video_codec):
    command = [
        "ffmpeg",  # 命令本身
        "-y",  # 覆盖输出文件而不提示
        "-i",
        input_file,  # 输入文件
        "-c:v",
        video_codec,  # 视频编解码器
        "-preset",
        "slow",
        "-c:a",
        "aac",  # 音频编解码器
        output_file,  # 输出文件
    ]

    if video_codec == "hevc_nvenc" or video_codec == "h264_nvenc":
        command.extend(["-hwaccel_output_format", "cuda"])

    subprocess.run(command)


def process_folder(input_folder, output_folder, video_codec):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, _, files in os.walk(input_folder):
        rel_root = os.path.relpath(root, input_folder)
        output_root = os.path.join(output_folder, rel_root)

        if not os.path.exists(output_root):
            os.makedirs(output_root)

        for filename in files:
            if filename.lower().endswith(
                (".avi", ".mp4", ".mkv", ".mov", ".wmv", ".rmvb", ".flv")
            ):
                input_file = os.path.join(root, filename)
                show_name, episode_info, remaining_info = extract_file_parts(filename)

                video_info = get_video_info(input_file, video_codec)  # 获取视频信息

                output_base_name = (
                    f"{show_name} - {episode_info} - {remaining_info} - {video_info}"
                )
                # output_subfolder = os.path.join(output_root, rel_root)
                # output_file = os.path.join(output_subfolder, f"{output_base_name}.mkv")
                output_file = os.path.join(output_root, f"{output_base_name}.mkv")
                process_video(input_file, output_file, video_codec)


def get_common_resolution_name(width, height):
    resolutions = {
        (1920, 1080): "1080p",
        (1280, 720): "720p",
        # 可以添加其他分辨率的映射
    }

    if (width, height) in resolutions:
        return resolutions[(width, height)]
    else:
        return f"{width}x{height}"


def get_video_info(video_file, video_codec):
    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height,codec_name",
        "-of",
        "csv=p=0:nk=1",
        video_file,
    ]
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    stdout, _ = process.communicate()
    codec_name, width, height = stdout.strip().split(",")

    resolution_name = get_common_resolution_name(int(width), int(height))

    if video_codec in ["libx264", "h264_nvenc"]:
        codec_name = "h264"
    elif video_codec in ["libx265", "hevc_nvenc"]:
        codec_name = "h265"
    else:
        codec_name = video_codec.split("_")[0]  # 使用编码选项的第一部分作为编码名称

    return f"[{codec_name}][{resolution_name}]"


def get_output_folder(input_folder, suffix):
    output_folder = input("请输入输出文件夹位置（留空则在对应的输入文件夹加后缀）: ")
    if not output_folder:
        output_folder = create_output_folder(input_folder, suffix)
    return output_folder


def main():
    input_folder = input("请输入输入文件夹路径: ")

    choices = {
        "0": ("copy", "复制格式"),
        "1": ("libx264", "H.264 - CPU"),
        "2": ("h264_nvenc", "H.264 - N-Card"),
        "3": ("libx265", "H.265 - CPU"),
        "4": ("hevc_nvenc", "H.265 - N-Card"),
    }

    print("选择编码格式:")
    for key, value in choices.items():
        print(f"{key}. {value[1]}")

    choice = input("请输入选项: ")

    if choice in choices:
        video_codec, description = choices[choice]
        suffix = ""
        if video_codec != "copy":
            suffix = f"-{video_codec.split('_')[0].lower()}"
        output_folder = get_output_folder(input_folder, suffix)
    else:
        print("无效的选项。")
        exit()

    process_folder(input_folder, output_folder, video_codec)
    print("编码格式转换完成")


if __name__ == "__main__":
    main()
