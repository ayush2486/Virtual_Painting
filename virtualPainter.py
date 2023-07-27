import cv2
import numpy as np
import time
import os
import handTrackingModule as htm


bbrushThickness=15
eraserThickness=60

folderpath="HandTracking\header"
myList=os.listdir(folderpath)
print(myList)

overlayList=[]
for imPath in myList:
    image=cv2.imread(f'{folderpath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))

header=overlayList[0]
drawColor=(87,87,255)
cap=cv2.VideoCapture(0)

detector=htm.handDetector(detectionCon=0.85)
xp,yp=0,0
imgCanvas=np.zeros((480,640,3),np.uint8)



while True:

    #1: import image
    success,img=cap.read()
    img=cv2.flip(img,1)


    #2: hand landmarks
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    if len(lmList)!=0:
        
        # print(lmList)

        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]

        #3: check which finger is up
        fingers=detector.fingersUp()
        

        #4: selection mode : i two fingers are up
        if fingers[1] and fingers[2]:
            xp,yp=0,0
            if y1<73:
                if 10<=x1<=100:
                    header=overlayList[0]
                    drawColor=(87,87,255)
                elif 120<=x1<=230:
                    header=overlayList[1]
                    drawColor=(223,192,12)
                elif 140<=x1<=380:
                    header=overlayList[2]
                    drawColor=(87,217,126)

                elif 420<=x1<=530:
                    header=overlayList[3]
                    drawColor=(0,0,0)
            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)

        #5: drawing mode: index finger is up
        if fingers[1] and fingers[2]==False:
            cv2.circle(img,(x1,y1),15,drawColor,cv2.FILLED)
            if xp==0 and yp==0:
                xp,yp=x1,y1
            if drawColor==(0,0,0):
                cv2.line(img,(xp,yp),(x1,y1),drawColor,eraserThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,eraserThickness)
            else:
                cv2.line(img,(xp,yp),(x1,y1),drawColor,bbrushThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,bbrushThickness)
            xp,yp=x1,y1
            
    imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)  
    _, ImgInv=cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    ImgInv=cv2.cvtColor(ImgInv,cv2.COLOR_GRAY2BGR)
    img=cv2.bitwise_and(img,ImgInv)
    img=cv2.bitwise_or(img,imgCanvas)



    #setting the header image
    img[0:73,0:640]=header
    cv2.imshow("Image",img)
    # cv2.imshow("canvas",imgCanvas)
    cv2.waitKey(1)