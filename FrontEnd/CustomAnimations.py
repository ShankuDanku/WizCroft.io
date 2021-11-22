from tkinter import *
from Palette import *


def HeaderAnimationSlidingDown(header, offset=-60):
    if offset != 5:
        header.place(x=0, y=offset, relwidth=1)
        offset += 5
        header.after(10, HeaderAnimationSlidingDown, header, offset)


def HeaderAnimationSlidingUp(header, offset=0):
    if offset != -65:
        header.place(x=0, y=offset, relwidth=1)
        offset -= 5
        header.after(10, HeaderAnimationSlidingUp, header, offset)


def PackRightSlideAnimation(frame, offset=0):
    if offset != 275:
        frame.pack(side=RIGHT, padx=(0, offset))
        offset += 5
        frame.after(1, PackRightSlideAnimation, frame, offset)


def PackLeftSlideDownAnimation(frame, offset=0):
    if offset != 110:
        frame.pack(side=LEFT, pady=(offset, 0))
        offset += 10
        frame.after(10, PackLeftSlideDownAnimation, frame, offset)


def ColorFade(frame, item, r=44, g=44, b=50):
    if r != 172 and g != 172 and b != 172:
        color = '#' + str(hex(r))[2:] + str(hex(g))[2:] + str(hex(b))[2:]
        frame.itemconfig(item, fill=color)
        if r != 172:
            r += 8
        if g != 172:
            g += 8
        if b != 172:
            b += 8
        frame.after(50, ColorFade, frame, item, r, g, b)


def psFade(btn, r=44, g=47, b=51):
    if r != 35 and g != 39 and b != 42:
        color = '#' + str(hex(r))[2:] + str(hex(g))[2:] + str(hex(b))[2:]
        btn.config(bg=color)
        if r != 35:
            r -= 1
        if g != 39:
            g -= 1
        if b != 42:
            b -= 1
        btn.after(25, psFade, btn, r, g, b)


def spFade(btn, r=35, g=39, b=42):
    if r != 44 and g != 47 and b != 51:
        color = '#' + str(hex(r))[2:] + str(hex(g))[2:] + str(hex(b))[2:]
        btn.config(bg=color)
        if r != 44:
            r += 1
        if g != 47:
            g += 1
        if b != 51:
            b += 1
        btn.after(25, spFade, btn, r, g, b)


def PlaceSlideRightAnimation(frame, offset=1000):
    if offset != 0:
        frame.place(x=offset, y=100)
        offset -= 10
        frame.after(1, PlaceSlideRightAnimation, frame, offset)


def PlaceScrollUp(frame):
    def ScrollUpAnimation(panel, start_y, offset=0):
        if offset != 360:
            offset += 6
            panel.place(x=100, y=offset + start_y)
            panel.after(1, ScrollUpAnimation, panel, start_y, offset)

    current_y = int(frame.place_info()['y'])
    if current_y != 0:
        ScrollUpAnimation(frame, current_y)


def PlaceScrollDown(frame):
    def ScrollDownAnimation(panel, start_y, offset=0):
        if offset != -360:
            offset -= 6
            panel.place(x=100, y=offset + start_y)
            panel.after(1, ScrollDownAnimation, panel, start_y, offset)

    current_y = int(frame.place_info()['y'])
    stop = int(((len(frame.winfo_children())) // 4) - 1) * (-360)
    if current_y != stop:
        ScrollDownAnimation(frame, current_y)
