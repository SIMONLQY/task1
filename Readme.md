# Autoaugment说明文档
## 16种图片处理方法用于扩充数据集：
### 1.shearX/Y：图片沿着X轴/Y轴方向扭转
#### 代码实现：
``` 
	magnitude=9
	img = Image.open("time.jpg")
	shearX = img.transform( img.size, Image.AFFINE, (1, magnitude , 0, 0, 1, 0))
	shearX.show()
	magnitude=0.2
	shearY = img.transform(img.size, Image.AFFINE, (1, 0, 0,magnitude, 1, 0))
	shearY.show()
```
### 2.
