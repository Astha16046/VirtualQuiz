import csv

import cvzone
from cvzone.HandTrackingModule import HandDetector
import cv2
import time
cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector = HandDetector(detectionCon=1)

class MCQ():
    def __init__(self,data):
        if len(data) >= 6:
            self.Question1= data[0]
            self.choice1 = data[1]
            self.choice2 = data[2]
            self.choice3 = data[3]
            self.choice4 = data[4]
            self.answer = int(data[5])
            self.userans=None
    def update(self,cursor,bboxs):

        for x, bbox in enumerate(bboxs):
            x1,y1,x2,y2=bbox
            if x1<cursor[0]<x2 and y1<cursor[1]<y2:
                self.userans= x+1
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),cv2.FILLED)

# import csv file data
pathCSV="mcq_quiz"
with open(pathCSV,newline='\n') as f:
    reader=csv.reader(f)
    datall=list(reader)[1:]
#create obj for each mcq
mcqList=[]
for q in datall:
    mcqList.append(MCQ(q))

print(len(mcqList))

qNo=0
qTotal=len(mcqList)
while True:
    success,img=cap.read()
    img=cv2.flip(img,1)
    hand,img=detector.findHands(img,flipType=False)
    if qNo<qTotal:
        mcq = mcqList[qNo]
        img, bbox = cvzone.putTextRect(img, mcq.Question1, [100, 100], 2, 2, offset=50, border=5)
        img, bbox1 = cvzone.putTextRect(img, mcq.choice1, [100, 250], 2, 2, offset=50, border=5)
        img, bbox2 = cvzone.putTextRect(img, mcq.choice2, [400, 250], 2, 2, offset=50, border=5)
        img, bbox3 = cvzone.putTextRect(img, mcq.choice3, [100, 400], 2, 2, offset=50, border=5)
        img, bbox4 = cvzone.putTextRect(img, mcq.choice4, [400, 400], 2, 2, offset=50, border=5)

        if hand:
            lmList = hand[0]['lmList']
            cursor = lmList[8]
            length, info = detector.findDistance(lmList[8], lmList[12])

            if length < 60:
                mcq.update(cursor, [bbox1, bbox2, bbox3, bbox4])
                print(mcq.userans)
                if mcq.userans is not None:
                    time.sleep(0.5)
                    qNo += 1
    else:
        score=0
        for mcq in mcqList:
            if mcq.answer==mcq.userans:
                score+=1
        score=round((score/qTotal)*100,2)
        img, bbox = cvzone.putTextRect(img,"Quiz Completed", [250, 300], 2, 2, offset=50, border=5)
        img, bbox = cvzone.putTextRect(img, f'Your Score:{score}%', [700, 300], 2, 2, offset=16, border=5)

    #draw progress
    barValue=150+(950//qTotal)*qNo
    cv2.rectangle(img, (150,600), (barValue,650), (0,255,0), cv2.FILLED)
    cv2.rectangle(img, (150,600), (1100,650), (255,0,255),5)
    img, bbox = cvzone.putTextRect(img, f'{round(qNo / qTotal * 100)}%', [1130, 635], 2, 2, offset=16, border=5)

    cv2.imshow("Img",img)
    cv2.waitKey(1)