#!python3

import pyautogui, time, os
import globalParam

def newMsg2ReqBox():
    print("in newMsg2ReqBox")
    #triple click at newMsgPos, ctrl+c
    pyautogui.doubleClick(globalParam.newMsgPos)
    pyautogui.click(globalParam.newMsgPos)
    pyautogui.hotkey('ctrl', 'c')
    #move to reqBox, paste, enter
    pyautogui.click(globalParam.reqBoxPos)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.typewrite(['enter'])
    return

def resBox2RepMsg():
    print("in resBox2RepMsg")
    #move to resBox, ctrl+A, ctrl+C
    pyautogui.click(globalParam.resBoxPos)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')

    #move to replyBox, ctrl+V, enter
    pyautogui.click(globalParam.replyBoxPos)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.typewrite(['enter'])
    return

def newMsg():
    print("in newMsg")
    #check the pixel RGB color at the position of new msg.
    if pyautogui.pixelMatchesColor(globalParam.newMsgPos[0], globalParam.newMsgPos[1], (globalParam.newMsgPixColor)):
        #second level check to ensure trigger happens only because of whatsapp
        if pyautogui.pixelMatchesColor(globalParam.newMsgPos[0] - 20, globalParam.newMsgPos[1], (22,33,39)):
            print("you have new request")
            return True
        else:
            return False
    else:
        return False


print('Make sure Whatsapp is opened and logged-in')
input('Press enter to start Virtual Admin...')
os.system("start /wait cmd /c py -3 virtualAdminGUI.py") #open new terminal and lauch GUI
time.sleep(1)
print('Virtual Admin is running. Press Ctrl-C to quit.')
try:
    while True:
        #will stuck in this loop until new whatsapp msg comes in
        while not newMsg():
            #check for new order
            #if new order, send alert and come back here
            time.sleep(1)

        newMsg2ReqBox()
        time.sleep(1)
        resBox2RepMsg()
except KeyboardInterrupt:
    print('\nDone.')
