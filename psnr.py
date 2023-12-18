import numpy as np
import os
import SimpleITK as sitk
import matplotlib.pyplot as plt
from skimage.metrics import peak_signal_noise_ratio
from skimage.metrics import structural_similarity
from skimage.metrics import mean_squared_error
from tifffile import imread
from PIL import Image

input_reference_nii = imread("test.tiff")
input_testimage_nii = imread("encrypted.tiff")

PSNR = peak_signal_noise_ratio(input_reference_nii,input_testimage_nii, 
                                data_range=np.max(input_reference_nii))

print(PSNR)







