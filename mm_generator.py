import os
import caption
from file_reader import CaptionInfo
from typing import List


def generate_image(captions: List[CaptionInfo], output_path: str):
    for caption_info in captions:
        print(caption_info.text)
        tc = caption.CaptionCreator(caption_info.text)
        tc.save(f"{output_path}/{caption_info.index}.png")


def generate_video(captions: List[CaptionInfo], output_path: str, video_path: str = "./video"):
    meta_path = "video_meta.txt"
    with open(meta_path, "w") as file:
        latest_end_time = 0
        for caption_info in captions:
            start_time = caption_info.start_time
            end_time = caption_info.end_time
            blank_duration = start_time - latest_end_time

            if blank_duration > 0:
                file.write("file './blank.png'\n")
                file.write(f"duration {blank_duration}ms\n")

            file.write(f"file '{output_path}{caption_info.index}.png'\n")
            file.write(f"duration {end_time - start_time}ms\n")

            latest_end_time = end_time

    os.system(f"ffmpeg -f concat -safe 0 -i {meta_path} -vf \"settb=AVTB,fps=30\" -vcodec png -r 30 {video_path}.mov -y")
    os.remove(meta_path)
