from tkinter import Button, Entry, END, Frame, Label, Canvas, LEFT, RIGHT, Toplevel
from Palette import *


def round_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]

    return canvas.create_polygon(points, **kwargs, smooth=True, splinesteps=8192)


class StdBtn(Button):
    def __init__(self, text, parent, font=std_font, **kwargs):
        super().__init__(parent, text=text, bg='grey', fg='white', font=font,
                         cursor='hand2',
                         activebackground=secondary, relief='flat', overrelief='flat', bd=0, activeforeground=content)


class InputBar(Entry):
    def __init__(self, text, parent, font):
        super().__init__(parent, font=font, fg='grey', bg=secondary, width=25, bd=10, relief='flat',
                         insertbackground=content)
        self.def_text = text
        self.insert(0, self.def_text)
        self.bind("<FocusIn>", lambda args: self.focus_in(self.def_text))
        self.bind("<FocusOut>", lambda args: self.focus_out(self.def_text))

    def focus_out(self, widget_text):
        if len(self.get()) == 0:
            self.delete(0, END)
            self.config(fg='grey')
            self.insert(0, widget_text)

    def focus_in(self, widget_text):
        if self.get() == widget_text:
            self.config(fg=content)
            self.delete(0, END)


class AttGroup(Canvas):
    def __init__(self, parent, name, organizer, active=False, **kw):
        super().__init__(parent, width=340, height=340, bd=0, bg=primary, highlightthickness=0)
        self.frame = Frame(self, bg=secondary, height=180, width=300, **kw)
        self.frame.pack_propagate(False)
        self.active = active
        if self.active:
            self.indicator = accent
        else:
            self.indicator = inactive
        self.frame2 = Frame(self, bg=self.indicator)
        self.name = Label(self.frame2, text=name, bg=self.indicator, fg=content, font=('Uni Sans-Trial Book', 15,
                                                                                       'normal'))
        self.name.pack(pady=(20, 20), anchor='w')
        self.organizer = Label(self.frame, text=organizer, bg=secondary, fg=content,
                               font=('Uni Sans-Trial Book', 20, 'normal'))
        self.organizer.pack(pady=(10, 50))
        self.button = RndBtn(self.frame, 'Attend', 'grey', secondary, primary, accent, 'white')
        self.button.pack()
        self.attending = False
        self.bg_up = round_rectangle(self, 0, 10, 340, 100, radius=50, fill=self.indicator, outline='')
        self.bg = round_rectangle(self, 0, 105, 340, 340, radius=100, fill=secondary, outline='')
        super().create_window(20, 20, window=self.frame2, anchor='nw')
        super().create_window(20, 120, window=self.frame, anchor='nw')


class OrgGroup(Canvas):
    def __init__(self, parent, name, active=False, **kw):
        super().__init__(parent, width=340, height=340, bd=0, bg=primary, highlightthickness=0)
        self.frame = Frame(self, bg=secondary, height=180, width=300, **kw)
        self.frame.pack_propagate(False)
        self.active = active
        if self.active:
            self.indicator = accent
        else:
            self.indicator = inactive
        self.frame2 = Frame(self, bg=self.indicator)
        self.name = Label(self.frame2, text=name, bg=self.indicator, fg=content,
                          font=('Uni Sans-Trial Book', 15, 'normal'))
        self.name.pack(pady=10, anchor='w')
        self.btn_frame = Frame(self.frame, bg=secondary)
        self.active = active
        self.btn1 = RndBtn(self.btn_frame, 'Activate', 'green', secondary, primary, accent, 'white')

        def func():
            if self.active:
                self.btn1.bg = 'red'
                self.btn1.label.config(text='Deactivate')
                self.indicator = accent
            else:
                self.btn1.bg = 'green'
                self.btn1.label.config(text='Activate')
                self.indicator = inactive
            self.active = ~self.active
            self.indicate()
        self.btn1.command = func
        self.btn1.pack(side=LEFT)
        self.btn2 = RndBtn(self.btn_frame, 'Get ID', 'grey', secondary, primary, accent, 'white')
        self.btn2.command = lambda: GetID(self)
        self.btn2.pack(side=RIGHT)
        self.btn_frame.pack(pady=25, fill='x')
        self.button = RndBtn(self.frame, 'View Attendance', 'grey', secondary, primary, accent, 'white',
                             font=('Uni Sans-Trial Book', 15, 'normal'))
        self.button.pack(side=LEFT)
        self.bg_up = round_rectangle(self, 0, 0, 340, 100, radius=50, fill=self.indicator, outline='')
        self.bg = round_rectangle(self, 0, 105, 340, 340, radius=100, fill=secondary, outline='')
        super().create_window(20, 20, window=self.frame2, anchor='nw')
        super().create_window(20, 120, window=self.frame, anchor='nw')
        func()

    def indicate(self):
        self.name.config(bg=self.indicator)
        self.frame2.config(bg=self.indicator)
        self.itemconfig(self.bg_up, fill=self.indicator)


