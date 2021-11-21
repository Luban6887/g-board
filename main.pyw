#coded by luban
#from os import PRIO_PGRP
#from multiprocessing import Process
import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import time
import numpy as np
import cvzone
from pynput.keyboard import Controller

with open('config.txt', "r") as word_list:
    words = word_list.read().split(' ')

camera = words[2]
accuracy = words[5]

ccolor = (0, 255, 0)
hover = (0,0,225)
red = (0,0,245)
cap = cv2.VideoCapture(int(camera))
eTime = time.time()
pTime = 0

detector = HandDetector(detectionCon=float(accuracy))
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
finalText = ""

keyboard = Controller()
ax = 746
ay = 1016
aw = 357
ah = 439

def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h),red, cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img


class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    #LBN = img
    img = cv2.resize(img,(1100,500))

    img = detector.findHands(img,draw=True)
    lmList, bboxInfo = detector.findPosition(img,draw=False)
    img = drawAll(img, buttonList)
    cTime = time.time() - eTime
    #________
    cTime = int(cTime)



    
#transparent exit box
    bbox = [300,100,200,200]
    blk = np.zeros(img.shape, np.uint8)
    cv2.rectangle(blk, (ax,aw),(ay,ah),red,cv2.FILLED)
    img = cv2.addWeighted(img, 0.6, blk, 0.50, 1)


    cv2.putText(img, 'EXIT', (800,420),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    if lmList:
        #print(lmList[8])
        for button in buttonList:
            x, y = button.pos
            w, h = button.size
            cursor = lmList[8]
            l, _, _ = detector.findDistance(8, 4, img, draw=False)
            cv2.circle(img, (cursor[0],cursor[1]), 5 , ccolor, cv2.FILLED)

            if 749 < lmList[8][0]  and 356 < lmList[8][1]:
                if l < 30:
                    x =cTime-pTime
                    if l < 30 and x == 0 : 
                        pTime+=2
                        keyboard.press('1')
                    else:
                        pTime=cTime
                
            
            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), hover, cv2.FILLED)#(175, 0, 175)
                cv2.putText(img, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                

                
                
                if l < 30:
                    x = cTime-pTime
                    #print(x)
                    if l < 30 and x == 0 :
                        pTime += 2

                        ccolor = (0, 0, 255)
                        cv2.circle(img, (cursor[0],cursor[1]), 20 , ccolor, 5, cv2.FILLED)
  #______________________________________________________________                      
                        keyboard.press(button.text)
                        finalText += button.text
                        lbn = button.text
                        #print(lbn)
                        x1 = len(finalText)
                        x1 = int(x1)
                        if x1 == 13:
                            finalText = ""
                            finalText += button.text
#___________________________________________________________________
    
                else:
                    pTime = cTime
                    ccolor = (0, 255, 0)

    cv2.rectangle(img, (50, 350), (700, 450), hover, cv2.FILLED) #(175, 0, 175)
    cv2.putText(img, finalText, (60, 430),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("coded by LUBAN", img)
    #cv2.imshow("Camera", LBN)
    if cv2.waitKey(1) == ord('1'):
     break
cv2.destroyAllWindows()
