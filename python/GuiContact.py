from tkinter import *
import customtkinter as ctk
import psycopg2 as sk

myconnection = sk.connect(
    host='localhost', user='postgres', password='sathish6730', database='sat')
mycursor = myconnection.cursor()

ctk.set_appearance_mode('system')
app = ctk.CTk()
app.title('contact')
app.geometry('720x480');


name = StringVar()
mobile = IntVar()
email = StringVar()
del_name = StringVar()


def d_names():
    mycursor.execute('select name from contact')
    d_names = mycursor.fetchall()
    names = []
    for i in d_names:
        names += i
    return names


def contact():
    for widget in main_frame.winfo_children():
        widget.destroy()

    names = d_names()

    def show(name):
        for widget in details_frame.winfo_children():
            widget.destroy()

        mycursor.execute(
            'select * from contact where name=%s', ([name]))
        result = mycursor.fetchall()
        ctk.CTkLabel(details_frame, text=f'Name : {result[0][0]}\nMobile : {result[0][1]}\nEmail : {result[0][2]}').grid(
            padx=10, pady=10)

    canvas = Canvas(main_frame, bg='black')
    canvas.pack(side=LEFT)
    canvas.pack_propagate(False)
    canvas.configure(width=200, height=2080)

    scrollbar = Scrollbar(canvas, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side='right', fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    details = Frame(canvas, bg='black')
    canvas.create_window((0, 0), window=details, anchor='nw')

    details_frame = Frame(main_frame, bg='black')
    details_frame.pack(side=RIGHT, fill=BOTH, expand=True, pady=10)

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox('all'))

    details.bind('<Configure>', on_frame_configure)

    if len(names) > 0:
        for i in names:
            ctk.CTkButton(
                details, text=f'{i}', command=lambda name=i: show(name)).pack(pady=3)
    else:
        ctk.CTkLabel(details, text='No contact found',
                     text_color='red').grid(padx=10, pady=10)


def create():
    for widget in main_frame.winfo_children():
        widget.destroy()

    def sumbit():
        names = d_names()
        if name.get() not in names:
            mycursor.execute('insert into contact values(%s,%s,%s)',
                             (name.get(), mobile.get(), email.get()))
            myconnection.commit()
            ctk.CTkLabel(create, text='Contact created successfully!',
                         text_color='green').grid(row=4, column=2, pady=10)
        else:
            ctk.CTkLabel(create, text=f'"{name.get()}" Mobile number already exist',
                         text_color='red').grid(row=4, column=2, pady=10)

    create = Frame(main_frame, bg='lightblue')
    create.pack(fill=BOTH, expand=True)
    Label(create, text='Enter your name', bg='lightblue').grid(
        row=0, column=1, pady=10)
    Label(create, text='Enter your mobile number',
          bg='lightblue').grid(row=1, column=1, pady=10)
    Label(create, text='Enter your email',
          bg='lightblue').grid(row=2, column=1, pady=10)
    Entry(create, textvariable=name).grid(row=0, column=2, pady=10)
    Entry(create, textvariable=mobile).grid(row=1, column=2, pady=10)
    Entry(create, textvariable=email).grid(row=2, column=2, pady=10)
    ctk.CTkButton(create, text='submit', command=sumbit).grid(
        row=3, column=2, pady=10)


def delete():
    for widget in main_frame.winfo_children():
        widget.destroy()

    def remove():
        names = d_names()

        if del_name.get() in names:
            mycursor.execute(
                'delete from contact where name=%s', (del_name.get(),))
            myconnection.commit()
            ctk.CTkLabel(delete, text='Contact deleted successfully!',
                         text_color='green').grid(row=4, column=2, pady=10)
        else:
            ctk.CTkLabel(delete, text="contact doesn't exist!",
                         text_color='red').grid(row=4, column=2, pady=10)

    delete = Frame(main_frame, bg='lightblue')
    delete.pack(fill=BOTH, expand=True)
    Label(delete, text='Enter name', bg='lightblue').grid(
        row=0, column=0, padx=10, pady=10)
    Entry(delete, textvariable=del_name).grid(
        row=0, column=1, padx=10, pady=10)
    ctk.CTkButton(delete, text='Delete', command=remove).grid(
        row=1, column=1, pady=10)


option_frame = Frame(app, bg='black')
option_frame.pack(side=LEFT)
option_frame.pack_propagate(False)
option_frame.configure(width=200, height=1080)

main_frame = Frame(app, bg='black')
main_frame.pack()
main_frame.pack_propagate(False)
main_frame.configure(width=2080, height=2080)

ctk.CTkButton(option_frame, text='Contact', command=contact).pack(pady=3)
ctk.CTkButton(option_frame, text='Create', command=create).pack(pady=3)
ctk.CTkButton(option_frame, text='Delete', command=delete).pack(pady=3)

app.mainloop()
