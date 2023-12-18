from skimage.metrics import structural_similarity as ssim
from PIL import Image
import numpy as np


img1 = np.array(Image.open('test.bmp'))
img2 = np.array(Image.open('encrypted.bmp'))


if __name__ == "__main__":
	# If the input is a multichannel (color) image, set multichannel=True.
    print(ssim(img1, img2, channel_axis=-1))
