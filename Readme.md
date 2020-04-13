# Autoaugment说明文档
## 随即调用图片处理的policy的类的说明：
#### 代码说明：
这里设立了两个类。  
一个类是SubPolicy，这个类里面设定了16种图片处理的方法，每个方法都在下面有详细讲解（shearX与Y算作两个）。传参是6个参数分别是（概率1，处理方式1，处理程度1，概率2，处理方式2，处理程度2），调用时会比对概率1和概率2的值并执行概率大的那个处理方式。  
另一个一个类是ImageNetPolicy，这个类里设立了25中处理策略，每个策略对应SubPolicy的一组参数，调用时会随机选择其中的一个策略，选中之后这个策略的内容是调用SubPolicy，最终会根据这个策略中的6个参数对图像进行处理，做到了随机选择策略的目的。

####图片效果：
例如这里给出一段示例效果和代码。
代码：

    def main():
    #定向使用sample_pairng
    img = Image.open("./imgs/time1.jpg")
    img2 = Image.open("./imgs/time2.jpg")
    #img.show()
    samp= SubPolicy(1,"sample_paring", 9,0,"rotate",9)
    samp(img,img2).show()
    #随机调用一个policy
    impolicy = ImageNetPolicy()
    impolicy(img).show()
    
	if __name__ == '__main__':
	main() 
     

<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/time1.jpg" title="原图" width=300>
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/sample.jpg" title="sample" width=300>

这里可以看到随机选中的是调用autocontrast的policy
***
## 16种图片处理方法用于扩充数据集：
### 1.shearX/Y：图片沿着X轴/Y轴方向扭转
#### 代码实现：
    
	magnitude=9
    img = image.open("time.jpg")
    shearx = img.transform( img.size, image.affine, (1, magnitude , 0, 0, 1, 0))
    shearx.show()
	magnitude=0.2
	sheary = img.transform(img.size, image.affine, (1, 0, 0,magnitude, 1, 0))
    sheary.show()

这里使用的是pil库自带的transform函数，这里transform函数的各个参数如下：

<center>img.transform（大小，仿射，数据，过滤器） ⇒图像</center>
对图像应用仿射变换，并将结果放入具有给定大小的新图像中。  
数据是一个6元组（a，b，c，d，e，f），其中包含仿射变换矩阵的前两行。对于输出图像中的每个像素（x，y），从输入图像中的位置（a x + b y + c，d x + e y + f）取新值，四舍五入到最接近的像素。  
这个函数作用比较大，可以用于缩放，平移，旋转，剪切多个功能。但是需要对仿射矩阵有一定了解，不是很直观。  
shearx的时候相当于对于原图的（x，y）位置的图像的y坐标保持不变，x坐标随着y的增大映射到对应的magnitudex,也就是说输出图像的（x,y）位置的像素应该由原图像（x+by,y）处的像素而来。所以仿射矩阵应该形如（1，magnitude,0,0,1,0）  
#### 参数影响：
在上述函数中所设置的参数magnitude的大小会影响图片的“扭转”程度，如果magnitude越大就是说输出图像中的(x,y)会由原图像中相对(x,y)越远的位置的像素来替代，那么就是说扭转程度会更大.
####图片效果：
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/time1.jpg" title="原图" width=300>
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/shearX.jpg" title="shearX" width=300>
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/shearY.jpg" title="shearY" width=300>

### 2.translateX/Y：沿着x轴/y轴平移
#### 代码实现：
    
	img = Image.open("time.jpg")
    magnitude = 90
    translateX = img.transform(
    img.size, Image.AFFINE, (1, 0, magnitude, 0, 1, 0))
    translateX.show()
#### 参数影响：
这里的参数影响比较简单，了解了tranform函数的功能之后就很容易了，magnitude越大，代表沿着轴平移越多
####图片效果：
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/time1.jpg" title="原图" width=300>
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/translateX.jpg" title="translateX" width=300>

