# Copyright (c) 2024 bilive.
# Copyright (c) 2025 auto-slice-video

import subprocess
import os


def format_time(seconds):
    """Format seconds to hh:mm:ss."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02}:{m:02}:{s:02}"


def slice_video(video_path, output_path, start_time, duration):
    """Slice the video using ffmpeg."""
    duration = format_time(duration)
    command = [
        "ffmpeg",
        "-y",
        "-ss",
        format_time(start_time),
        "-i",
        video_path,
        "-t",
        duration,
        "-map_metadata",
        "0",  # 保留原始视频的 metadata
        "-c:v",
        "copy",
        "-c:a",
        "copy",
        output_path,
    ]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False


def add_mllm_title_to_metadata(video_path, mllm_title):
    """Add MLLM generated title to video metadata as 'generate' field."""
    if not os.path.exists(video_path):
        print(f"Video file not found: {video_path}")
        return False

    if not mllm_title:
        print("No MLLM title provided")
        return False

    # 创建临时文件路径
    temp_path = video_path + ".temp"

    # 使用 ffmpeg 添加 generate 字段到 metadata
    command = [
        "ffmpeg",
        "-y",
        "-i",
        video_path,
        "-c",
        "copy",
        "-metadata",
        f"generate={mllm_title}",
        temp_path,
    ]

    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)

        # 替换原文件
        os.replace(temp_path, video_path)
        print(f"Successfully added MLLM title to metadata: {mllm_title}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error adding metadata: {e.stderr}")
        # 清理临时文件
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return False
