#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import yaml


class CaptionCreator():
    with open('color_map.yml') as c:
        color_map = yaml.load(c, Loader=yaml.FullLoader)

    screen_width = 1920
    screen_height = 1080
    text_padding = 10
    space_between_lines = 10
    space_bottom = 50
    border_width = 8
    image_resizing_size = 150  # max(height, width) of image will set to image_size

    def __init__(self, texts):
        image_name = ""
        if ":" in texts[0]:
            splitted = texts[0].split(":")
            image_name = splitted[0].strip()
            texts[0] = ":".join(splitted[1:])

        fnt = ImageFont.truetype("./DOSMyungjo.ttf", encoding="UTF-8", size=65)
        text_height = 0
        text_width = -1
        for s in texts:
            (w, h) = fnt.getsize(s)
            if w > text_width:
                text_width = w
            text_height += h

        text_height += self.text_padding * 2
        text_height += self.space_between_lines * (len(texts) - 1)
        text_width += self.text_padding * 2

        image = Image.open(f"./image/{image_name}.png")
        image_resizing_ratio = self.image_resizing_size / max(image.height, image.width)
        image_height = int(image.height * image_resizing_ratio)
        image_width = int(image.width * image_resizing_ratio)
        resized_img = image.resize((image_height, image_width))

        self.im = Image.new("RGBA", (self.screen_width, self.screen_height), (0, 0, 0, 0))

        text_x = (self.screen_width - text_width - image_width) // 2 + image_width
        text_y = self.screen_height - self.space_bottom - text_height
        image_x = text_x - image_width - self.border_width
        image_y = text_y - (image_height - text_height) // 2

        pxs = self.im.load()

        for y in range(text_height):
            for x in range(text_width):
                pxs[text_x + x, text_y + y] = (0, 0, 0, 128)

        if image_name in self.color_map:
            r = self.color_map[image_name]["r"]
            g = self.color_map[image_name]["g"]
            b = self.color_map[image_name]["b"]
            a = self.color_map[image_name]["a"]

            # fill upper, lower border
            for y in range(self.border_width):
                for x in range(text_width):
                    pxs[text_x + x, text_y - y - 1] = (r, g, b, a)
                    pxs[text_x + x, text_y + text_height + y] = (r, g, b, a)

            # fill left, right border
            for y in range(text_height):
                for x in range(self.border_width):
                    pxs[text_x - x - 1, text_y + y] = (r, g, b, a)
                    pxs[text_x + text_width + x, text_y + y] = (r, g, b, a)

            # fill corner
            for y in range(self.border_width // 2):
                for x in range(self.border_width // 2):
                    pxs[text_x - x - 1, text_y - y - 1] = (r, g, b, a)
                    pxs[text_x + x, text_y + y] = (r, g, b, a)
                    pxs[text_x + text_width + x, text_y - y - 1] = (r, g, b, a)
                    pxs[text_x + text_width - x - 1, text_y + y] = (r, g, b, a)
                    pxs[text_x - x - 1, text_y + text_height + y] = (r, g, b, a)
                    pxs[text_x + x, text_y + text_height - y - 1] = (r, g, b, a)
                    pxs[text_x + text_width + x, text_y + text_height + y] = (r, g, b, a)
                    pxs[text_x + text_width - x - 1, text_y + text_height - y - 1] = (r, g, b, a)

        draw = ImageDraw.Draw(self.im)
        draw.multiline_text((text_x + self.text_padding, text_y + self.text_padding), "\n".join(texts), font=fnt,
                            fill=(255, 255, 255), align="left", spacing=self.space_between_lines)

        image_layer = Image.new("RGBA", (self.screen_width, self.screen_height), (0, 0, 0, 0))
        image_layer.paste(resized_img, (image_x, image_y))
        self.im = Image.alpha_composite(self.im, image_layer)

    def show(self):
        self.im.show()

    def save(self, path):
        self.im.save(path, "PNG")