### 3.rotate：旋转图片
#### 代码实现：
    
	img = Image.open("time.jpg")
	magnitude = 30
	rotate = img.rotate(magnitude)
	rotate.show()

#### 参数影响：
这里的rotate函数的原理是传入一个角度，就是绕中心旋转magnitude度数。
####图片效果：
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/time1.jpg" title="原图" width=300>
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/rotate.jpg" title="rotate" width=300>

### 3.rotate：旋转图片
#### 代码实现：
    
	img = Image.open("time.jpg")
    magnitude = 0.9
    color = ImageEnhance.Color(img).enhance(1+magnitude)
    color.show()


#### 参数影响：
这里的magnitude是调整颜色饱和度的，加1是因为当括号里等于1时，显示原图，所以1+magnitude就可以以原图为基准来调整颜色的饱和度。
####图片效果：
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/time1.jpg" title="原图" width=300>
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/color1.jpg" title="color(magnitude=0.9)" width=300>
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/color2.jpg" title="color(magnitude=-0.9)" width=300>

### 4.color：调整图片颜色饱和度
#### 代码实现：
    
	img = Image.open("time.jpg")
	magnitude = 30
	rotate = img.rotate(magnitude)
	rotate.show()

#### 参数影响：
这里的rotate函数的原理是传入一个角度，就是绕中心旋转magnitude度数。
####图片效果：
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/time1.jpg" title="原图" width=300>
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/rotate.jpg" title="rotate" width=300>

### 5.contrast: 调整图像的对比度。类似于调整彩色电视机的对比度
#### 代码实现：
    
	img = Image.open("time.jpg")
    magnitude = 0.9
    contrast = ImageEnhance.Contrast(img).enhance(1 + magnitude)
    contrast.show()


#### 参数影响：
同color，contrast(img).enhance()函数中传参数为0，代表无对比度，为1代表原图，所以这里用1+magnitude就可以用magnitude来控制对比度增强或是减弱。
####图片效果：
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/time1.jpg" title="原图" width=300>
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/contrast1.jpg" title="contrast(magnitude=0.9)" width=300>
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/contrast2.jpg" title="contrast(magnitude=-0.9)"width=300>

### 6.brightness: 调整图像的亮度
#### 代码实现：
    
	img = Image.open("time.jpg")
    magnitude = 0.5
    brightness= ImageEnhance.Brightness(img).enhance(1 + magnitude)
    brightness.show()


#### 参数影响：
ImageEnhance.Brightness(img).enhance(1 + magnitude)中的magnitude=-1时代表亮度为0，为1时表示亮度加倍。
####图片效果：
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/time1.jpg" title="原图" width=300>
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/brightness1.jpg" title="brightness(magnitude=0.9)" width=300>
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/brightness2.jpg" title="brightness(magnitude=-0.5)"width=300>

### 7.sharpness：用于调整图像的锐度
#### 代码实现：
    
	img = Image.open("time.jpg")
	magnitude = 10
	sharpness = ImageEnhance.Sharpness(img).enhance(1 + magnitude)
	sharpness.show()

#### 参数影响：
传参为0（magnitude=-1）代表图片模糊，传参为2（magnitude=1）代表整个锐度增强一倍。
####图片效果：
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/time1.jpg" title="原图" width=300>
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/sharpness1.jpg" title="sharpness(magnitude=-10)" width=300>
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/sharpness2.jpg" title="sharpness(magnitude=10)"width=300>

### 8.autocontrast：最大图像对比度
#### 代码实现：
    
	img = Image.open("time.jpg")
    magnitude = 20
    autocontrast = ImageOps.autocontrast(img,magnitude)
    autocontrast.show()

#### 参数影响：
这个函数计算一个输入图像的直方图，从这个直方图中去除最亮和最暗的百分之（magnitude），然后重新映射图像，以便保留的最暗像素变为黑色，即0，最亮的变为白色，即255。
####图片效果：
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/time1.jpg" title="原图" width=300>
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/autocontrast1.jpg" title="autocontrast(magnitude=10)" width=300>
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/autocontrast2.jpg" title="autocontrast(magnitude=20)"width=300>

