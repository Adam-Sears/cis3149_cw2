# -*- coding: utf-8 -*-
"""
Created on Fri Mar 6 14:47:07 2020
@author: Dakota Hampson, Adam Sears
Last edit by Adam Sears on Mon May 18 02:48:36 2020
"""

import cv2
import numpy as np
import simpleaudio as sa

# Open Camera
camera = cv2.VideoCapture(0)
camera.set(10, 200)

camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
camera.set(cv2.CAP_PROP_EXPOSURE, 0.01)

high_wav = sa.WaveObject.from_wave_file('sfx-high.wav')
low_wav = sa.WaveObject.from_wave_file('sfx-low.wav')

hand = cv2.CascadeClassifier('haarcascades/Hand.Cascade.1.xml')
fist = cv2.CascadeClassifier('haarcascades/fist.xml')

#Create array of shapes and coordinates
pts = np.array([[5,240],[105,340],[105,140]], np.int32)
pts = pts.reshape([-1,1,2])
back_arrow = {
    'pts': pts,
    'startEnd': [5,140,105,340]
}

pts = np.array([[635,240],[535,140],[535,340]], np.int32)
pts = pts.reshape([-1,1,2])
next_arrow = {
    'pts': pts,
    'startEnd': [535,140,635,340]
}

menu_item_0 = {
    'start': (135,5),
    'end': (310,105),
    'startEnd': [135,5,310,105],
    'textPos': (145,65)
}

menu_item_1 = {
    'start': (330,5),
    'end': (505,105),
    'startEnd': [330,5,505,105],
    'textPos': (340,65)
}

menu_item_2 = {
    'start': (135,190),
    'end': (310,290),
    'startEnd': [135,190,310,290],
    'textPos': (145,250)
}

menu_item_3 = {
    'start': (330,190),
    'end': (505,290),
    'startEnd': [330,190,505,290],
    'textPos': (340,250)
}

menu_item_4 = {
    'start': (135,375),
    'end': (310,475),
    'startEnd': [135,375,310,475],
    'textPos': (145,435)
}

menu_item_5 = {
    'start': (330,375),
    'end': (505,475),
    'startEnd': [330,375,505,475],
    'textPos': (340,435)
}

menu_shapes = [menu_item_0, menu_item_1, menu_item_2, menu_item_3, menu_item_4, menu_item_5, back_arrow, next_arrow]

menu_item = []
menu_item.append(["if","while","print","number","variable","not"]) #Page 0
menu_item.append(["if","if","if","if","if","if"]) #Page 1

menu_page = 0
action = ""

#Previous state
palmsBool = False
fistsBool = False

#Current count
palmsCount = 0
fistsCount = 0

while camera.isOpened():
    #Main Camera
    ret, img = camera.read()
    
    if(ret):        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        #Draw shapes on camera image
        cv2.fillPoly(img,[menu_shapes[6]['pts']],(255,0,0))
        cv2.fillPoly(img,[menu_shapes[7]['pts']],(255,0,0))
        for i in range(6):
            img = cv2.rectangle(img,menu_shapes[i]['start'],menu_shapes[i]['end'],(128,0,0),-1)
            img = cv2.putText(img,menu_item[menu_page][i],menu_shapes[i]['textPos'],cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255))
        
        #Detect body parts
        palms = hand.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in palms:
            palmsCount += 1 #Counts how many hands have been detected
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,128,255),2)
        
        fists = fist.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in fists:
            fistsCount += 1 #Counts how many fists have been detected
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        
        """
        #Gesture detection
        """
        #Palm turns to fist
        if palmsBool == True and fistsCount > 0:
            for (xFist,yFist,wFist,hFist) in fists:
                img = cv2.putText(img,"Palm to Fist",(xFist,yFist),cv2.FONT_HERSHEY_DUPLEX,1,(0,255,0))
                xFistMiddle = xFist+(wFist/2)
                yFistMiddle = yFist+(hFist/2)
                for i in range(len(menu_shapes)):
                    xShapeStart = menu_shapes[i]['startEnd'][0]
                    yShapeStart = menu_shapes[i]['startEnd'][1]
                    xShapeEnd = menu_shapes[i]['startEnd'][2]
                    yShapeEnd = menu_shapes[i]['startEnd'][3]
                    if (xFistMiddle > xShapeStart and xFistMiddle < xShapeEnd) and (yFistMiddle > yShapeStart and yFistMiddle < yShapeEnd):
                        if i < 6:
                            #Menu option selected    
                            play_obj = high_wav.play()
                            action = i
                        else:
                            #Arrow selected
                            play_obj = low_wav.play()
                            if i == 6:
                                action = "back"
                            elif i == 7:
                                action = "next"
        """
        #
        """
        
        cv2.imshow('Gesture controlled programming software', img)
        
        k = cv2.waitKey(10)
        if k == 27:  # press ESC to exit
            break
        
        """
        #Take action
        """
        if action == "back":
            if menu_page > 0:
                menu_page -= 1
            else:
                img = cv2.putText(img,"On first page",(10,30),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,255))
                print("On first page")
        elif action == "next":
            if menu_page < len(menu_item)-1:
                menu_page += 1
            else:
                img = cv2.putText(img,"On last page",(10,30),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,255))
                print("On last page")
        """
        #
        """
        
        """
        #Set variables for next stage of while loop
        """
        #If body part(s) detected set "previous state" boolean to true, if none set to false
        palmsBool = True if palmsCount > 0 else False
        fistsBool = True if fistsCount > 0 else False
            
        #Clear current counts
        palmsCount = 0
        fistsCount = 0
        action = ""
        """
        #
        """
    else:
        break
    
camera.release()
cv2.destroyAllWindows()
