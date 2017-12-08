import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg




def color_grad(img, s_thresh=(170, 255), sx_thresh=(20, 100), DEBUG=False):

    img = np.copy(img)
    # Convert to HLS color space and separate the V channel
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS).astype(np.float)
    l_channel = hls[:,:,1]
    s_channel = hls[:,:,2]
    # Sobel x
    sobelx = cv2.Sobel(l_channel, cv2.CV_64F, 1, 0) # Take the derivative in x
    abs_sobelx = np.absolute(sobelx) # Absolute x derivative to accentuate lines away from horizontal
    scaled_sobel = np.uint8(255*abs_sobelx/np.max(abs_sobelx))
    # Threshold x gradient
    sxbinary = np.zeros_like(scaled_sobel)
    sxbinary[(scaled_sobel >= sx_thresh[0]) & (scaled_sobel <= sx_thresh[1])] = 1

    # Threshold color channel
    s_binary = np.zeros_like(s_channel)
    s_binary[(s_channel >= s_thresh[0]) & (s_channel <= s_thresh[1])] = 1

    # Stack each channel
    color_binary = np.uint8(np.dstack((np.zeros_like(s_channel), sxbinary, s_binary)) * 255)
    if DEBUG == True:
        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3))
        f.tight_layout()

        ax1.imshow(img)
        ax1.set_title('Original Image', fontsize=15)

        ax2.imshow(color_binary)
        ax2.set_title('Pipeline Result', fontsize=15)
        plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
        plt.show()
        cv2.imwrite()
    return color_binary
