from tkinter import *
from tkinter import filedialog

from Palette import *
from CustomAnimations import HeaderAnimationSlidingDown, HeaderAnimationSlidingUp, PlaceSlideRightAnimation, \
    PlaceScrollUp, PlaceScrollDown, psFade, spFade
from CustomWidgets import StdBtn, AttGroup, OrgGroup, RndBtn, InputBar, PopUp
from Firebase.Database import db, CreateGroup, CheckGroup, JoinGroup, CheckAttendee, GetSessions, StrToTime, \
    GetAttendeeList
import LoginAndSignupPage
from datetime import *
import pandas as pd


def Header(client, name):
    header = Frame(client, bg=secondary)
    header.place(x=0, y=-60, relwidth=1)
    welcome = Label(header, fg=content, bg=secondary, text='Welcome, ' + name, font=std_font)
    welcome.pack(side=LEFT, pady=(10, 20))

    # logout = StdBtn("Logout", header, ('Uni Sans-Trial Book', 20, 'normal'))
    # logout.config(bg=secondary, fg=content, activeforeground='white', activebackground='grey', command=client.quit)
    def Logout():
        for x in client.winfo_children():
            x.destroy()
        LoginAndSignupPage.LoginPage(client, True)

    logout = RndBtn(header, 'Logout', primary, secondary, 'black', command=Logout)
    logout.pack(side=RIGHT, pady=(10, 20), padx=(5, 5))
    header.bind('<Enter>', lambda event: HeaderAnimationSlidingDown(header))
    header.bind('<Leave>', lambda event: HeaderAnimationSlidingUp(header))


def MainPage(client, user=None):
    Header(client, db.child('Users').child(user).child('name').get().val())
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
            psFade(att)
            spFade(org)
            OrgFrame(body, client, user)

    def GetAttFrame():
        if len(body.winfo_children()) > 2:
            body.winfo_children()[-1].destroy()
            return GetAttFrame()
        else:
            psFade(org)
            spFade(att)
            AttFrame(body, client, user)

    org.config(command=GetOrgFrame)
    att.config(command=GetAttFrame)


