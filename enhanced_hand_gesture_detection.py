import cv2
import numpy as np
import utlis
import sys

##############################################################################

cameraNo = 0  # 0 = Laptop webcam, 1 = Phone camera, 2 = External USB camera
portNo = "COM5"  # Change this to your Arduino port
cropVals = 80, 80, 320, 420  # StartPointY StartPointX h w (larger detection area)
frameWidth = 640
frameHeight = 480
brightnessImage = 180  # Adjusted for better detection

# IMPORTANT: Clean background for best results
print("=" * 60)
print("HAND DETECTION TIPS:")
print("1. Use a PLAIN background (wall, paper, etc.)")
print("2. Good lighting - avoid shadows")
print("3. Place hand CLOSE to camera (fills green box)")
print("4. Adjust HSV sliders to ONLY show your hand (white)")
print("5. Press 'r' to reset HSV to default skin tone values")
print("=" * 60)

##############################################################################

print("Initializing camera...")
cap = cv2.VideoCapture(cameraNo)

if not cap.isOpened():
    print(f"Error: Could not open camera {cameraNo}")
    print("Trying camera 0...")
    cameraNo = 2
    cap = cv2.VideoCapture(cameraNo)
    if not cap.isOpened():
        print("Error: No camera found. Please check your camera connection.")
        sys.exit(1)

print(f"Camera {cameraNo} opened successfully!")

# Set camera properties (some cameras may not support all settings)
try:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frameWidth)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frameHeight)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, brightnessImage)
    print(f"Camera resolution set to {frameWidth}x{frameHeight}")
except Exception as e:
    print(f"Warning: Could not set camera properties: {e}")

print("Initializing trackbars...")
utlis.initializeTrackBar()

print("Connecting to robot...")
utlis.connectToRobot(portNo)
print("Setup complete! Press 'q' to quit.")
print("Starting camera feed...")


while True:
    success, img = cap.read()
    
    if not success:
        print("Error: Failed to read from camera")
        break
    
    # Flip the image horizontally for a mirror effect (more intuitive)
    img = cv2.flip(img, 1)
    imgResult = img.copy()

    # Enhanced image processing for better hand detection
    # Step 1: Blur to reduce noise
    imgBlur = cv2.GaussianBlur(img, (9, 9), 2)
    
    # Step 2: Convert to HSV color space
    imgHSV = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2HSV)
    
    # Step 3: Get HSV values from trackbars
    trackBarPos = utlis.getTrackbarValues()
    imgMask, imgColorFilter = utlis.colorFilter(imgHSV, trackBarPos)

    # Crop the region of interest
    imgCropped = imgMask[cropVals[1]:cropVals[2]+cropVals[1], cropVals[0]:cropVals[0]+cropVals[3]]
    imgResult = imgResult[cropVals[1]:cropVals[2] + cropVals[1], cropVals[0]:cropVals[0] + cropVals[3]]
    
    # Enhanced morphological operations for noise removal and gap filling
    # Step 4: Remove small noise with opening
    kernel_open = np.ones((7, 7), np.uint8)
    imgOpen = cv2.morphologyEx(imgCropped, cv2.MORPH_OPEN, kernel_open, iterations=2)
    
    # Step 5: Fill small holes with closing
    kernel_close = np.ones((11, 11), np.uint8)
    imgClosed = cv2.morphologyEx(imgOpen, cv2.MORPH_CLOSE, kernel_close, iterations=3)
    
    # Step 6: Dilate to expand hand region slightly
    kernel_dilate = np.ones((5, 5), np.uint8)
    imgDilate = cv2.dilate(imgClosed, kernel_dilate, iterations=2)
    
    # Step 7: Erode slightly to restore original size with smooth edges
    kernel_erode = np.ones((3, 3), np.uint8)
    imgErode = cv2.erode(imgDilate, kernel_erode, iterations=1)
    
    # Step 8: Final smoothing with median filter (better than bilateral for this)
    imgFilter = cv2.medianBlur(imgErode, 7)
    
    # Get contours and detect fingers
    imgContour, imgResult = utlis.getContours(imgFilter, imgResult)

    ## TO DISPLAY
    # Draw detection rectangle with thicker line
    cv2.rectangle(img, (cropVals[0], cropVals[1]), 
                 (cropVals[0]+cropVals[3], cropVals[2]+cropVals[1]), 
                 (0, 255, 0), 3)
    
    # Add helpful text instructions
    cv2.putText(img, "Hand CLOSE to camera in GREEN box", (10, 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(img, "Use PLAIN background - adjust HSV", (10, 60), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.putText(img, "Press 'r' to reset | 'q' to quit", (10, 90), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Stack images for display with better layout
    stackedImage = utlis.stackImages(0.6, ([img, imgMask, imgColorFilter], 
                                            [imgFilter, imgContour, imgResult]))

    cv2.imshow('Hand Gesture Detection - Enhanced', stackedImage)

    # Press 'q' to quit, 'r' to reset HSV values
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        # Reset to default skin detection values
        cv2.setTrackbarPos("HUE MIN", "HSV Value", 0)
        cv2.setTrackbarPos("HUE MAX", "HSV Value", 25)
        cv2.setTrackbarPos("SAT MIN", "HSV Value", 30)
        cv2.setTrackbarPos("SAT MAX", "HSV Value", 255)
        cv2.setTrackbarPos("VALUE MIN", "HSV Value", 60)
        cv2.setTrackbarPos("VALUE MAX", "HSV Value", 255)
        print("HSV values reset to SKIN TONE defaults")
        print("IMPORTANT: Adjust sliders so ONLY YOUR HAND appears WHITE in the mask!")

print("Cleaning up...")
cap.release()
cv2.destroyAllWindows()
print("Program ended successfully!")
