# **Finding Lane Lines on the Road** 

## Writeup Template

### You can use this file as a template for your writeup if you want to submit it as a markdown file. But feel free to use some other method and submit a pdf if you prefer.

---

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report


[//]: # (Image References)

[image2]: ./images/gray.png
[image3]: ./images/darken.png
[image4]: ./images/color_selection.png
[image6]: ./images/canny.png
[image7]: ./images/region.png
[image9]: ./images/result.png

---

### Reflection

### 1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

My pipeline is defined in process.py and all the CV2 stuff is moved to cv2_wrapper.py
Pipeline consisted of the following steps. 

First, I converted the images to grayscale,

![alt text][image2] 

and darken them to get better contrast.

![alt text][image3]

Next I added a color selection for white and yellow. This was needed or the challenge video, where in one segment due to
increased light the lines are not detected without color selection.

![alt text][image4]

Now I applied a gaussian blur and canny transform

![alt text][image6]

Before doing Hough transformation I had to crop the image to exclude the sky and the surroundings.

![alt text][image7]

The final result is:

![alt text][image9]

In order to draw a single line on the left and right lanes, I modified the draw_lines() function to first classify the
lines to left and right lines. 
Since it is first needed to classify the lines to left and right according to the sloap value, 
and then average the lines on both side to get one line for right and left. 
I moved the calculation to lines.py (class Lines) Last left and right
line coordinates are stored here to avoid disappearing of the lines in challenge.mp4, when no right line is detected.
To avoid sudden jumps I'm ignoring the lines with a absolute slope value smaller than 0.5

I moved all the parameters used to parameters.py (class Parameters) or easier manipulation with parameters. 


### 2. Identify potential shortcomings with your current pipeline


One potential shortcoming would be handling curved lanes, since the lines are now straight.
Also intersection would be interesting to see what would the pipeline do in that case. 
Having a car close in front, traffic jam, construction site would probably cause a lot of weird behaviours.
Environment conditions, snow, rain, fog...


### 3. Suggest possible improvements to your pipeline

Playing around with parameters could improve the result.
Since there is little or no error handling, it would make the pipeline more robust.
Parameters are static now, one improvement could be to have a way to optimise/calibrate the params to better detect lanes.
