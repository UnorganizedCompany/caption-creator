#!/usr/bin/env python
# -*- coding: utf-8 -*-

import caption
import sys
import os
from parse import *


if __name__=="__main__":
    srt_path = sys.argv[1]
    output_filename = sys.argv[2] # should not include file extension
    with open(srt_path, "r") as srt_file:
        state = "index" # index, time, text
        caption_info = []
        latest_end_time = -1

        srt = {}
        for l in srt_file:
            if l.strip() == "":
                state = "index"
                if not "text" in srt:
                    continue
                print(srt["text"])
                tc = caption.CaptionCreator(srt["text"].strip().split("\n"))
                tc.save("./dist/"+srt['id']+".png")
                continue
            if state == "index":
                srt = {}
                srt["id"] = l.strip()
                state = "time"
                caption_info.append("file \'./dist/{0}.png\'".format(l.strip()))
                continue
            if state == "time":
                parsed_time = parse('{}:{}:{},{} --> {}:{}:{},{}', l)
                start_time = int(parsed_time[3]) + int(parsed_time[2]) * 1000 + int(parsed_time[1]) * 60 * 1000 + \
                    int(parsed_time[0]) * 60 * 60 * 1000
                end_time = int(parsed_time[7]) + int(parsed_time[6]) * 1000 + int(parsed_time[5]) * 60 * 1000 + \
                    int(parsed_time[4]) * 60 * 60 * 1000
                if (latest_end_time > 0 and start_time > latest_end_time):
                    caption_info.insert(len(caption_info) - 1, "file \'./blank.png\'")
                    caption_info.insert(len(caption_info) - 1, "duration {0}ms".format(start_time - latest_end_time))
                duration = end_time - start_time
                caption_info.append("duration {0}ms".format(duration))
                latest_end_time = end_time
                state = "text"
                continue
            if state == "text":
                if not "text" in srt:
                    srt["text"] = l
                else:
                    srt["text"] += l

    caption_info.append("file \'./blank.png\'")
    caption_info_filename = "{0}.txt".format(output_filename)
    caption_video_filename = "{0}.mov".format(output_filename)
    f = open(caption_info_filename, "w")
    for info in caption_info:
        f.write(info + "\n")
    f.close()

    os.system("ffmpeg -f concat -safe 0 -i {0} -vf \"settb=AVTB,fps=30\" -vcodec png -r 30 {1}.mov -y" \
        .format(caption_info_filename, caption_video_filename)