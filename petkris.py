
import random
import tkinter as tk
import pyautogui
x = 1400
cycle = 0
check = 1
idle_num =[1,2,3,4]
sleep_num = [10,11,12,13,15]
walk_left = [6,7]
walk_right = [8,9]
event_number = random.randrange(1,3,1)
impath = 'C:\\your\\path\\to\\file'

window = tk.Tk()

#call buddy's action .gif to an array
idle = [tk.PhotoImage(file=impath+'idle.gif',format = 'gif -index %i' %(i)) for i in range(5)]#idle gif , 5 frames#idle to sleep gif, 8 frames
sleep = [tk.PhotoImage(file=impath+'sleep.gif',format = 'gif -index %i' %(i)) for i in range(3)]#sleep gif, 3 frames
walk = [tk.PhotoImage(file=impath+'walk.gif',format = 'gif -index %i' %(i)) for i in range(8)]#walk to left gif, 8 frames
walk2 = [tk.PhotoImage(file=impath+'walk2.gif',format = 'gif -index %i' %(i)) for i in range(8)]#walk to right gif, 8 frames
