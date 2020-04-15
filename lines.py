import numpy as np


# Class with static variables in case the lane is NaN
def calculate_coordinates(height, value, default):
    if np.all(np.isnan(value)):
        return default
    slope, intercept = value
    y1 = height
    y2 = int(y1 * 0.6)
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])


class Lines:
    left_line = []
    right_line = []

    @staticmethod
    def calculate_lines(height, lines):
        left = []
        right = []
        # Loops through every detected line
        for line in lines:
            # Reshapes line from 2D array to 1D array
            x1, y1, x2, y2 = line.reshape(4)
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            y_intercept = parameters[1]
            # Don't care about steep slopes
            if np.fabs(slope) < 0.5:
                continue

            if slope < 0:
                left.append((slope, y_intercept))
            else:
                right.append((slope, y_intercept))

        # Calculates the x1, y1, x2, y2 coordinates for the left and right line
        Lines.left_line = calculate_coordinates(height,
                                                np.average(left, axis=0),
                                                Lines.left_line)
        Lines.right_line = calculate_coordinates(height,
                                                 np.average(right, axis=0),
                                                 Lines.right_line)
        return np.array([Lines.left_line, Lines.right_line])
