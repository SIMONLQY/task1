# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 08:20:39 2020

@author: Simon
"""
from autoaugment import SubPolicy
from autoaugment import ImageNetPolicy
from PIL import Image
    
    
def main():
    #定向使用sample_pairng
    img = Image.open("./imgs/time1.jpg")
    img2 = Image.open("./imgs/time2.jpg")
#    img.show()
#    samp= SubPolicy(1,"sample_paring", 9,0,"rotate",9)
#    samp(img,img2).show()
    #随机调用一个policy
    impolicy = ImageNetPolicy()
    impolicy(img).show()

if __name__ == '__main__':
    main()