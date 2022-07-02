#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import random
import sys

class CaptionCreator():
    space_between_name_text = 10
    space_between_lines = 10
    def __init__(self, texts):
        namefnt = ImageFont.truetype("./DOSMyungjo.ttf", encoding="UTF-7", size=50)
        name = ""
        if ":" in texts[0]:
            splitted = texts[0].split(":")
            name = splitted[0].strip()
            texts[0] = ":".join(splitted[1:])
        nameW, nameH = namefnt.getsize(name)

        fnt = ImageFont.truetype("./DOSMyungjo.ttf", encoding="UTF-8", size=50)
        textH = 0
        textW = -1
        for s in texts:
            (w,h) = fnt.getsize(s)
            if w > textW:
                textW = w
            textH += h
        #  while fnt.getsize(texts[0])[0] < maxW:
            #  texts[0] += " "

        textH += self.space_between_lines*(len(texts)-1)

        imgW = nameW + self.space_between_name_text + textW
        imgH = textH if textH > nameH else nameH

        self.im = Image.new("RGBA", (imgW, imgH), (0, 0, 0, 128))

        # color 242, 242, 242 for name
        pxs = self.im.load()
        for y in range(nameH):
            for x in range(nameW):
                pxs[x, y] = (242, 242, 242)
        
        pxs = self.im.load()
        for y in range(imgH-nameH):
            for x in range(nameW):
                pxs[x, nameH+y] = (0, 0, 0, 0)

        draw = ImageDraw.Draw(self.im)
        draw.multiline_text((0,0), name, font=fnt, fill=(0, 0, 0))
       
        draw.multiline_text((nameW+self.space_between_name_text,0), "\n".join(texts), font=fnt, fill=(255, 255, 255), 
                                align="left", spacing=self.space_between_lines)

    def show(self):
        self.im.show()

    def save(self, path):
        self.im.save(path, "PNG")
