import cv2
import numpy as np
import os
import utilities.handTracyModule as ht


def Painter():
    brushThickness = 15
    eraserThickness = 50

    imageFolderPath = "painterImage"
    myList = os.listdir(imageFolderPath)
    print(myList)
    overlayList = []
    for imgPath in myList:
        image = cv2.imread(f'{imageFolderPath}/{imgPath}')
        overlayList.append(image)
    print(len(overlayList))
    header = overlayList[3]
    drawColour = (255, 0, 255)

    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    detection = ht.handDetection(detectionConfidence=0.85)
    xp, yp = 0, 0
    newImgCanvas = np.zeros((720, 1280, 3), np.uint8)

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)

        img = detection.findHands(img)
        landmarkList = detection.findPosition(img, draw=False)

        if len(landmarkList) != 0:
            # print(landmarkList)

            # Tip of the index and the middle fingers
            x1, y1 = landmarkList[8][1:]
            x2, y2 = landmarkList[12][1:]

            fingers = detection.fingersUp()
            print(fingers)

            if fingers[1] and fingers[2]:
                xp, yp = 0, 0
                print("Selected")
                if y1 < 100:
                    if 250 < x1 < 450:
                        header = overlayList[3]
                        drawColour = (255, 182, 56)
                    elif 550 < x1 < 750:
                        header = overlayList[1]
                        drawColour = (0, 128, 55)
                    elif 800 < x1 < 950:
                        header = overlayList[2]
                        drawColour = (22, 22, 255)
                    elif 1050 < x1 < 1200:
                        header = overlayList[0]
                        drawColour = (0, 0, 0)
                cv2.rectangle(img, (x1, y1 - 20), (x2, y2 + 20), drawColour, cv2.FILLED)

            if fingers[1] and fingers[2] == False:
                cv2.circle(img, (x1, y1), 10, drawColour, cv2.FILLED)
                print("Drawing")
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                if drawColour == (0, 0, 0):
                    cv2.line(img, (xp, yp), (x1, y1), drawColour, eraserThickness)
                    cv2.line(newImgCanvas, (xp, yp), (x1, y1), drawColour, eraserThickness)
                else:
                    cv2.line(img, (xp, yp), (x1, y1), drawColour, brushThickness)
                    cv2.line(newImgCanvas, (xp, yp), (x1, y1), drawColour, brushThickness)
                xp, yp = x1, y1

        grayImg = cv2.cvtColor(newImgCanvas, cv2.COLOR_BGR2GRAY)
        _, inverseImg = cv2.threshold(grayImg, 50, 255, cv2.THRESH_BINARY_INV)
        inverseImg = cv2.cvtColor(inverseImg, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, inverseImg)
        img = cv2.bitwise_or(img, newImgCanvas)

        # Setting the header image (1.png)
        img[0:100, 0:1280] = header
        # img = cv2.addWeighted(img, 0.5, newImgCanvas, 0.5, 0)
        # cv2.imshow("Image", img)
        # cv2.imshow("ImageCanvas", newImgCanvas)
        # cv2.waitKey(1)
        _, jpeg = cv2.imencode('.jpg', img)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(jpeg) + b'\r\n')