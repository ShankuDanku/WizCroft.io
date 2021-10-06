from ctypes import windll
from LoginAndSignupPage import LoginPage
from MainPage import *

gui = Tk()
gui.state('zoomed')
gui.title('WizCroft.io')
# gui.tk.call('tk', 'scaling', 1.0)
gui.minsize(windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
gui.config(bg=primary)
gui.resizable(width=False, height=False)
gui.minsize(1920, 1080)

windll.shcore.SetProcessDpiAwareness(1)

LoginPage(gui,True)
#MainPage(gui)
gui.mainloop()
