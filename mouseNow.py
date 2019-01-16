#! python3
# mouseNow.py - Displays the mouse cursor's current position.
import pyautogui
print('Press Ctrl-C to quit.')
try:
   while True:
        # Get and print the mouse coordinates.
        x, y = pyautogui.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        pixelColor = pyautogui.screenshot().getpixel((x, y))
        positionStr += ' RGB: (' + str(pixelColor[0]).rjust(3)
        positionStr += ', ' + str(pixelColor[1]).rjust(3)
        positionStr += ', ' + str(pixelColor[2]).rjust(3) + ')'
        print(positionStr)
except KeyboardInterrupt:
    print('\nDone.')



"""
positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
pixelColor = pyautogui.screenshot().getpixel((x, y))
positionStr += ' RGB: (' + str(pixelColor[0]).rjust(3)
positionStr += ', ' + str(pixelColor[1]).rjust(3)
positionStr += ', ' + str(pixelColor[2]).rjust(3) + ')'
print(positionStr)

#move the mouse:
pyautogui.moveTo(1342, 1006, duration=0.5)

#move the mouse and click:
pyautogui.click(100, 150)




#triple click at newMsgPos, ctrl+c
pyautogui.doubleClick(1340, 930)
pyautogui.click(1340, 930)
pyautogui.hotkey('ctrl', 'c')

#move to reqBox, paste, enter
pyautogui.click(80, 45)
pyautogui.hotkey('ctrl', 'v')
pyautogui.typewrite(['enter'])

#move to resBox, ctrl+A, ctrl+C
pyautogui.click(85,70)
pyautogui.hotkey('ctrl', 'a')
pyautogui.hotkey('ctrl', 'c')

#move to replyBox, ctrl+V, enter
pyautogui.click(1500,1000)
pyautogui.hotkey('ctrl', 'v')
pyautogui.typewrite(['enter'])


"""