### 9.posterize: 色彩分离
#### 代码实现：
    
	img = Image.open("time.jpg")
    magnitude = 2
    posterize = ImageOps.posterize(img, magnitude)
    posterize.show()

#### 参数影响：
将每个颜色通道上变量magnitude对应的低(8-bits)个bit置0。变量magnitude的取值范围为[0，8]；当变量magnitude为2时，将每个颜色通道的像素值低6bit清0，保留剩下的2 bit位。即124=二进制1111100，其处置之后为，二进制1000000=32
####图片效果：
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/time1.jpg" title="原图" width=300>
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/posterize1.jpg" title="posterize(magnitude=2)" width=300>
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/posterize2.jpg" title="posterize(magnitude=4)"width=300>

### 10.solarize: (曝光效果)在指定的阈值范围内，反转所有的像素点。
#### 代码实现：
    
	img = Image.open("time.jpg")
    magnitude = 128
    solarize = ImageOps.solarize(img, magnitude)
    solarize.show()

#### 参数影响：
大于magnitude的值做反转（二进制位取反）所以magnitude的值越大，反转的像素越少。
####图片效果：
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/time1.jpg" title="原图" width=300>
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/posterize1.jpg" title="solarize(magnitude=200)" width=300>
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/posterize2.jpg" title="solarize(magnitude=128)"width=300>

### 11.equalize: 均衡图像的直方图
#### 代码实现：
    
	img = Image.open("time.jpg")
    equalize = ImageOps.equalize(img)
    equalize.show()

#### 参数影响：
无参数，就是把原图像的灰度值均衡化。
####图片效果：
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/time1.jpg" title="原图" width=300>
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/posterize1.jpg" title="equalize(magnitude=200)" width=300>

### 12.invert: 将输入图像转换为反色图像
#### 代码实现：
    
	img = Image.open("time.jpg")
    magnitude = 128
    invert = ImageOps.invert(img)
    invert.show()

#### 参数影响：
无参数，算法就是将像素二进制位取反。
####图片效果：
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/time1.jpg" title="原图" width=300>
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/invert.jpg" title="invert" width=300>

### 13.cutout：随机选取一篇矩形区域并覆盖
#### 代码实现：
    
	def cut_out(img,magnitude):
        draw =ImageDraw.Draw(img)
        x1 = random.random()*(img.size[0]-100)
        y1 = random.random()*(img.size[1]-100)
        draw.rectangle([x1, y1,x1+magnitude, y1+magnitude],fill=(0,0,0,0))
        return img

#### 参数影响：
这个在PIL库中没有现成的函数，不过也很简单，就是随机生成位置，然后用ImageDraw画出矩形就可以了。这里magnitude是矩形的长宽
####图片效果：
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/time1.jpg" title="原图" width=300>
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/cutout.jpg" title="cutout" width=300>

### 14.sample paring：同一个数据包里的两张图像进行融合
#### 代码实现：
    
	def sample_paring(img1,img2, magnitude):
        for i in range(img1.size[0]):
            for j in range(img1.size[1]):
                r1,g1,b1 = img1.getpixel((i,j))
                r2,g2,b2 = img2.getpixel((i,j))
                img1.putpixel((i,j),(int(magnitude*r1+(1-magnitude)*r2),
                               int(magnitude*g1+(1-magnitude)*g2),
                               int(magnitude*b1+(1-magnitude)*b2)))
        return img1


#### 参数影响：
这里的融合方式是两张图片对应位置的像素取加权平均，magnitude就是权值。
####图片效果：
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/time1.jpg" title="原图1" width=300>
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/time2.jpg" title="原图2" width=300>
<img src="https://raw.githubusercontent.com/SIMONLQY/task1/master/imgs/sample_paring.jpg" title="sample_paring" width=300>
