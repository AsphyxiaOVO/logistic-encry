from PIL import Image
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
import os
def logistic(r, x0, steps):
    """
    生成Logistic映射方程的值


    参数：
    - r: 映射的参数，大于3.57是系统进入混沌状态，值的范围通常为[0，4]
    - x0: 初始值范围为[0,1]
    - steps: 生成的步数

    返回值：
    - x_values: 生成的值的列表
    """
    x_values = [x0]
    values=[]
    for _ in range(steps - 1):
        x_next = r * x_values[-1] * (1 - x_values[-1])
        x_values.append(x_next)
    for i in range(steps - 1):
        values.append(int(x_values[i]*255))#将生成的值扩大255倍使其适应rgb的异或运算
    return values

def XOR(x,y):
    '''
    定义异或加解密函数，明文异或后为密文，密文异或后为明文,二进制和十进制下结果相同
    :x:十进制
    :y:十进制
    :return:十进制转为8位二进制按位异或后转为十进制
    '''
    # 将两个数转换为8位二进制表示
    binary_x = format(x, '08b')
    binary_y = format(y, '08b')
    out_binary=""
    # 执行异或运算
    for i in range(8):
        if(binary_x[i]==binary_y[i]):
            out_binary+="0"
        else:
            out_binary+="1"
    #print(out_binary)
    result_binary=int(out_binary,2)#将二进制转换为十进制
    return result_binary

def encrypt(image_path, output_path, result_values, frquency):
    """
    定义加解密函数，由于使用异或计算，加密后再次运行为解密成果
    :param image_path: 需要加密的图片路径
    :param output_path: 加密后的图片保存的路径
    :param result_values: 生成的混沌序列的数组
    :param frquency:加密轮数
    :return:
    """
    #打开原始图片
    extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    for ext in extensions:
        try:
            image = Image.open(image_path + ext)
            break
        except FileNotFoundError:
            continue
    else:
        raise FileNotFoundError(f"未找到名为 {image_path} 的文件。")

    # 转换图片格式为BMP并保存
    bmp_image_path = image_path.rsplit('.', 1)[0] + '.bmp'
    image.save(bmp_image_path, format='BMP')

    # 重新打开保存后的BMP图片
    image = Image.open(bmp_image_path)

    width, height = image.size
    pixels = image.load()
    i, j = 0, 1  # i控制每一轮的混沌序列依次给rgb，j控制加密轮数
    while(j <= frquency):
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                r = XOR(r, result_values[i + (height * width) * 0])  # 红色通道进行异或运算
                g = XOR(g, result_values[i + (height * width) * 1])  # 绿色通道进行异或运算
                b = XOR(b, result_values[i + (height * width) * 2])  # 蓝色通道进行异或运算
                pixels[x, y] = (r, g, b)
                i += 1
        j += 1
    image.save(output_path + '.bmp', format='BMP')


class EncryptorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 创建标签和文本框
        self.rLabel = QLabel("映射参数 r (大于3.57):")
        self.rInput = QLineEdit(self)
        self.x0Label = QLabel("初始值 x0:")
        self.x0Input = QLineEdit(self)
        self.frequencyLabel = QLabel("加密轮数:")
        self.frequencyInput = QLineEdit(self)
        self.imagePathLabel = QLabel("图片文件名:")
        self.imagePathInput = QLineEdit(self)
        self.outputPathLabel = QLabel("保存后的文件名:")
        self.outputPathInput = QLineEdit(self)

        # 创建按钮
        self.encryptButton = QPushButton("加密", self)
        self.decryptButton = QPushButton("解密", self)

        # 添加组件到布局
        layout.addWidget(self.rLabel)
        layout.addWidget(self.rInput)
        layout.addWidget(self.x0Label)
        layout.addWidget(self.x0Input)
        layout.addWidget(self.frequencyLabel)
        layout.addWidget(self.frequencyInput)
        layout.addWidget(self.imagePathLabel)
        layout.addWidget(self.imagePathInput)
        layout.addWidget(self.outputPathLabel)
        layout.addWidget(self.outputPathInput)
        layout.addWidget(self.encryptButton)
        layout.addWidget(self.decryptButton)

        # 设置布局
        self.setLayout(layout)

        # 连接按钮的点击事件
        self.encryptButton.clicked.connect(self.encrypt)
        self.decryptButton.clicked.connect(self.decrypt)

        # 设置窗口属性
        self.setWindowTitle('图片加解密工具')
        self.setGeometry(300, 300, 350, 250)

    def encrypt(self):
        # 加密逻辑
        try:
            r = float(self.rInput.text())
            x0 = float(self.x0Input.text())
            frquency = int(self.frequencyInput.text())
            image_path = self.imagePathInput.text()
            output_path = self.outputPathInput.text()

            # 读取图片的宽和高
            extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
            for ext in extensions:
                try:
                    image = Image.open(image_path + ext)
                    break
                except FileNotFoundError:
                    continue
            else:
                raise FileNotFoundError(f"未找到名为 {image_path} 的文件。")

            width, height = image.size
            result_values = logistic(r=r, x0=x0, steps=(width * height + 1) * 3 * frquency)
            encrypt(image_path, output_path, result_values, frquency)
            QMessageBox.information(self, '成功', '加密成功，文件已保存！')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'发生错误: {e}')

    def decrypt(self):
        # 解密逻辑，与加密类似
        try:
            r = float(self.rInput.text())
            x0 = float(self.x0Input.text())
            frquency = int(self.frequencyInput.text())
            image_path = self.imagePathInput.text()
            output_path = self.outputPathInput.text()

            # 读取图片的宽和高
            extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
            for ext in extensions:
                try:
                    image = Image.open(image_path + ext)
                    break
                except FileNotFoundError:
                    continue
            else:
                raise FileNotFoundError(f"未找到名为 {image_path} 的文件。")

            width, height = image.size
            result_values = logistic(r=r, x0=x0, steps=(width * height + 1) * 3 * frquency)
            encrypt(image_path, output_path, result_values, frquency)
            QMessageBox.information(self, '成功', '解密成功，文件已保存！')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'发生错误: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EncryptorWindow()
    ex.show()
    sys.exit(app.exec_())