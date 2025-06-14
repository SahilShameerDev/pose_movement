import cv2
import numpy as np

# Create a black image
image = np.zeros((600, 800, 3), dtype=np.uint8)

# Draw a white rectangle
cv2.rectangle(image, (200, 150), (600, 450), (255, 255, 255), -1)

# Create a window named 'Game'
cv2.namedWindow('Game', cv2.WINDOW_NORMAL)

# Resize the window to desired dimensions
cv2.resizeWindow('Game', 640, 480)

# Show the image in the window
cv2.imshow('Game', image)

# Wait for a key press and close the window
cv2.waitKey(0)
cv2.destroyAllWindows()