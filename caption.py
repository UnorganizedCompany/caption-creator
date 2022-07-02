#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import random
import sys

class CaptionCreator():
    space_between_name_text = 10
    space_between_lines = 10
    space_bootom = 50
    def __init__(self, texts):
        namefnt = ImageFont.truetype("./DOSMyungjo.ttf", encoding="UTF-7", size=65)
        name = ""
        if ":" in texts[0]:
            splitted = texts[0].split(":")
            name = splitted[0].strip()
            texts[0] = ":".join(splitted[1:])
        nameW, nameH = namefnt.getsize(name)

        fnt = ImageFont.truetype("./DOSMyungjo.ttf", encoding="UTF-8", size=65)
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

        capW = nameW + self.space_between_name_text + textW
        capH = textH if textH > nameH else nameH

        self.im = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))

        capX = (1920-capW)//2
        capY = 1080-(self.space_bootom + capH)

        # color 242, 242, 242 for name
        pxs = self.im.load()
        for y in range(nameH):
            for x in range(nameW):
                pxs[capX+x, capY+y] = (242, 242, 242)
        
        pxs = self.im.load()
        for y in range(capH-nameH):
            for x in range(nameW):
                pxs[capX+x, capY+nameH+y] = (0, 0, 0, 0)

        for y in range(textH):
            for x in range(capW-nameW):
                pxs[capX+nameW+x, capY+y] = (0, 0, 0, 128)

        draw = ImageDraw.Draw(self.im)
        draw.multiline_text((capX,capY), name, font=fnt, fill=(0, 0, 0))
       
        draw.multiline_text((capX+nameW+self.space_between_name_text,capY), "\n".join(texts), font=fnt, fill=(255, 255, 255), 
                                align="left", spacing=self.space_between_lines)

    def show(self):
        self.im.show()

    def save(self, path):
        self.im.save(path, "PNG")
