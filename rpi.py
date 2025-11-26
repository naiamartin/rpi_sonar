import tkinter as tk
import math
import threading
import random

root = tk.Tk()
canvas = tk.Canvas(root, width=500, height=500, borderwidth=0, highlightthickness=0,
                   bg="black")
canvas.grid()

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

canvas.create_circle(250, 250,  250, fill="#383838", outline="#0E3618", width=1)

angle = 0
forward = True
points = {}

def moving_line():
    global angle
    global forward

    canvas.delete("line") 

    radians = math.radians(angle)
    x = 250 + 250 * math.cos(radians)
    y = 250 - 250 * math.sin(radians)

    canvas.create_line(250, 250, x, y, fill="#4CFF4C", width=2, tags="line")

    if angle+2 <= 180 and forward:
        angle = (angle + 2) % 360
        try:
            canvas.delete(points[angle])
        except:
            pass
        draw_danger_point(angle, random.randint(0,250))       
    else:
        forward = False
        if(forward == False):
            angle = (angle -2) % 360
            if(angle+2<=2):
                forward = True    
        try:
            canvas.delete(points[angle])
        except:
            pass
        draw_danger_point(angle, random.randint(0,250))
    canvas.after(40, moving_line) 

def draw_danger_point(point, distance):
    radians = math.radians(point)
    x = 250 + distance * math.cos(radians)
    y = 250 - distance * math.sin(radians)

    r = 3
    o = canvas.create_oval(x - r, y - r, x + r, y + r, fill="#E14CFF", outline="", tags=str(angle))
    points[angle] = o
    canvas.tag_raise(str(angle))

t1 = threading.Thread(target=moving_line, daemon=True)
t1.start()

root.title("Sonar Display")
root.mainloop()