# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 12:24:22 2020

@author: Simon
"""

from PIL import Image, ImageEnhance, ImageOps, ImageDraw
import numpy as np
import random

class SubPolicy(object):
    def __init__(self,operation, magnitude_idx,fillcolor=(128, 128, 128)):
        ranges = {
            "shearX": np.linspace(0, 0.3, 10),
            "shearY": np.linspace(0, 0.3, 10),
            "translateX": np.linspace(0, 150 / 331, 10),
            "translateY": np.linspace(0, 150 / 331, 10),
            "rotate": np.linspace(0, 30, 10),
            "color": np.linspace(0.0, 0.9, 10),
            "posterize": np.round(np.linspace(8, 4, 10), 0).astype(np.int),
            "solarize": np.linspace(256, 0, 10),
            "contrast": np.linspace(0.0, 0.9, 10),
            "sharpness": np.linspace(0.0, 0.9, 10),
            "brightness": np.linspace(0.0, 0.9, 10),
            "autocontrast": [0] * 10,
            "cutout": np.linspace(0,60,10),
            "sample_paring":np.linspace(0,0.4,10),
            "equalize": [0] * 10,
            "invert": [0] * 10
        }
        def cut_out(img,magnitude):
            draw =ImageDraw.Draw(img)
            x1 = random.random()*(img.size[0]-100)
            y1 = random.random()*(img.size[1]-100)
            draw.rectangle([x1, y1,x1+magnitude, y1+magnitude],fill=(0,0,0,0))
            return img
        def sample_paring(img1,img2, magnitude):
            for i in range(img1.size[0]):
                for j in range(img1.size[1]):
                    r1,g1,b1 = img1.getpixel((i,j))
                    r2,g2,b2 = img2.getpixel((i,j))
                    img1.putpixel((i,j),(int(magnitude*r1+(1-magnitude)*r2),
                                   int(magnitude*g1+(1-magnitude)*g2),
                                     int(magnitude*b1+(1-magnitude)*b2)))
            return img1
        
        func = {
            "shearX": lambda img, magnitude: img.transform(
                img.size, Image.AFFINE, (1, magnitude* random.choice([-1, 1]) , 0, 0, 1, 0),
                Image.BICUBIC, fillcolor=fillcolor),
            "shearY": lambda img, magnitude: img.transform(
                img.size, Image.AFFINE, (1, 0, 0, magnitude * random.choice([-1, 1]), 1, 0),
                Image.BICUBIC, fillcolor=fillcolor),
            "translateX": lambda img, magnitude: img.transform(
                img.size, Image.AFFINE, (1, 0, magnitude * img.size[0] * random.choice([-1, 1]), 0, 1, 0),
                fillcolor=fillcolor),
            "translateY": lambda img, magnitude: img.transform(
                img.size, Image.AFFINE, (1, 0, 0, 0, 1, magnitude * img.size[1] * random.choice([-1, 1])),
                fillcolor=fillcolor),
            "rotate": lambda img, magnitude:img.rotate(magnitude*random.choice([-1, 1])),
            "color": lambda img, magnitude: ImageEnhance.Color(img).enhance(1 + magnitude * random.choice([-1, 1])),
            "contrast": lambda img, magnitude: ImageEnhance.Contrast(img).enhance(
                1 + magnitude * random.choice([-1, 1])),
            "sharpness": lambda img, magnitude: ImageEnhance.Sharpness(img).enhance(
                1 + magnitude * random.choice([-1, 1])),
            "brightness": lambda img, magnitude: ImageEnhance.Brightness(img).enhance(
                1 + magnitude * random.choice([-1, 1])),
            "autocontrast": lambda img, magnitude: ImageOps.autocontrast(img),
            "posterize": lambda img, magnitude: ImageOps.posterize(img, magnitude),
            "solarize": lambda img, magnitude: ImageOps.solarize(img, magnitude),
            "equalize": lambda img, magnitude: ImageOps.equalize(img),
            "invert": lambda img, magnitude: ImageOps.invert(img),
            "cutout":lambda img,magnitude:cut_out(img,magnitude),
            "sample_paring":lambda img,img2,magnitude:sample_paring(img,img2,magnitude)
        }
        self.operation_name=operation
        self.operation = func[operation]
        self.magnitude = ranges[operation][magnitude_idx]
        


    def __call__(self, img,  img2=None):
        if self.operation_name=="sample_paring":
            img = self.operation(img, img2, self.magnitude)
        else:
            img = self.operation(img, self.magnitude)
        return img
    




