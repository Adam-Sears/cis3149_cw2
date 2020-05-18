# -*- coding: utf-8 -*-
"""
Created on Fri Mar 6 14:47:07 2020
@author: Dakota Hampson, Adam Sears
Last edit by Adam Sears on Mon May 18 22:38:13 2020
"""

import cv2
import numpy as np
import math
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

white = (255,255,255)
red = (0,0,255)
green = (0,255,0)
blue = (255,0,0)
orange = (0,128,255)
dark_blue = (128,0,0)

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

numbers_menu = [[205,395,305,475,245,425],[5,5,105,85,45,35],[205,5,305,85,245,35],[405,5,505,85,445,35],[5,135,105,215,45,165],[205,135,305,215,245,165],[405,135,505,215,445,165],[5,265,105,345,45,295],[205,265,305,345,245,295],[405,265,505,345,445,295]]

var_count = 0
var_page = 0

menu_item = []
menu_item.append(["end line","delete current line","delete last line","backspace","space","execute"]) #Page 0
menu_item.append(["if","while","print","number","variable","not"]) #Page 1
menu_item.append(["True","False","!","=","+","-"]) #Page 2
menu_item.append(["(",")","[","]","{","}"]) #Page 3
menu_item.append([":","None",'"',"'","indent","remove indent"]) #Page 3 #Some quotes changed to allow entry of "

menu_page = 0
action = ""
change_menu = ""

code = []
temp_code = ""
executable_string = ""

#Previous state
palms_bool = False
fists_bool = False
selected_bool = False
error_bool = False

#Current count
palms_count = 0
fists_count = 0

