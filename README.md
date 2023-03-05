# Wisconsin Autonomous Perception Coding Challenge

## Libraries Used
- cv2
- NumPy

# Methodolgy
## Color Segmentation
To begin, I first approached this problem by using color segmentation to find the location of the cones. To do so, I converted the image to HSV colorspace and found bounds for the color of the cones. Here are some of the resources that I found helpful:
- https://techvidvan.com/tutorials/detect-objects-of-similar-color-using-opencv-in-python/
- https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv/48367205#48367205


## Reading The Data
Once I had obtained the masked image and contours, I stored the coordinates by finding the centers of each contour area, which can be found by using the moments.

To create two lines, I found the mean of the x values and split the data into two separate sets. Since we're only using this program for this image, it worked, but I know this isn't a good general approach.

This tutorial was particularily useful (same as first one above):
- https://techvidvan.com/tutorials/detect-objects-of-similar-color-using-opencv-in-python/


## Plotting The Lines
To plot the lines I used NumPy's polyfit function to find the slope and y-intercepts of the lines of best fit. Using that, I was able to plot lines that ran across the whole image by using cv2's imwrite function.