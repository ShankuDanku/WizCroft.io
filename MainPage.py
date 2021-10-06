from tkinter import *
from Palette import *
from CustomAnimations import HeaderAnimationSlidingDown, HeaderAnimationSlidingUp, PlaceSlideRightAnimation, \
    PlaceScrollUp, PlaceScrollDown, psFade, spFade
from CustomWidgets import StdBtn, AttGroup, OrgGroup, RndBtn, InputBar, PopUp


def Header(client):
    header = Frame(client, bg=secondary)
    header.place(x=0, y=-60, relwidth=1)
    welcome = Label(header, fg=content, bg=secondary, text='Welcome Sashank', font=std_font)
    welcome.pack(side=LEFT, pady=(10, 20))
    # logout = StdBtn("Logout", header, ('Uni Sans-Trial Book', 20, 'normal'))
    # logout.config(bg=secondary, fg=content, activeforeground='white', activebackground='grey', command=client.quit)
    logout = RndBtn(header, 'Logout', primary, secondary, 'black', command=client.quit)
    logout.pack(side=RIGHT, pady=(10, 20), padx=(5, 5))
    header.bind('<Enter>', lambda event: HeaderAnimationSlidingDown(header))
    header.bind('<Leave>', lambda event: HeaderAnimationSlidingUp(header))


def MainPage(client, user=None):
    Header(client)
    body = Frame(client, bg=primary)
    body.place(x=5, y=100, relwidth=1, relheight=0.85)
    org = Button(body, fg=content, bg=secondary, text='Organize', font=('Uni Sans Thin CAPS', 20, 'normal')
                 , relief='flat', overrelief='flat', bd=0, cursor='hand2')
    org.place(x=0, y=0, relwidth=0.49)
    att = Button(body, fg=content, bg=secondary, text='Attend', font=('Uni Sans Thin CAPS', 20, 'normal')
                 , relief='flat', overrelief='flat', bd=0, cursor='hand2')

    att.place(relx=0.51, y=0, relwidth=0.49)

    def GetOrgFrame():
        if len(body.winfo_children()) > 2:
            body.winfo_children()[-1].destroy()
            return GetOrgFrame()
        else:
            # att.config(bg=secondary)
            # org.config(bg=primary)
            psFade(att)
            spFade(org)
            OrgFrame(body)

    def GetAttFrame():
        if len(body.winfo_children()) > 2:
            body.winfo_children()[-1].destroy()
            return GetAttFrame()
        else:
            # att.config(bg=primary)
            # org.config(bg=secondary)
            psFade(org)
            spFade(att)
            AttFrame(body)

    org.config(command=GetOrgFrame)
    att.config(command=GetAttFrame)


def OrgFrame(parent):
    org_frame = Frame(parent, bg=primary)
    org_frame.place(x=0, y=100, relwidth=0.98, relheight=0.98)
    org_btn = RndBtn(org_frame, 'Create', secondary, primary, accent)
    org_btn.pack(anchor='w', pady=(0, 25), padx=(48, 0))

    def Pop_Up(parent):
        top = PopUp(parent)
        bar = InputBar('Enter Group Name', top, font=('Uni Sans-Trial Book', 20, 'normal'))
        bar.pack(pady=(20, 0))
        create_btn = RndBtn(top, 'Create Group', secondary, primary, accent)
        create_btn.pack(pady=(20, 0))

    org_btn.command = lambda: Pop_Up(parent)
    org_scroll_btn = Frame(org_frame, bg=primary, width=80, height=650)
    org_scroll_btn.pack(side=RIGHT)
    org_scroll_btn.pack_propagate(False)
    up_arrow = PhotoImage(file='Images/Arrow .png')
    org_up_scroll = Label(org_scroll_btn, image=up_arrow, bg=primary)
    org_up_scroll.image = up_arrow
    org_up_scroll.pack()
    org_up_scroll.bind('<Button-1>', lambda args: PlaceScrollUp(org_body))
    down_arrow = PhotoImage(file='Images/ArrowUD.png')
    org_down_scroll = Label(org_scroll_btn, image=down_arrow, bg=primary)
    org_down_scroll.image = down_arrow
    org_down_scroll.pack(side=BOTTOM, pady=(0, 100))
    org_down_scroll.bind('<Button-1>', lambda event: PlaceScrollDown(org_body))
    org_scroll = Frame(org_frame, bg=primary, height=740)
    org_body = Frame(org_scroll, bg=primary)
    org_body.place(x=100, y=0)
    org_scroll.pack(fill='x', expand=True)
    for x in range(0, 10):
        grp = OrgGroup(org_body, 'Padi Hai')
        grp.grid(row=x // 4, column=x % 4, padx=38, pady=(0, 20))
    PlaceSlideRightAnimation(org_frame)


def AttFrame(parent):
    att_frame = Frame(parent, bg=primary)
    att_frame.place(x=0, y=100, relwidth=0.98, relheight=0.98)
    att_btn = RndBtn(att_frame, 'Join', secondary, primary, accent)
    att_btn.pack(anchor='e', pady=(0, 25), padx=(0, 48))

    def Pop_Up(parent):
        top = PopUp(parent)
        bar = InputBar('Enter Group ID', top, font=('Uni Sans-Trial Book', 20, 'normal'))
        bar.pack(pady=(20, 0))
        join_btn = RndBtn(top, 'Join Group', secondary, primary, accent)
        join_btn.pack(pady=(20, 0))

    att_btn.command = lambda: Pop_Up(parent)
    att_scroll_btn = Frame(att_frame, bg=primary, width=80, height=650)
    att_scroll_btn.pack(side=LEFT)
    att_scroll_btn.pack_propagate(False)
    up_arrow = PhotoImage(file='Images/Arrow .png')
    att_up_scroll = Label(att_scroll_btn, image=up_arrow, bg=primary)
    att_up_scroll.image = up_arrow
    att_up_scroll.pack()
    att_up_scroll.bind('<Button-1>', lambda args: PlaceScrollUp(att_body))
    down_arrow = PhotoImage(file='Images/ArrowUD.png')
    att_down_scroll = Label(att_scroll_btn, image=down_arrow, bg=primary)
    att_down_scroll.image = down_arrow
    att_down_scroll.pack(side=BOTTOM, pady=(0, 100))
    att_down_scroll.bind('<Button-1>', lambda event: PlaceScrollDown(att_body))
    att_scroll = Frame(att_frame, bg=primary, height=740)
    att_body = Frame(att_scroll, bg=primary)
    att_body.place(x=100, y=0)
    att_scroll.pack(fill='x', expand=True)
    for x in range(0, 10):
        grp = AttGroup(att_body, 'Test' + str(x), 'Admin',bool(x%2))
        grp.grid(row=x // 4, column=x % 4, padx=38, pady=(0, 20))
    PlaceSlideRightAnimation(att_frame)


def ManageGroup(parent):
    btn_bar = Frame(parent, bg=primary)
    btn_bar.place(relwidth=1)
    btn_bar.grid_columnconfigure(0, weight=1)
    btn_bar.grid_columnconfigure(1, weight=1)
    btn_bar.grid_columnconfigure(2, weight=1)
    back = RndBtn(btn_bar, 'Go Back', secondary, primary, accent)
    back.grid(sticky='w')
    activate = RndBtn(btn_bar, 'Activate', secondary, primary, accent)
    activate.grid(row=0, column=1)
    end_m = RndBtn(btn_bar, 'End meeting', secondary, primary, accent)
    end_m.grid(row=0, column=2, sticky='e', padx=(0, 10))
