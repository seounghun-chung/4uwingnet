import pyautogui as p
from pywinauto.application import Application

app = Application().start("notepad.exe")
app.UntitledNotepad.menu_select("Help->About Notepad")
for ii in range(0,10):
    msleep(100)
    print(p.position())
