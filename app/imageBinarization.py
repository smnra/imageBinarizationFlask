import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import os


def showImage(name, img):
    plt.imshow(img, cmap="gray")
    plt.title(name)
    plt.show()


def AdaptiveThreshold(img):
    C = 6
    win = 21
    img_blur = cv.blur(img, (win, win))
    img2 = np.uint8(img > img_blur - C) * 255
    return img2


def AdaptiveThreshold2(img):
    alpha = 0.05
    win = 21
    img_blur = cv.GaussianBlur(img, (win, win), 5)
    img2 = np.uint8(img > (1 - alpha) * img_blur) * 255
    return img2




def imageBinarizationAdaptive(source_path, output_path):
    img = cv.imread(source_path, 0)
    img3 = AdaptiveThreshold2(img)
    cv.imwrite(output_path, img3)
    return output_path

if __name__ == "__main__":
    output_path = os.path.split(os.path.abspath(__file__))[0]+"/outputs/"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    img = cv.imread("./uploads/736c0d1887738142cbddf1cbf9e3432.jpg", 0)
    img3 = AdaptiveThreshold2(img)
    showImage("img3", img3)
    cv.imwrite(output_path + "img3_p.jpg", img3)


