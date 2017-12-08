import matplotlib.pyplot as plt

def compare_image(image1, image2, resulttype):

    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3))
    f.tight_layout()
    ax1.imshow(image1)
    ax1.set_title('Original Image', fontsize=15)
    ax2.imshow(image2)
    ax2.set_title('{} Image'.format(resulttype), fontsize=15)
    plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
    plt.show()
