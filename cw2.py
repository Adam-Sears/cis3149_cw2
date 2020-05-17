# -*- coding: utf-8 -*-
"""
Created on Fri Mar 6 14:47:07 2020
@author: Dakota Hampson, Adam Sears
Last edit by Adam Sears on Sun May 17 19:53:40 2020
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
pts = np.array([[5,240],[55,340],[55,140]], np.int32)
pts = pts.reshape((-1,1,2))
back_arrow = {
    'pts' : pts,
    'startEnd' : (5,140,105,340)
}

pts = np.array([[635,240],[585,140],[585,340]], np.int32)
pts = pts.reshape((-1,1,2))
next_arrow = {
    'pts' : pts,
    'startEnd' : (535,140,635,340)
}

menu_item_0 = {
    'start' : (85,5),
    'end' : (285,105),
    'startEnd' : (85,5,285,105)
}

menu_item_1 = {
    'start' : (355,5),
    'end' : (555,105),
    'startEnd' : (355,5,555,105)
}

menu_item_2 = {
    'start' : (85,190),
    'end' : (285,290),
    'startEnd' : (85,190,285,290)
}

menu_item_3 = {
    'start' : (355,190),
    'end' : (555,290),
    'startEnd' : (355,190,555,290)
}

menu_item_4 = {
    'start' : (85,375),
    'end' : (285,475),
    'startEnd' : (85,375,285,475)
}

menu_item_5 = {
    'start' : (355,375),
    'end' : (555,475),
    'startEnd' : (355,375,555,475)
}

menu_shapes = [menu_item_0, menu_item_1, menu_item_2, menu_item_3, menu_item_4, menu_item_5, back_arrow, next_arrow]

menu_item = []
temp_menu = []
temp_menu.append("if")
temp_menu.append("if")
temp_menu.append("if")
temp_menu.append("if")
temp_menu.append("if")
temp_menu.append("if")
menu_item.append(temp_menu)
temp_menu = []
temp_menu.append("if")
temp_menu.append("if")
temp_menu.append("if")
temp_menu.append("if")
temp_menu.append("if")
temp_menu.append("if")
menu_item.append(temp_menu)

menu_page = 0

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
            img = cv2.putText(img,menu_item[menu_page][i],menu_shapes[i]['end'],cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255))
        
        #Detect body parts
        palms = hand.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in palms:
            palmsCount += 1 #Counts how many hands have been detected
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,128),2)
        
        fists = fist.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in fists:
            fistsCount += 1 #Counts how many fists have been detected
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        
        """
        Gesture detection
        """
        #Palm turns to fist
        if palmsBool == True and fistsCount > 0:
            for (xFist,yFist,wFist,hFist) in fists:
                img = cv2.putText(img,"Palm to Fist",(xFist,yFist),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,0))
                xFistMiddle = xFist+(wFist/2)
                yFistMiddle = yFist+(hFist/2)
                for key, val in menu_shapes.items():
                    xShapeStart = val['startEnd'][0]
                    yShapeStart = val['startEnd'][1]
                    xShapeEnd = val['startEnd'][2]
                    yShapeEnd = val['startEnd'][3]
                    if (xFistMiddle > xShapeStart and xFistMiddle < xShapeEnd) and (yFistMiddle > yShapeStart and yFistMiddle < yShapeEnd):
                        print(val)
                        if "arrow" in val:
                            play_obj = low_wav.play()
                        else:
                            play_obj = high_wav.play()
        """
        #
        """
        
        cv2.imshow('Gesture controlled programming software', img)
        
        k = cv2.waitKey(10)
        if k == 27:  # press ESC to exit
            break
        
        """
        Set variables for next stage of while loop
        """
        #If body part(s) detected set "previous state" boolean to true, if none set to false
        palmsBool = True if palmsCount > 0 else False
        fistsBool = True if fistsCount > 0 else False
            
        #Clear current counts
        palmsCount = 0
        fistsCount = 0
        """
        #
        """
    else:
        break
    
camera.release()
cv2.destroyAllWindows()
