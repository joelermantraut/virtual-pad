import cv2
import numpy as np
import pyautogui
import HandTracking as ht


def main():
    # Variables Declaration
    width = 640  # Width of Camera
    height = 480  # Height of Camera
    frame_r = 100  # Frame Rate
    smoothening = 8  # Smoothening Factor
    prev_x, prev_y = 0, 0  # Previous coordinates
    curr_x, curr_y = 0, 0  # Current coordinates

    cap = cv2.VideoCapture(0)  # Getting video feed from the webcam
    cap.set(3, width)  # Adjusting size
    cap.set(4, height)

    detector = ht.HandDetector(maxHands=1)  # Detecting one hand at max
    screen_width, screen_height = pyautogui.size()  # Getting the screen size

    while True:
        success, img = cap.read()
        img = detector.findHands(img)  # Finding the hand
        lmlist, bbox = detector.findPosition(img)  # Getting position of hand

        if len(lmlist) != 0:
            x1, y1 = lmlist[8][1:]

            fingers = detector.fingersUp()  # Checking if fingers are upwards
            cv2.rectangle(
                img,
                (frame_r, frame_r),
                (width - frame_r, height - frame_r),
                (255, 0, 255),
                2,
            )  # Creating boundary box
            if fingers[1] == 1 and fingers[2] == 0:  # If forefinger is up and middle finger is down
                x3 = np.interp(x1, (frame_r, width - frame_r), (0, screen_width))
                y3 = np.interp(y1, (frame_r, height - frame_r), (0, screen_height))

                curr_x = prev_x + (x3 - prev_x) / smoothening
                curr_y = prev_y + (y3 - prev_y) / smoothening

                pyautogui.moveTo(
                    screen_width - curr_x, curr_y, pyautogui.MINIMUM_DURATION
                )  # Moving the cursor
                prev_x, prev_y = curr_x, curr_y

            if fingers[1] == 1 and fingers[2] == 1:  # If forefinger & middle finger both are up
                length, img, line_info = detector.findDistance(8, 12, img)

                if length < 40:  # If both fingers are really close to each other
                    pyautogui.click()  # Perform Click

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