while camera.isOpened():
    #Main Camera
    ret, img = camera.read()
    
    if(ret):        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        #Draw shapes on camera image
        if change_menu == "" or change_menu == "variable":
            cv2.fillPoly(img,[menu_shapes[6]['pts']],blue)
            cv2.fillPoly(img,[menu_shapes[7]['pts']],blue)
            for i in range(6):
                img = cv2.rectangle(img,menu_shapes[i]['start'],menu_shapes[i]['end'],dark_blue,-1)
                if change_menu == "":
                    img = cv2.putText(img,menu_item[menu_page][i],menu_shapes[i]['textPos'],cv2.FONT_HERSHEY_DUPLEX,1,white)
                elif change_menu == "variable":
                    if var_page == 0 and i == 0:
                        img = cv2.putText(img,"new variable",menu_shapes[i]['textPos'],cv2.FONT_HERSHEY_DUPLEX,1,white)
                    else:
                        variable_id = (var_page*6)+i
                        if variable_id <= var_count:
                            img = cv2.putText(img,"variable"+str(variable_id),menu_shapes[i]['textPos'],cv2.FONT_HERSHEY_DUPLEX,1,white)
        elif change_menu == "number":
            for i in range(10):
                img = cv2.rectangle(img,(numbers_menu[i][0],numbers_menu[i][1]),(numbers_menu[i][2],numbers_menu[i][3]),dark_blue,-1)
                img = cv2.putText(img,str(i),(numbers_menu[i][4],numbers_menu[i][5]),cv2.FONT_HERSHEY_DUPLEX,1,white)
        
        #Detect body parts
        palms = hand.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in palms:
            palms_count += 1 #Counts how many hands have been detected
            img = cv2.rectangle(img,(x,y),(x+w,y+h),orange,2)
        
        fists = fist.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in fists:
            fists_count += 1 #Counts how many fists have been detected
            img = cv2.rectangle(img,(x,y),(x+w,y+h),green,2)
        
        """
        #Gesture detection
        """
        #Palm turns to fist
        if palms_bool == True and fists_count > 0:
            for (x_fist,y_fist,w_fist,h_fist) in fists:
                img = cv2.putText(img,"Palm to Fist",(x_fist,y_fist),cv2.FONT_HERSHEY_DUPLEX,1,green)
                x_fist_middle = x_fist+(w_fist/2)
                y_fist_middle = y_fist+(h_fist/2)
                if change_menu == "" or change_menu == "variable":
                    for i in range(len(menu_shapes)):
                        x_shape_start = menu_shapes[i]['startEnd'][0]
                        y_shape_start = menu_shapes[i]['startEnd'][1]
                        x_shape_end = menu_shapes[i]['startEnd'][2]
                        y_shape_end = menu_shapes[i]['startEnd'][3]
                        if (x_fist_middle > x_shape_start and x_fist_middle < x_shape_end) and (y_fist_middle > y_shape_start and y_fist_middle < y_shape_end):
                            if i < 6:
                                #Menu option selected    
                                play_obj = high_wav.play()
                                play_obj.wait_done()
                                action = i
                            else:
                                #Arrow selected
                                play_obj = low_wav.play()
                                play_obj.wait_done()
                                if i == 6:
                                    action = "back"
                                elif i == 7:
                                    action = "next"
                elif change_menu == "number":
                    for i in range(10):
                        x_shape_start = numbers_menu[i][0]
                        y_shape_start = numbers_menu[i][1]
                        x_shape_end = numbers_menu[i][2]
                        y_shape_end = numbers_menu[i][3]
                        if (x_fist_middle > x_shape_start and x_fist_middle < x_shape_end) and (y_fist_middle > y_shape_start and y_fist_middle < y_shape_end):
                            #Number selected    
                            play_obj = high_wav.play()
                            temp_code += str(i)
                            change_menu = ""
                            selected_bool = True
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
            if change_menu == "" and menu_page > 0:
                menu_page -= 1
            elif change_menu == "variable" and var_page > 0:
                var_page -= 1
            else:
                img = cv2.putText(img,"On first page",(10,30),cv2.FONT_HERSHEY_DUPLEX,1,red)
                print("On first page")
                error_bool = True
        elif action == "next":
            if change_menu == "" and menu_page < len(menu_item)-1:
                menu_page += 1
            elif change_menu == "variable" and var_page < math.floor(var_count/6): #Divides the number of variables by 6 and rounds down to split into 2x3 grid. Allows for first block to be new var
                var_page += 1
            else:
                img = cv2.putText(img,"On last page",(10,30),cv2.FONT_HERSHEY_DUPLEX,1,red)
                print("On last page")
                error_bool = True
        elif action != "":
            if change_menu == "":
                if menu_item[menu_page][action] == "end line":
                    if temp_code != "":
                        code = code + [temp_code]
                        temp_code = ""
                    else:
                        img = cv2.putText(img,"Syntax error",(10,30),cv2.FONT_HERSHEY_DUPLEX,1,red)
                        print("Syntax error - Cannot end line")
                        error_bool = True
                elif menu_item[menu_page][action] == "delete current line":
                    temp_code = ""
                elif menu_item[menu_page][action] == "delete last line":
                    if code:
                        code.pop()
                    else:
                        img = cv2.putText(img,"Syntax error",(10,30),cv2.FONT_HERSHEY_DUPLEX,1,red)
                        print("Syntax error - Cannot delete last line")
                        error_bool = True
                elif menu_item[menu_page][action] == "backspace":
                    if temp_code != "":
                        temp_code = temp_code[:-1]
                    else:
                        img = cv2.putText(img,"Syntax error",(10,30),cv2.FONT_HERSHEY_DUPLEX,1,red)
                        print("Syntax error - Cannot backspace")
                        error_bool = True
                elif menu_item[menu_page][action] == "space":
                    temp_code += " "
                elif menu_item[menu_page][action] == "execute":
                    if code:
                        try:
                            executable_string = "''\n"
                            for i in range(len(code)):
                                executable_string += code[i]+"\n"
                            executable_string += "''"
                            exec(executable_string)
                        except:
                            print("' " + code[i] + " ' encountered an error")
                            error_bool = True
                    else:
                        img = cv2.putText(img,"Syntax error",(10,30),cv2.FONT_HERSHEY_DUPLEX,1,red)
                        print("Syntax error - Cannot execute")
                elif menu_item[menu_page][action] == "if":
                    temp_code += "if"
                elif menu_item[menu_page][action] == "while":
                    temp_code += "while"
                elif menu_item[menu_page][action] == "print":
                    temp_code += "print("
                elif menu_item[menu_page][action] == "number":
                    change_menu = "number"
                elif menu_item[menu_page][action] == "variable":
                    change_menu = "variable"
                elif menu_item[menu_page][action] == "not":
                    temp_code += "not"
                elif menu_item[menu_page][action] == "True":
                    temp_code += "True"
                elif menu_item[menu_page][action] == "False":
                    temp_code += "False"
                elif menu_item[menu_page][action] == "!":
                    temp_code += "!"
                elif menu_item[menu_page][action] == "=":
                    temp_code += "="
                elif menu_item[menu_page][action] == "+":
                    temp_code += "+"
                elif menu_item[menu_page][action] == "-":
                    temp_code += "-"
                elif menu_item[menu_page][action] == "(":
                    temp_code += "("
                elif menu_item[menu_page][action] == ")":
                    temp_code += ")"
                elif menu_item[menu_page][action] == "[":
                    temp_code += "["
                elif menu_item[menu_page][action] == "]":
                    temp_code += "]"
                elif menu_item[menu_page][action] == "{":
                    temp_code += "{"
                elif menu_item[menu_page][action] == "}":
                    temp_code += "}"
                elif menu_item[menu_page][action] == ":":
                    temp_code += ":"
                elif menu_item[menu_page][action] == "None":
                    temp_code += "None"
                elif menu_item[menu_page][action] == '"': #Quotes changed to allow entry of "
                    temp_code += '"'
                elif menu_item[menu_page][action] == "'":
                    temp_code += "'"
                elif menu_item[menu_page][action] == "indent":
                    temp_code += "    "
                elif menu_item[menu_page][action] == "remove indent":
                    if temp_code != "":
                        temp_code = temp_code[:-4]
                    else:
                        img = cv2.putText(img,"Syntax error",(10,30),cv2.FONT_HERSHEY_DUPLEX,1,red)
                        print("Syntax error - Cannot backspace")
                        error_bool = True
                else:
                    img = cv2.putText(img,"Handling error",(10,30),cv2.FONT_HERSHEY_DUPLEX,1,red)
                    print("Error - Command not handled")
                    error_bool = True
            elif change_menu == "variable":
                if var_page == 0 and action == 0:
                    var_count += 1
                    temp_code += "variable"+str(var_count)
                else:
                    temp_code += "variable"+str((var_page*6)+action)
                change_menu = ""
            else:
                img = cv2.putText(img,"Handling error",(10,30),cv2.FONT_HERSHEY_DUPLEX,1,red)
                print("Error - Menu not handled")
                error_bool = True
                
            if not error_bool: selected_bool = True #If no errors mark a selection has been made
        #else:
            #selected_bool = False
        """
        #
        """
        if selected_bool:
            print("---")
            print(temp_code)
            print(code)
            print("---")
        """
        #Set variables for next stage of while loop
        """
        #If body part(s) detected set "previous state" boolean to true, if none set to false
        palms_bool = True if palms_count > 0 else False
        fists_bool = True if fists_count > 0 else False
        selected_bool = False
        error_bool = False
            
        #Clear current counts
        palms_count = 0
        fists_count = 0
        action = ""
        """
        #
        """
    else:
        break
    
camera.release()
cv2.destroyAllWindows()
