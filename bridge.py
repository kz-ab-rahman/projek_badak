#!python3

import pyautogui
import time
import os
import global_param


def new_msg_to_req_box():
    print("in new_msg_to_req_box")
    # triple click at newMsgPos, ctrl+c
    pyautogui.doubleClick(global_param.newMsgPos)
    pyautogui.click(global_param.newMsgPos)
    pyautogui.hotkey('ctrl', 'c')
    # move to reqBox, paste, enter
    pyautogui.click(global_param.reqBoxPos)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.typewrite(['enter'])
    return


def res_box_to_rep_msg():
    print("in res_box_to_rep_msg")
    # move to resBox, ctrl+A, ctrl+C
    pyautogui.click(global_param.resBoxPos)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')

    # move to replyBox, ctrl+V, enter
    pyautogui.click(global_param.replyBoxPos)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(1)
    pyautogui.typewrite(['enter'])
    return


def new_msg():
    print("in new_msg")
    # check the pixel RGB color at the position of new msg.
    if pyautogui.pixelMatchesColor(global_param.newMsgPos[0], global_param.newMsgPos[1], global_param.newMsgPixColor):
        # second level check to ensure trigger happens only because of whatsapp
        if pyautogui.pixelMatchesColor(global_param.newMsgPos[0] - 20, global_param.newMsgPos[1], (22, 33, 39)):
            print("New request received")
            return True
        else:
            return False
    else:
        return False


print('Make sure Whatsapp is opened, logged-in, and snapped to the right')
input('Press enter to start Virtual Admin...')
os.system("start /wait cmd /c py -3 virtual_admin_gui.py")  # open new terminal and launch GUI
time.sleep(1)
print('Virtual Admin is running. Press Ctrl-C to quit.')
try:
    while True:
        # will stuck in this loop until new whatsapp msg comes in
        while not new_msg():
            # check for new order
            # if new order, send alert and come back here
            time.sleep(1)

        new_msg_to_req_box()
        time.sleep(1)
        res_box_to_rep_msg()
except KeyboardInterrupt:
    print('\nDone.')
