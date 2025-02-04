#Importing the required files
import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
#capturing the webcame video
cap = cv2.VideoCapture(0)
#setting the size of webcame
cap.set(3, 640)
cap.set(4, 480)
#detecting the hand using module
detector = HandDetector(maxHands=1)
#setting the initial values
timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # [AI, Player]
#ruuning the program
while True:
    #reading th ebackground image
    imgBG = cv2.imread("Resources/BG.png")
    success, img = cap.read()
    #resizing the webcam video to the size of the backgraound img and overlaying it
    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]

    # Finding Hands
    hands, img = detector.findHands(imgScaled)  # with draw
    #if game is started afer pressing "s" button on keyboard
    if startGame:
        #starting the timer from 0-3
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)
            #it won' show anything until the timer if finished
            if timer > 3:
                stateResult = True
                timer = 0
                #detecting the hands after the timer is finished
                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    #stone hand values
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1
                    #paper hand values
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2
                    #scissor hand values
                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3
                    #As we assigned the values to the hands now we are randomly selecting the hands and displaying using the images
                    randomNumber = random.randint(1, 3)
                    imgAI = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                    # Player Wins updating the score
                    if (playerMove == 1 and randomNumber == 3) or \
                            (playerMove == 2 and randomNumber == 1) or \
                            (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1
                    # AI Wins updating the score
                    if (playerMove == 3 and randomNumber == 1) or \
                            (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1
    #fitting the webcam video and fitting it to the background image
    imgBG[234:654, 795:1195] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))
    #displaying the fonts
    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    #to show the image
    cv2.imshow("BG", imgBG)

    #assigning the key to start the timer and the game
    key = cv2.waitKey(1)
    if key == ord('s'):
        #setting the values after pressing the s button on keyboard
        startGame = True
        initialTime = time.time()
        stateResult = False