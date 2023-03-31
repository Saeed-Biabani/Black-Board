import cv2 as cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone import stackImages
from numpy import zeros, uint8
from random import randint

def Draw(point, x, y, R, Color):
    x, y = point[-1]
    x2, y2 = point[-2]
    cv2.line(Board, (x,y), (x2, y2), Color, R)

def ShowInfo(color):
    cv2.rectangle(Board, (10, 10), (25, 25), color, -1)

def Nothig(x):
    pass


# CREATE NAMED WINDOW
cv2.namedWindow("Draw")

# CREAT TRACKBARS
cv2.createTrackbar("Draw", "Draw", 15, 100, Nothig)
cv2.createTrackbar("Font", "Draw", 10, 100, Nothig)
cv2.createTrackbar("Clear", "Draw", 5, 100, Nothig)
cv2.createTrackbar("Color", "Draw", 10, 100, Nothig)

cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

Detector = HandDetector(detectionCon = 0.8,  maxHands = 2)

# CREATE BLACK IMAGE
Board = zeros((480, 640, 3), uint8)

Points = []

Color = (255, 255, 255)
R = 1 # FONT

# SHOW COLOR ON BOARD
ShowInfo(Color)

while True:
    re, frame = cap.read()

    Hand, frame = Detector.findHands(frame, draw = True, flipType = False)

    if Hand:
        LmList = Hand[0]['lmList']
        x, y, w, h = Hand[0]['bbox']
        X2, Y2, _ = LmList[8]

        # CALCULATE DISTANCE BETWEEN SPECIAL POINTS
        Dist12 = int(Detector.findDistance(LmList[4][:2], LmList[8][:2])[0])
        Dist13 = int(Detector.findDistance(LmList[4][:2], LmList[12][:2])[0])
        Dist14 = int(Detector.findDistance(LmList[4][:2], LmList[16][:2])[0])
        Dist15 = int(Detector.findDistance(LmList[4][:2], LmList[20][:2])[0])

        # GET TRACKBAR VALUES
        DIFF12 = cv2.getTrackbarPos("Draw", "Draw")
        DIFF13 = cv2.getTrackbarPos("Font", "Draw")
        DIFF14 = cv2.getTrackbarPos("Clear", "Draw")
        DIFF15 = cv2.getTrackbarPos("Color", "Draw")

        if Dist12 < DIFF12:
            Points.append((X2, Y2))
            if len(Points) >= 2:
                Draw(Points, X2, Y2, R, Color)

        elif Dist13 < DIFF13:
            # INCREASE LINE THIKNESS
            R += 1
            if R >= 10:
                R = 1

        elif Dist14 < DIFF14:
            Board = zeros((480, 640, 3), uint8)
            ShowInfo(Color)

        elif Dist15 < DIFF15:
            # GENERATE RANDOM COLOR
            Color = (randint(0, 255), randint(0, 255), randint(0, 255))
            ShowInfo(Color)
        
        elif Dist13 >= DIFF13:
            Points.clear()
    
    stackIMG = stackImages([frame, Board], 2, 1)
    
    # SHOW BOARD
    cv2.imshow("Draw", stackIMG)

    if cv2.waitKey(1) &0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()