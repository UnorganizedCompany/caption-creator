from dataclasses import dataclass
from parse import *
from typing import List


@dataclass
class CaptionInfo:
    index: int
    start_time: int
    end_time: int
    text: List[str]


def parse_time(time_str: str) -> tuple[int, int]:
    parsed = parse('{}:{}:{},{} --> {}:{}:{},{}', time_str)

    def convert_to_ms(hours, minutes, seconds, milliseconds):
        return int(milliseconds) + int(seconds) * 1000 + int(minutes) * 60 * 1000 + int(hours) * 60 * 60 * 1000

    start_time = convert_to_ms(*parsed[0:4])
    end_time = convert_to_ms(*parsed[4:8])

    return start_time, end_time


class FileReader:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.captions = []
        self.read()

    def read(self):
        with open(self.filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            blocks = content.split("\n\n")

            for block in blocks:
                lines = block.split("\n")
                if len(lines) >= 3 and lines[0].strip().isdigit():
                    idx = int(lines[0].strip())
                    start_time, end_time = parse_time(lines[1].strip())
                    text = lines[2].strip().split("\n")
                    self.captions.append(CaptionInfo(idx, start_time, end_time, text))

    def get_captions(self):
        return self.captions
