import cv2
import numpy as np

from lines import Lines
from parameters import Parameters


def to_hls(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2HLS)


def darken(img, gamma=1.0):
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(img, table)


class CV2Wrapper:
    def __init__(self):
        self.parameters = Parameters(kernel_size=9,
                                     low_threshold=50,
                                     high_threshold=140,
                                     threshold=35,
                                     min_line_length=20,
                                     max_line_gap=150)

    def grayscale(self, img):
        """Applies the Grayscale transform
        This will return an image with only one color channel
        but NOTE: to see the returned image as grayscale
        (assuming your grayscaled image is called 'gray')
        you should call plt.imshow(gray, cmap='gray')"""
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        # Return darken grayscale image
        return darken(gray, self.parameters.grayscale.gamma)
        # Or use BGR2GRAY if you read an image with cv2.imread()
        # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def canny(self, img):
        """Applies the Canny transform"""
        return cv2.Canny(img, self.parameters.canny.low_threshold, self.parameters.canny.high_threshold)

    def gaussian_blur(self, img):
        """Applies a Gaussian Noise kernel"""
        return cv2.GaussianBlur(img, (self.parameters.gaussian.kernel_size, self.parameters.gaussian.kernel_size), 0)

    def region_of_interest(self, img):
        """
        Applies an image mask.

        Only keeps the region of the image defined by the polygon
        formed from `vertices`. The rest of the image is set to black.
        `vertices` should be a numpy array of integer points.
        """
        # defining a blank mask to start with
        mask = np.zeros_like(img)

        img_height = img.shape[0]
        img_width = img.shape[1]

        # defining a 3 channel or 1 channel color to fill the mask with depending on the input image
        if len(img.shape) > 2:
            channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
            ignore_mask_color = (255,) * channel_count
        else:
            ignore_mask_color = 255

        vertices = np.array([[(0, img_height),  # lower_left
                              (img_width * self.parameters.vertices.left_width_ration,
                               img_height * self.parameters.vertices.height_ratio),  # upper_left
                              (img_width * self.parameters.vertices.right_width_ratio,
                               img_height * self.parameters.vertices.height_ratio),  # upper_right
                              (img_width, img_height)]],  # lower_right
                            dtype=np.int32)

        # filling pixels inside the polygon defined by "vertices" with the fill color
        cv2.fillPoly(mask, vertices, ignore_mask_color)

        # returning the image only where mask pixels are nonzero
        masked_image = cv2.bitwise_and(img, mask)

        return masked_image

    def draw_lines(self, img, lines):
        """
        NOTE: this is the function you might want to use as a starting point once you want to
        average/extrapolate the line segments you detect to map out the full
        extent of the lane (going from the result shown in raw-lines-example.mp4
        to that shown in P1_example.mp4).

        Think about things like separating line segments by their
        slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
        line vs. the right line.  Then, you can average the position of each of
        the lines and extrapolate to the top and bottom of the lane.

        This function draws `lines` with `color` and `thickness`.
        Lines are drawn on the image inplace (mutates the image).
        If you want to make the lines semi-transparent, think about combining
        this function with the weighted_img() function below
        """

        calculated_lines = Lines.calculate_lines(img.shape[0], lines)

        if calculated_lines is not None:
            for x1, y1, x2, y2 in calculated_lines:
                cv2.line(img, (x1, y1), (x2, y2), self.parameters.lines.color, self.parameters.lines.thickness)
        return img

    def hough_lines(self, img):
        """
        `img` should be the output of a Canny transform.

        Returns an image with hough lines drawn.
        """
        lines = cv2.HoughLinesP(img,
                                self.parameters.hough.rho,
                                self.parameters.hough.theta,
                                self.parameters.hough.threshold,
                                np.array([]),
                                minLineLength=self.parameters.hough.min_line_length,
                                maxLineGap=self.parameters.hough.max_line_gap)
        line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
        self.draw_lines(line_img, lines)
        return line_img

    # Python 3 has support for cool math symbols.

    def weighted_img(self, img, initial_img, α=0.8, β=1., γ=0.):
        return cv2.addWeighted(initial_img, α, img, β, γ)

    def color_selection(self, img, gray):
        white_mask = cv2.inRange(to_hls(img),
                                 self.parameters.color_selection.white_low_thresh,
                                 self.parameters.color_selection.white_high_thresh)
        yellow_mask = cv2.inRange(to_hls(img),
                                  self.parameters.color_selection.yellow_low_thresh,
                                  self.parameters.color_selection.yellow_high_thresh)
        mask = cv2.bitwise_or(white_mask, yellow_mask)
        return cv2.bitwise_and(gray, gray, mask=mask)
