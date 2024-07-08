import cv2
import numpy as np
import HandTracking as ht
import pyautogui
import time

def main():
    ### Variables Declaration
    width = 640             # Width of Camera
    height = 480            # Height of Camera
    frameR = 100            # Frame Rate
    prev_x, prev_y = 0, 0   # Previous coordinates
    curr_x, curr_y = 0, 0   # Current coordinates
    samples = 5
    samples_index = 0

    last_x = [0 for i in range(samples)]
    last_y = [0 for i in range(samples)]

    cap = cv2.VideoCapture(0)   # Getting video feed from the webcam
    cap.set(3, width)           # Adjusting size
    cap.set(4, height)

    detector = ht.HandDetector(maxHands=1)                  # Detecting one hand at max
    screen_width, screen_height = pyautogui.size()          # Getting the screen size
    while True:
        success, img = cap.read()

        img = cv2.flip(img, 0)
        # Needs a X mirror because was written to take palm
        # and in this mode is capturing dorsum

        if not success:
            continue

        img = detector.findHands(img, False)                      # Finding the hand
        lmlist, bbox = detector.findPosition(img)                 # Getting position of hand

        if len(lmlist)!=0:
            x1, y1 = lmlist[8][1:]
            # x2, y2 = lmlist[12][1:]

            fingers = detector.fingersUp()      # Checking if fingers are upwards
            cv2.rectangle(img, (frameR, frameR), (width - frameR, height - frameR), (255, 0, 255), 2)   # Creating boundary box
            if fingers[1] == 1 and fingers[2] == 0:     # If fore finger is up and middle finger is down
                x3 = np.interp(x1, (frameR,width-frameR), (0,screen_width))
                y3 = np.interp(y1, (frameR, height-frameR), (0, screen_height))

                curr_x = prev_x + (x3 - prev_x)
                curr_y = prev_y + (y3 - prev_y)
                # Calculates mouse position from finger position

                samples_index = (samples_index + 1) % samples
                # Index that keeps last samples position

                last_x[samples_index] = curr_x
                last_y[samples_index] = curr_y
                curr_x = sum(last_x) / samples
                curr_y = sum(last_y) / samples
                # Averages it using last N samples

                pyautogui.moveTo(screen_width - curr_x, curr_y, pyautogui.MINIMUM_DURATION) # Moving the cursor
                # cv2.circle(img, (x1, y1), 7, (255, 0, 255), cv2.FILLED)
                prev_x, prev_y = curr_x, curr_y

            if fingers[1] == 1 and fingers[2] == 1:     # If fore finger & middle finger both are up
                length, img, lineInfo = detector.findDistance(8, 12, img)

                if length < 40:     # If both fingers are really close to each other
                    # cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                    pyautogui.click() # Perform Click

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()