def OrgFrame(parent, client, user):
    org_frame = Frame(parent, bg=primary)
    org_frame.place(relwidth=0.98, relheight=0.98)
    org_btn = RndBtn(org_frame, 'Create', secondary, primary, accent)
    org_btn.pack(anchor='w', pady=(0, 25), padx=(48, 0))

    def Pop_Up(parent):
        top = PopUp(parent, bg=secondary)
        bar = InputBar('Enter Group Name', top, font=('Uni Sans-Trial Book', 20, 'normal'))
        bar.pack(pady=(20, 0))
        create_btn = RndBtn(top, 'Create Group', secondary, secondary, accent)
        create_btn.pack(pady=(20, 0))

        def createGroup():
            if bar.get() != 'Enter Group Name':
                if bar.get() in CheckGroup(user):
                    PopUp(client, 'Group already exists!', secondary)
                    top.destroy()
                else:
                    CreateGroup(bar.get(), user)
                    PopUp(client, 'Group Created!', secondary)
                    top.destroy()

        create_btn.command = createGroup

    org_btn.command = lambda: Pop_Up(parent)
    org_scroll_btn = Frame(org_frame, bg=primary, width=80, height=650)
    org_scroll_btn.pack(side=RIGHT)
    org_scroll_btn.pack_propagate(False)
    up_arrow = PhotoImage(file='../Images/Arrow .png')
    org_up_scroll = Label(org_scroll_btn, image=up_arrow, bg=primary)
    org_up_scroll.image = up_arrow
    org_up_scroll.pack()
    org_up_scroll.bind('<Button-1>', lambda args: PlaceScrollUp(org_body))
    down_arrow = PhotoImage(file='../Images/ArrowUD.png')
    org_down_scroll = Label(org_scroll_btn, image=down_arrow, bg=primary)
    org_down_scroll.image = down_arrow
    org_down_scroll.pack(side=BOTTOM, pady=(0, 100))
    org_down_scroll.bind('<Button-1>', lambda event: PlaceScrollDown(org_body))
    org_scroll = Frame(org_frame, bg=primary, height=740)
    org_body = Frame(org_scroll, bg=primary)
    org_body.place(x=100, y=0)
    org_scroll.pack(fill='x', expand=True)
    pos = 0
    groups = db.child('Groups').get().val()
    for key in groups:
        if groups[key]['Organizer'] == user:
            grp = OrgGroup(org_body, groups[key]['Name'], key, active=groups[key]['Active'] != 'False')

            def func():
                for x in parent.winfo_children():
                    x.destroy()
                ManageGroup(parent, client, user, key)

            grp.button.command = func
            grp.grid(row=pos // 4, column=pos % 4, padx=38, pady=(0, 20))
            pos += 1
    PlaceSlideRightAnimation(org_frame)


def AttFrame(parent, client, user):
    att_frame = Frame(parent, bg=primary)
    att_frame.place(relwidth=0.98, relheight=0.98)
    att_btn = RndBtn(att_frame, 'Join', secondary, primary, accent)
    att_btn.pack(anchor='e', pady=(0, 25), padx=(0, 48))

    def Pop_Up(parent):
        top = PopUp(parent, bg=secondary)
        bar = InputBar('Enter Group ID', top, font=('Uni Sans-Trial Book', 20, 'normal'))
        bar.pack(pady=(20, 0))
        join_btn = RndBtn(top, 'Join Group', secondary, primary, accent)
        join_btn.pack(pady=(20, 0))

        def joinGroup():
            if bar.get() != 'Enter Group ID':
                if bar.get() not in db.child('Groups').get().val().keys():
                    PopUp(client, "Group does not exist!", secondary)
                    top.destroy()
                elif user == db.child('Groups').child(bar.get()).child('Organizer').get().val():
                    PopUp(client, "Cannot join group you organize", secondary)
                    top.destroy()
                elif CheckAttendee(bar.get(), user):
                    PopUp(client, 'Already joined this group!', secondary)
                    top.destroy()
                else:
                    JoinGroup(bar.get(), user)
                    PopUp(client, 'Joined group', secondary)
                    top.destroy()

        join_btn.command = joinGroup

    att_btn.command = lambda: Pop_Up(parent)
    att_scroll_btn = Frame(att_frame, bg=primary, width=80, height=650)
    att_scroll_btn.pack(side=LEFT)
    att_scroll_btn.pack_propagate(False)
    up_arrow = PhotoImage(file='../Images/Arrow .png')
    att_up_scroll = Label(att_scroll_btn, image=up_arrow, bg=primary)
    att_up_scroll.image = up_arrow
    att_up_scroll.pack()
    att_up_scroll.bind('<Button-1>', lambda args: PlaceScrollUp(att_body))
    down_arrow = PhotoImage(file='../Images/ArrowUD.png')
    att_down_scroll = Label(att_scroll_btn, image=down_arrow, bg=primary)
    att_down_scroll.image = down_arrow
    att_down_scroll.pack(side=BOTTOM, pady=(0, 100))
    att_down_scroll.bind('<Button-1>', lambda event: PlaceScrollDown(att_body))
    att_scroll = Frame(att_frame, bg=primary, height=740)
    att_body = Frame(att_scroll, bg=primary)
    att_body.place(x=100, y=0)
    att_scroll.pack(fill='x', expand=True)
    pos = 0
    groups = db.child('Attendees').get().val()
    grp_data = db.child('Groups').get().val()
    for key in groups:
        if groups[key]['User'] == user:
            grp_id = groups[key]['Group']
            grp = AttGroup(att_body, grp_data[grp_id]['Name'],
                           db.child('Users').child(grp_data[grp_id]['Organizer']).child('name').get().val(),
                           grp_id, user,
                           grp_data[grp_id]['Active'] == 'True')
            grp.grid(row=pos // 4, column=pos % 4, padx=38, pady=(0, 20))
            pos += 1
    PlaceSlideRightAnimation(att_frame)


def ManageGroup(parent, client, user, group):
    btn_bar = Frame(parent, bg=primary)
    btn_bar.pack(fill='x')
    # btn_bar.grid_columnconfigure(0, weight=1)
    # btn_bar.grid_columnconfigure(1, weight=1)
    back = RndBtn(btn_bar, 'Go Back', secondary, primary, accent)

    def func():
        for x in parent.winfo_children():
            x.destroy()
        MainPage(client, user)

    back.command = func
    back.pack(side=LEFT)
    option = StringVar(btn_bar)
    option.set('Select Session')
    session = GetSessions()
    sessions = [(session[key], session[key]['Start']) for key in session if session[key]['Group'] == group]
    dates = [x[1] for x in sessions]
    menu = OptionMenu(btn_bar, option, *dates)
    menu.config(fg=content, font=std_font)
    menu.config(bg=secondary)
    menu["highlightthickness"] = 0
    menu["borderwidth"] = 0
    menu['menu'].config(bg=secondary, fg=content, font=std_font)
    menu['menu'].config(bd=0)
    menu.pack(side=LEFT, padx=(100, 0))
    graph = RndBtn(btn_bar, 'Graph', secondary, primary, accent)
    download = RndBtn(btn_bar, 'Download', secondary, primary, accent)
    graph.pack(side=RIGHT, padx=(0, 50))
    download.pack(side=RIGHT, padx=(0, 50))

    def getDataframe():
        if option.get() != 'Select Session':
            current = sessions[dates.index(option.get())][0]
            start = StrToTime(current['Start'])
            end = StrToTime(current['End'])
            timestamps = db.child('Timestamps').get().val()
            data = []
            for key in timestamps:
                if timestamps[key]['Group'] == group and start < StrToTime(timestamps[key]['Time']) < end:
                    data.append(key)
            times = []
            while start < end:
                times.append(start + timedelta(seconds=5))
                start += timedelta(seconds=5)
            attendees = GetAttendeeList(group)
            dataframe = {}
            for attendee in attendees:
                dataframe[attendee] = [False for t in times]
            for key in data:
                for t in range(len(times) - 1):
                    if times[t] < StrToTime(timestamps[key]['Time']) < times[t + 1]:
                        if not dataframe[timestamps[key]['User']][t]:
                            dataframe[timestamps[key]['User']][t] = timestamps[key]['Present'] == 'True'
            df = pd.DataFrame(dataframe, index=times)
            # df = df.transpose()
            #print(df)
            return df

    def Download():
        df = getDataframe()
        folder_path = filedialog.asksaveasfilename(filetypes=[('Comma Separated values', '*.csv')])
        df.to_csv(folder_path+'.csv')
    download.command = Download
