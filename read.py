from PIL import Image
"""
    用来读取图片上每个像素点的rpg值
"""
# 打开图像文件，不加扩展名
image_path = "test.bmp"
img = Image.open(image_path)

# 获取图像的宽度和高度
width, height = img.size

# 获取图像的像素点信息
pixels = list(img.getdata())

# 遍历像素点列表获取每个像素的颜色信息
for y in range(height):
    for x in range(width):
        pixel = img.getpixel((x, y))
        print(pixel)

# 关闭图像文件
img.close()
