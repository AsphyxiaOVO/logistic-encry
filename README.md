# logistic-encry

> 中文：基于 Logistic 混沌映射的图像加密与解密实验  
> English: An image encryption and decryption experiment based on the chaotic Logistic map

## 中文说明

### 项目简介

本项目是 `2023-2024-1`《密码工程》课程设计，核心思路是使用 Logistic 映射生成混沌序列，并把该序列作为流密钥，对彩色图像执行多轮 XOR 加密。仓库中同时提供了命令行版本、PyQt5 图形界面版本，以及用于结果评估的 PSNR / SSIM 脚本。

### 核心方法

1. 使用 Logistic 映射生成序列：

   `x_(n+1) = r * x_n * (1 - x_n)`

2. 当 `r > 3.57` 时，系统进入混沌状态，序列具备较强伪随机性。
3. 将生成的序列缩放到 `0-255`，分别与图像像素的 `R / G / B` 通道做异或运算。
4. 因为 XOR 具有可逆性，解密时只需要使用相同的 `r`、`x0` 和加密轮数再次执行一次异或。

### 仓库结构

| 文件 | 说明 |
| --- | --- |
| `logistic.py` | 命令行版图像加密 / 解密主程序 |
| `pyqt5.py` | PyQt5 图形界面版加密 / 解密工具 |
| `psnr.py` | 计算原图与加密图之间的 PSNR |
| `ssim.py` | 计算原图与加密图之间的 SSIM |
| `read.py` | 读取并打印图像像素值的辅助脚本 |
| `origin.bmp`, `test.bmp` | 示例原始图像 |
| `encrypted.bmp`, `decrypted.bmp`, `output.bmp`, `reverse.bmp` | 示例输出结果 |
| `encrypted.tiff`, `test.tiff`, `十轮.bmp`, `二十轮.bmp` | 不同格式与不同轮数下的实验结果 |

### 运行环境

推荐使用 `Python 3.9+`，常用依赖如下：

```bash
pip install pillow pyqt5 numpy scikit-image tifffile matplotlib
```

说明：

- `psnr.py` 中导入了 `SimpleITK`，但当前脚本主体并未实际使用它。
- `random`、`os`、`sys` 等为 Python 标准库，无需额外安装。

### 使用方法

#### 1. 命令行版本

```bash
python logistic.py
```

脚本会依次要求输入：

- `r`：Logistic 映射参数，建议大于 `3.57`
- `x0`：初始值，通常位于 `(0, 1)`
- `frquency`：加密轮数
- `image_path`：输入图像文件名主体
- `output_path`：输出图像文件名主体

说明：

- 当前代码会按 `.jpg`、`.jpeg`、`.png`、`.bmp`、`.tiff` 的顺序自动尝试拼接扩展名，因此更适合输入“不带扩展名”的文件名主体。

#### 2. 图形界面版本

```bash
python pyqt5.py
```

图形界面支持直接填写参数并执行加密或解密，适合课程展示和快速实验。

#### 3. 图像质量评估

```bash
python psnr.py
python ssim.py
```

这两个脚本默认比较仓库中已有的测试文件。如果需要评估其他图片，可以直接修改脚本中的文件名。

### 实验结论

- 当 `r` 进入混沌区间后，生成的密钥流能够明显打乱原图像素分布。
- 加密图像与原图的 `PSNR` 明显降低，`SSIM` 接近 `0`，说明二者的结构相关性显著下降。
- 只要参数一致，重新执行一次 XOR 就可以恢复原图，从而验证该方案的可逆性。

### 项目特点与局限

- 适合用于展示 Logistic 混沌映射在图像加密中的基本思路。
- 同时提供 CLI 和 GUI 两种交互方式，便于课程实验与演示。
- 当前实现更偏向教学和复现，不是工程级的完整安全加密系统。
- 评估脚本和输入文件名存在一定“示例数据绑定”，首次使用时建议直接基于仓库现有文件复现实验。

## English Overview

### Summary

This repository is a course-design project for image encryption based on the Logistic map. It generates a chaotic sequence from the Logistic equation and uses that sequence as a stream key for multi-round XOR encryption on RGB images. The repository also includes a CLI tool, a PyQt5 GUI, and PSNR / SSIM evaluation scripts.

### Core Idea

1. Generate a chaotic sequence with the Logistic equation:

   `x_(n+1) = r * x_n * (1 - x_n)`

2. When `r > 3.57`, the system enters a chaotic regime.
3. Scale the sequence to `0-255` and XOR it with the `R / G / B` channels.
4. Decrypt the image by running XOR again with the same `r`, `x0`, and number of rounds.

### Repository Structure

| File | Purpose |
| --- | --- |
| `logistic.py` | CLI program for encryption and decryption |
| `pyqt5.py` | PyQt5 GUI version |
| `psnr.py` | PSNR evaluation script |
| `ssim.py` | SSIM evaluation script |
| `read.py` | Helper script for inspecting pixel values |
| sample `.bmp` / `.tiff` files | Example inputs and outputs |

### Quick Start

Install dependencies:

```bash
pip install pillow pyqt5 numpy scikit-image tifffile matplotlib
```

Run the CLI version:

```bash
python logistic.py
```

Run the GUI version:

```bash
python pyqt5.py
```

Run the evaluation scripts:

```bash
python psnr.py
python ssim.py
```

### Notes

- The current implementation is intended for teaching, experimentation, and reproduction.
- The input image is searched by trying common extensions automatically, so using a filename stem without the extension is the safest choice.
- The repository already contains sample images that can be used directly for demonstration.
