from cv2_wrapper import CV2Wrapper


def process_image(img):
    cv2_wrapper = CV2Wrapper()
    gray = cv2_wrapper.grayscale(img)
    color_image = cv2_wrapper.color_selection(img, gray)
    blur_gray = cv2_wrapper.gaussian_blur(color_image)
    canny_edges = cv2_wrapper.canny(blur_gray)
    cropped_image = cv2_wrapper.region_of_interest(canny_edges)
    line_image = cv2_wrapper.hough_lines(cropped_image)
    return cv2_wrapper.weighted_img(line_image, img)
