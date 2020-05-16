# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 14:47:07 2020
@author: Dakota Hampson, Adam Sears
Last edit by Adam Sears on Fri May 15 11:02:43 2020
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
pts = np.array([[5,350],[5,450],[305,450]], np.int32)
pts = pts.reshape((-1,1,2))
back_arrow = {
'pts' : pts,
'thickness' : 2,
'startEnd' : (5,350,305,450)
}

pts = np.array([[5,350],[5,450],[305,450]], np.int32)
pts = pts.reshape((-1,1,2))
next_arrow = {
        'pts' : pts,
        'thickness' : 2,
        'startEnd' : (5,350,305,450)
}

menu_item_0 = {
        'start' : (5,5),
        'end' : (205,205),
        'thickness' : 2,
        'startEnd' : (5,5,205,205)
}

pts = np.array([[5,350],[5,450],[305,450]], np.int32)
pts = pts.reshape((-1,1,2))
menu_item_1 = {
        'start' : (5,5),
        'end' : (205,205),
        'thickness' : 2,
        'startEnd' : (5,5,205,205)
}

menu_item_2 = {
        'start' : (5,5),
        'end' : (205,205),
        'thickness' : 2,
        'startEnd' : (5,5,205,205)
}

menu_item_3 = {
        'start' : (5,5),
        'end' : (205,205),
        'thickness' : 2,
        'startEnd' : (5,5,205,205)
}

menu_item_4 = {
        'start' : (5,5),
        'end' : (205,205),
        'thickness' : 2,
        'startEnd' : (5,5,205,205)
}

menu_item_5 = {
        'start' : (5,5),
        'end' : (205,205),
        'thickness' : 2,
        'startEnd' : (5,5,205,205)
}

menu_shapes = {
        'back_arrow' : back_arrow,
        'next_arrow' : next_arrow,
        'item0' : menu_item_0,
        'item1' : menu_item_1,
        'item2' : menu_item_2,
        'item3' : menu_item_3,
        'item4' : menu_item_4,
        'item5' : menu_item_5
}

menu_item = dict()
temp_menu = dict()
temp_menu.append("if")
temp_menu.append("if")
temp_menu.append("if")
temp_menu.append("if")
temp_menu.append("if")
temp_menu.append("if")
menu_item.append(temp_menu)
temp_menu = dict()
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
        cv2.fillPoly(img,[menu_shapes['back_arrow']['pts']],(0,0,255))
        cv2.fillPoly(img,[menu_shapes['next_arrow']['pts']],(0,0,255))
        for i in range(6):
            img = cv2.rectangle(img,menu_shapes['item'+i]['start'],menu_shapes['item1']['end'],(0,0,255),menu_shapes['item1']['thickness'])
            img = cv2.putText(img,menu_item[menu_page][i],(400,450),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,255))
        
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
        
        cv2.imshow('Task 4', img)
        
        k = cv2.waitKey(10)
        if k == 27:  # press ESC to exit
            break
        
        """
        Set variables for next stage of while loop
        """
        #If body part(s) detected set "previous state" boolean to true, if none set to false
        palmsBool = True if palmsCount > 0 else False
        fistsBool = True if fistsCount > 0 else False
        facesBool = True if facesCount > 0 else False
            
        #Clear current counts
        palmsCount = 0
        fistsCount = 0
        facesCount = 0
        """
        #
        """
    else:
        break
    
camera.release()
cv2.destroyAllWindows()
