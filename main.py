#!/usr/bin/env python
# -*- coding: utf-8 -*-

import caption 

import sys

if __name__=="__main__":
    srt_path = sys.argv[1]
    with open(srt_path, "r") as srt_file:
        state = "index" # index, time, text

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
                continue
            if state == "time":
                state = "text"
                continue
            if state == "text":
                if not "text" in srt:
                    srt["text"] = l
                else:
                    srt["text"] += l
