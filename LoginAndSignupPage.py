from tkinter import *
from Palette import *
from CustomWidgets import round_rectangle, InputBar,RndBtn
from CustomAnimations import PackRightSlideAnimation, PackLeftSlideDownAnimation, ColorFade


def SignUpPage(client):
    signup_frame = Frame(client, bg=primary, bd=5)
    signup_frame.pack(side=RIGHT, padx=(0, 250))
    signup_heading = Label(signup_frame, text='Sign up.', font=('Uni Sans Thin CAPS', 25, 'normal'), fg=content,
                           bg=primary)
    signup_heading.grid(row=0, sticky='w')
    name = InputBar('Name', signup_frame, font=('Uni Sans-Trial Book', 20, 'normal'))
    name.grid(row=1, column=0, pady=30)
    u_name = InputBar('Username', signup_frame, font=('Uni Sans-Trial Book', 20, 'normal'))
    u_name.grid(row=2, column=0, pady=30)
    enter_password = InputBar('Enter Password', signup_frame, font=('Uni Sans-Trial Book', 20, 'normal'))
    enter_password.grid(row=3, column=0, pady=30)
    confirm_password = InputBar('Confirm Password', signup_frame, font=('Uni Sans-Trial Book', 20, 'normal'))
    confirm_password.grid(row=4, column=0, pady=30)
    create_acc = RndBtn(signup_frame,'Create Account','grey',primary,accent,'black','white',font=('Uni Sans Thin CAPS', 15, 'normal'))
    create_acc.grid(row=5, column=0, pady=15)
    log_in_text = Button(signup_frame, text='Have an account ? Log in', bg=primary, fg=content,
                         font=('Uni Sans-Trial', 15, 'normal'),
                         relief='flat', activebackground=primary, bd=0, cursor='hand2')
    log_in_text.grid(row=6, column=0, pady=15, sticky='w')

    def getLogIn():
        signup_frame.pack_forget()
        LoginPage(client)

    log_in_text.config(command=getLogIn)
    PackRightSlideAnimation(signup_frame)


def LoginPage(client, first=False):
    if first:
        left_stuff = TitleBlurb(client, True)
    login_frame = Frame(client, bg=primary, bd=5)
    login_frame.pack(side=RIGHT, padx=(0, 250))
    login_heading = Label(login_frame, text='Log in.', font=('Uni Sans Thin CAPS', 25, 'normal'), fg=content,
                          bg=primary)
    login_heading.grid(row=0, sticky='w')
    username = InputBar('Username', login_frame, font=('Uni Sans-Trial Book', 20, 'normal'))
    username.grid(row=1, column=0, pady=30)
    password = InputBar('Password', login_frame, font=('Uni Sans-Trial Book', 20, 'normal'))
    password.grid(row=2, column=0, pady=30)
    # lgn_btn = Button(login_frame, text='Login', bg='grey', fg='white', font=('Uni Sans Thin CAPS', 15, 'normal'),
    #                  padx=80, cursor='hand2',
    #                  activebackground=secondary, relief='flat', overrelief='flat', bd=0, activeforeground=content)
    lgn_btn = RndBtn(login_frame,'Login','grey',primary,accent,'black','white',font=('Uni Sans Thin CAPS', 15, 'normal'))
    lgn_btn.grid(row=3, column=0, pady=15)
    sign_up_text = Button(login_frame, text='Sign up here', bg=primary, fg=content,
                          font=('Uni Sans-Trial', 15, 'normal'),
                          relief='flat', activebackground=primary, bd=0, cursor='hand2')
    sign_up_text.grid(row=4, column=0, pady=15, sticky='w')

    def getSignUp():
        login_frame.pack_forget()
        SignUpPage(client)

    sign_up_text.config(command=getSignUp)
    PackRightSlideAnimation(login_frame)


def TitleBlurb(client, animate=False):
    title = Frame(client, bg=primary, bd=0)
    title.pack(padx=(150, 0), pady=(100, 0), side=LEFT)
    wz_label = Label(title, text='WizCroft.io', bg=primary, fg=content, padx=0, pady=5,
                     font=('Uni Sans Heavy CAPS', 80, 'normal'))
    wz_label.pack()
    info_label = Label(title, text='Automatic Attendance Management\nusing facial detection AI', bg=primary,
                       fg=content,
                       padx=15, pady=30,
                       font=('Uni Sans Thin CAPS', 20, 'normal'))
    info_label.pack()
    image = PhotoImage(file='Images/Logo.png')
    logo = Label(title, image=image, bd=0)
    logo.image = image
    logo.pack()
    canvas = Canvas(client, width=380, height=1000, bd=0, bg=primary, highlightthickness=0)
    divider = round_rectangle(canvas, 187, 100, 193, 900, radius=6, fill=primary, outline='')
    canvas.pack(side=LEFT)
    if animate:
        PackLeftSlideDownAnimation(title)
        ColorFade(canvas, divider)
    else:
        canvas.itemconfig(divider, fill=content)
    return title, canvas
