# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 08:20:39 2020

@author: Simon
"""
from autoaugment import SubPolicy
from PIL import Image
    
    
def main():
    #引入图片
    img = Image.open("time1.jpg")
    img2 = Image.open("time2.jpg")
    img.show()
    samp= SubPolicy("sample_paring", 9)
    samp.__call__(img,img2).show()

if __name__ == '__main__':
    main()