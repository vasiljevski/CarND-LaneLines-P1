import math
import numpy as np


class Parameters:
    def __init__(self,
                 gamma: object = 0.5,
                 kernel_size: object = 5,
                 white_low_thresh: object = np.array([0, 200, 0], dtype=np.uint8),
                 white_high_thresh: object = np.array([200, 255, 255], dtype=np.uint8),
                 yellow_low_thresh: object = np.array([10, 0, 100], dtype=np.uint8),
                 yellow_high_thresh: object = np.array([40, 255, 255], dtype=np.uint8),
                 low_threshold: object = 50,
                 high_threshold: object = 150,
                 height_ratio: object = 0.58,
                 left_width_ration: object = 0.49,
                 right_width_ratio: object = 0.51,
                 rho: object = 1,
                 theta: object = math.pi / 180,
                 threshold: object = 35,
                 min_line_length: object = 5,
                 max_line_gap: object = 2,
                 color: object = [255, 0, 0],
                 thickness: object = 10) -> object:
        self.grayscale = Grayscale(gamma)
        self.color_selection = ColorSelection(white_low_thresh,
                                              white_high_thresh,
                                              yellow_low_thresh,
                                              yellow_high_thresh)
        self.gaussian = Gaussian(kernel_size)
        self.canny = Canny(low_threshold, high_threshold)
        self.vertices = Vertices(height_ratio, left_width_ration, right_width_ratio)
        self.hough = Hough(rho, theta, threshold, min_line_length, max_line_gap)
        self.lines = Lines(color, thickness)


class Grayscale:
    def __init__(self, gamma):
        # Grayscale parameters
        self.gamma = gamma


class ColorSelection:
    def __init__(self, white_low_thresh, white_high_thresh, yellow_low_thresh, yellow_high_thresh):
        # White and Yellow low/high
        self.yellow_low_thresh = yellow_low_thresh
        self.white_high_thresh = white_high_thresh
        self.white_low_thresh = white_low_thresh
        self.yellow_high_thresh = yellow_high_thresh


class Gaussian:
    def __init__(self, kernel_size):
        # Gaussian parameters
        self.kernel_size = kernel_size


class Canny:
    def __init__(self, low_threshold, high_threshold):
        # Define our parameters for Canny
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold


class Vertices:
    def __init__(self, height_ratio, left_width_ration, right_width_ratio):
        # Vertices params
        self.height_ratio = height_ratio
        self.left_width_ration = left_width_ration
        self.right_width_ratio = right_width_ratio


class Hough:
    def __init__(self, rho, theta, threshold, min_line_length, max_line_gap):
        self.rho = rho  # distance resolution in pixels of the Hough grid
        self.theta = theta  # angular resolution in radians of the Hough grid
        self.threshold = threshold  # minimum number of votes (intersections in Hough grid cell)
        self.min_line_length = min_line_length  # minimum number of pixels making up a line
        self.max_line_gap = max_line_gap  # maximum gap in pixels between connectable line segments


class Lines:
    def __init__(self, color, thickness):
        # Vertices params
        self.color = color
        self.thickness = thickness