class RndBtn(Canvas):
    def __init__(self, parent, text, bg, corner_bg, hover_bg=secondary, hover_fg=content, text_fg=content,
                 font=('Uni Sans-Trial Book', 20, 'normal'), command=None, **kw):
        super().__init__(parent, highlightthickness=0, bd=0, bg=corner_bg, relief='flat')
        self.bg = bg
        self.command = command
        self.frame = Frame(self, bg=self.bg)
        self.label = Label(self.frame, text=text, bg=self.bg, fg=text_fg, font=font)
        self.label.pack()
        self.config(height=self.label.winfo_reqheight() + 20, width=self.label.winfo_reqwidth() + 30)
        self.capsule = round_rectangle(self, 0, 0, self.label.winfo_reqwidth() + 30, self.label.winfo_reqheight() + 20,
                                       (self.label.winfo_reqheight() + 20) // 2, fill=self.bg, outline='', tags='rect')
        self.create_window(15, 10, window=self.frame, anchor='nw')

        def enter():
            self.config(cursor='hand2')
            self.itemconfig(self.capsule, fill=hover_bg)
            self.label.config(cursor='hand2', bg=hover_bg, fg=hover_fg)

        def leave():
            self.config(cursor='')
            self.itemconfig(self.capsule, fill=self.bg)
            self.label.config(cursor='', bg=self.bg, fg=text_fg)

        def press(event):
            self.itemconfig(self.capsule, fill=corner_bg)
            self.label.config(bg=corner_bg, fg=text_fg)

        def release(event):
            if self.command is not None:
                self.command()
            if self.winfo_exists() == 1:
                self.resize()
                self.itemconfig(self.capsule, fill=hover_bg)
                self.label.config(bg=hover_bg, fg=hover_fg)

        self.bind('<Enter>', lambda args: enter())
        self.bind('<Leave>', lambda args: leave())
        self.bind('<ButtonPress-1>', press)
        self.label.bind('<ButtonPress-1>', press)
        self.bind('<ButtonRelease-1>', release)
        self.label.bind('<ButtonRelease-1>', release)

    def resize(self):
        self.config(height=self.label.winfo_reqheight() + 20, width=self.label.winfo_reqwidth() + 30)
        self.capsule = round_rectangle(self, 0, 0, self.label.winfo_reqwidth() + 30, self.label.winfo_reqheight() + 20,
                                       (self.label.winfo_reqheight() + 20) // 2, fill=self.bg, outline='', tags='rect')


class PopUp(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("500x250+730+415")
        self.overrideredirect(1)
        self.resizable(width=False, height=False)
        self.close_btn = RndBtn(self, 'X', secondary, primary, '#8B0000')
        self.close_btn.pack(anchor='e')
        self.close_btn.command = self.destroy
        self.config(bg=primary)


def GetID(parent):
    top = PopUp(parent)
    id = Label(top, bg=secondary, fg=content, font=std_font, text='ID')
    id.pack(pady=20)
