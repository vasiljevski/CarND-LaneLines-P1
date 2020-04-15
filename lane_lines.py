# importing some useful packages
import os

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from moviepy.editor import VideoFileClip
from process import process_image


def process_images(path):
    files = os.listdir(path)
    images = []
    titles = []
    for file in files:
        if file[0:3] != "out":
            img = mpimg.imread(path + file)
            result = process_image(img)
            images.append(result)
            titles.append(file)
    show_images(images, 3, titles)


def show_images(images, cols=1, titles=None):
    """Display a list of images in a single figure with matplotlib.

    Parameters
    ---------
    images: List of np.arrays compatible with plt.imshow.

    cols (Default = 1): Number of columns in figure (number of rows is
                        set to np.ceil(n_images/float(cols))).

    titles: List of titles corresponding to each image. Must have
            the same length as titles.
    """
    assert ((titles is None) or (len(images) == len(titles)))
    n_images = len(images)
    if titles is None:
        titles = ['Image (%d)' % i for i in range(1, n_images + 1)]
    fig = plt.figure()
    for n, (image, title) in enumerate(zip(images, titles)):
        a = fig.add_subplot(cols, np.ceil(n_images / float(cols)), n + 1)
        if image.ndim == 2:
            plt.gray()
        plt.imshow(image)
        a.set_title(title)
    fig.set_size_inches(np.array(fig.get_size_inches()) * n_images)
    # plt.savefig('image.png')  # save the figure
    plt.show()


def process_video(file):
    clip = VideoFileClip("test_videos/" + file)
    result = clip.fl_image(process_image)
    result.write_videofile("test_videos_output/" + file, audio=False)


# Video files: solidWhiteRight, solidYellowLeft, challenge
def main():
    process_video("solidWhiteRight.mp4")
    process_video("solidYellowLeft.mp4")
    process_video("challenge.mp4")
    process_images("test_images/")


if __name__ == '__main__':
    main()
