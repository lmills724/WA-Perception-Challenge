import cv2
import numpy as np

# Finds segments matching the cone's color
def colorSegmentation(img):
    # Converting to hsv colorspace
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
   
    # Lower bound and upper bound for cone color
    lower_bound = np.array([177, 200, 77])
    upper_bound = np.array([180, 494, 432])
 
    # Create mask to find color within boundaries
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Remove unnecessary noise from mask
    kernel = np.ones((7, 7), np.uint8) # Creates 5x5 8bit int matrix

    # Remove unnecessary black noise from white region
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    # Remove unnecessary white noise from black region
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Segment only detected region (bitwise_and applies mask only on true white)
    segmented_img = cv2.bitwise_and(img, img, mask=mask)

    # Find contours from mask
    contours, hierarchy = cv2.findContours(
        mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    colorSegImg =  cv2.drawContours(segmented_img, contours, -1, (0,0, 255), 3)
    
    return colorSegImg, contours


# Find the locations of the center of each detected cone
def getPoints(contours):
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse= False)

    # Store detected object coordinates
    X = []
    Y = []
    for c in sorted_contours:
        M = cv2.moments(c)
        xcenter = int(M['m10']/M['m00'])
        ycenter = int(M['m01']/M['m00'])
        X.append(xcenter)
        Y.append(ycenter)

    # Convert to numpy array of ints
    X = np.asarray(X, dtype=int)
    Y = np.asarray(Y, dtype=int)

    # Find mean of X values so we can split into two datasets
    x_mean = np.mean(X)

    # Split the dataset by X value
    X1 = []
    X2 = []
    Y1 = []
    Y2 = []
    for i in range(len(X)):
        if X[i] <= x_mean:
            X1.append(X[i])
            Y1.append(Y[i])
        else:
            X2.append(X[i])
            Y2.append(Y[i])
    X1 = np.asarray(X1, dtype=int)
    Y1 = np.asarray(Y1, dtype=int)
    X2 = np.asarray(X2, dtype=int)
    Y2 = np.asarray(Y2, dtype=int)
    
    return X1,X2,Y1,Y2


# Plots the line and creates an answer image
def plotData(X1, X2, Y1, Y2, img):
 
    # Finds slope and intercept of line of best fit
    a,b = np.polyfit(X1,Y1,1)
    c,d = np.polyfit(X2,Y2,1)
    
    x0 = img.shape[0]
  
    # Put lines on the images
    cv2.line(img, (int(-d/c),0), (x0, int(c*x0 + d)), (0,0,255),5)
    cv2.line(img, (int(-b/a),0), (0, int(b)), (0,0,255),5)
    cv2.imwrite('answer.png', img)



# Read in image
img = cv2.imread('red.png')
# Color segment image
colorSegImg, contours = colorSegmentation(img)
# Get points
x1,x2,y1,y2 = getPoints(contours)
# Plot answer
plotData(x1, x2, y1, y2, img)
