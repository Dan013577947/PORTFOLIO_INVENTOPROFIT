import subprocess
# Install pip
subprocess.check_call(['python', '-m', 'ensurepip'])
# Upgrade pip
subprocess.check_call(['python', '-m', 'pip', 'install', '--upgrade', 'pip'])
from tkinter import *
import tkinter.messagebox
import os
import time
import datetime
import shutil

mods = ['pyzbar','opencv-python','matplotlib','pyqrcode','pypng','pywin32','pillow']
mods_error = ['pyzbar','cv2','matplotlib','pyqrcode','png','win32api','PIL']
imp = ["from pyzbar.pyzbar import decode","import cv2","import matplotlib.pyplot as plt","from pyqrcode import QRCode","import png","import win32api","from PIL import Image,ImageTk"]

for i in range(7):
    try:
        exec(imp[i])
    except Exception as e:
        print(e,"execute")
        e = str(e) 
        if e == f"No module named '{mods_error[i]}'":
            package_name = mods[i]
            subprocess.call(['pip', 'install', package_name])    
for i in range(7):
    try:
        exec(imp[i])
    except Exception as e:
        print(e,"execute")
        e = str(e) 
        if e == f"No module named '{mods_error[i]}'":
            package_name = mods[i]
            subprocess.call(['pip', 'install', package_name])

import pyqrcode

root= Tk()

root.title("InventoProfit")
root.geometry("900x600")
root.resizable(False,False)
frame = Frame(root)
frame.pack(expand=True, fill="both")

d,cap,detector,current_time,months_lists= {},cv2.VideoCapture(0),cv2.QRCodeDetector(),datetime.datetime.now(),["January","February","March","April","May","June","July","August","September","October","November","December"]

def folder_create():
    folder_path = ["./QR_CODES","./texts","./ARCHIVED_ITEMS"]
    for i in range(len(folder_path)):
        if not os.path.exists(folder_path[i]):
            os.mkdir(folder_path[i])
            print(f"{folder_path[i]} created successfully")
        else:
            print(f"{folder_path[i]} already exists")   
folder_create()
def text_create():
    file_name = ["items_name_price_stock.txt","items_preferences.txt", "weekly_expense_list.txt","accounts_lists.txt","items_archive.txt","monthly_expense_list.txt"]
    for i in range(6):
        try:
            file = open(f"./texts/{file_name[i]}",'r')
            file.readlines()
            file.close()
            print(f"{file_name[i]} already exist")
        except Exception as e:
            
            handler = f"[Errno 2] No such file or directory: './texts/{file_name[i]}'"
            e = str(e)
            if handler == e:
                file = open(f"./texts/{file_name[i]}",'w')
                file.write("")
                file.close()
                print(f"{file_name[i]} created succesfully")
text_create()
def file_opener():
    global fields,date,item_name,unit,quantity,critical_value,orig_price,mark_up,selling_price,lines
    fields,date,item_name,unit,quantity,critical_value,orig_price,mark_up,selling_price= [],[],[],[],[],[],[],[],[]
    file = open("./texts/items_name_price_stock.txt", 'r')
    lines = file.readlines()
    file.close()
    for x in lines:
        fields = x.split(",")
        date.append(fields[0])
        item_name.append(fields[1])
        unit.append(fields[2])
        quantity.append(int(fields[3]))
        critical_value.append(float(fields[4]))
        orig_price.append(float(fields[5]))
        mark_up.append(float(fields[6]))
        selling_price.append(float(fields[7]))
    return item_name

def file_opener_archive():
    global fromMainMenu,fields,date_archive_text,item_name_archive_text,unit_archive_text,quantity_archive_text,critical_value_archive_text,orig_price_archive_text,mark_up_archive_text,selling_price_archive_text,lines
    fromMainMenu = False
    fields,date_archive_text,item_name_archive_text,unit_archive_text,quantity_archive_text,critical_value_archive_text,orig_price_archive_text,mark_up_archive_text,selling_price_archive_text= [],[],[],[],[],[],[],[],[]
    file = open("./texts/items_archive.txt", 'r')
    lines = file.readlines()
    file.close()
    for x in lines:
        fields = x.split(",")
        date_archive_text.append(fields[0])
        item_name_archive_text.append(fields[1])
        unit_archive_text.append(fields[2])
        quantity_archive_text.append(int(fields[3]))
        critical_value_archive_text.append(float(fields[4]))
        orig_price_archive_text.append(float(fields[5]))
        mark_up_archive_text.append(float(fields[6]))
        selling_price_archive_text.append(float(fields[7]))  
    return item_name_archive_text
item_name,fromMainMenu,quantity_restock,fromArchive = file_opener(),False,[],False

def clear():
    for widgets in frame.winfo_children():
        widgets.destroy()
def clear_win():
    global frame_win
    for widgets in frame_win.winfo_children():
        widgets.destroy()
def month_determine(current_time):
    global month,months_lists
    month_num = current_time.month
    month=""
    for i in range(12): 
        if month_num == i+1:
            month = months_lists[i]
    return month
month = month_determine(current_time)    
#this function updates the current time     
def update_time(time_label):
    current_time = time.strftime('%I:%M:%S %p')
    time_label.config(text=current_time)
    time_label.after(1000, lambda: update_time(time_label)) # update time every second
#this function updates the current time  
def update_date(date_label):
    current_date = datetime.datetime.now().strftime("%m-%d-%Y")
    date_label.configure(text = f"Date: {current_date}",)
    date_label.after(10,lambda: update_date(date_label))
def sign_up_widgets():
    global user_name_text,password_text,fromCreate,fromMenu,fromForgot,password_q
    fromCreate,fromMenu,fromForgot = False,False,True
    clear()
    root.geometry("500x300")
    Label(frame, text = "RETRIEVE ACCOUNT: ", font = ("Arial", 15, 'bold')).pack(pady=10)
    Label(frame, text = "USER NAME: ", font = ("Arial", 10, 'bold')).place(x = 10, y = 100)
    Label(frame, text = "NEW\nPASSWORD: ", font = ("Arial", 10, 'bold'),justify = "left").place(x = 10, y = 150)
    user_name_text = Text(frame, width = 40, height = 1)
    password_text = Entry(frame,width=53,show = "*")
    password = ""
    def user_name_def():
        if user_name_text.get("1.0", "end-1c") == "Username" or user_name_text.get("1.0", "end-1c") == "":
            user_name_text.delete("1.0", "end-1c") 
            user_name_text.insert(END, "Username")
            user_name_text.config(fg='grey')
        def on_entry_click(event):
            global password_q
            if user_name_text.get("1.0", "end-1c") == "Username": 
                user_name_text.delete("1.0", "end-1c")  
                user_name_text.config(fg='black')
                password_def()
            elif user_name_text.get("1.0", "end-1c") != "Username" or user_name_text.get("1.0", "end-1c") != "":
                password_text = Entry(frame,width=53,show = "*")
                password_q = password_text.get()
                try:
                    password_text.delete(0,END)        
                    if password_text.get() == "Password" or password_text.get() == "":
                        password_text.insert(END, "Password")
                        password_text.config(fg='grey',show = "Password")
                    else:
                        password_text.insert(END, f"{password_q}")
                        password_text.config(fg='black')
                except:
                    pass 
        user_name_text.bind('<FocusIn>', on_entry_click) 
    def password_def():
        if password_text.get() == "Password" or password_text.get() == "" :
            password_text.delete(0,END)  
            password_text.insert(END, "Password")
            password_text.config(fg='grey')
        def on_entry_click1(event):
            if password_text.get() == "Password":
               password_text.delete(0,END)  
               password_text.config(fg='black')
               user_name_def()
            elif password_text.get() != "Password" or password_text.get() != "":
                user_name_text = Text(frame, width = 40, height = 1)
                user_name_text = user_name_text.get("1.0", "end-1c")
                try:
                    user_name_text.delete("1.0", "end-1c")
                    if user_name_text.get("1.0", "end-1c") == "Username" or user_name_text.get("1.0", "end-1c") == "":
                        user_name_text.insert(END, "Username")
                        user_name_text.config(fg='grey')
                    else:
                        user_name_text.insert(END, f"{user_name_text}")
                        user_name_text.config(fg='black')
                except:
                    pass
        password_text.bind('<FocusIn>', on_entry_click1)
    user_name_def()
    password_def()
    user_name_text.place(x = 100, y = 100)
    password_text.place(x = 100, y = 150)
    Button(frame, text = "SIGN UP", font = ("Arial", 12, 'bold'), command = opening_forgot, bd = 3).place(x = 200, y = 200)
    Button(frame, text = "CANCEL", font = ("Arial", 10, 'bold'), command = opening_menu, bd = 3).place(x = 400, y = 250)
    def handle_keypress(event):
        if event.keysym == "Return":
            return "break"  # Prevents the default behavior of the Enter key
        else:
            # Perform any other desired actions
            pass
    user_name_text.bind("<KeyPress>", handle_keypress)
    password_text.bind("<KeyPress>", handle_keypress)
    def on_enter_press(event):
        opening_forgot()
    user_name_text.bind("<Return>", on_enter_press)
    password_text.bind("<Return>", on_enter_press) 
def label_clicked(event):
    global window
    if window == "Forgot Password":
        sign_up_widgets()
    elif window == "\u2190,sales":
        menu_widgets("")
    elif window == "LOG OUT,menu":
        opening_menu()
    elif window == "\u2190,daily_report":
        sales()
   
def label_enter(event):
    global window
    if window == "Forgot Password":
        label.config(font=("Arial", 14,"underline"))
    elif window == "\u2190,sales":
        label_sales.config(font=("Arial", 25,"underline"))
    elif window == "LOG OUT,menu":
        label_menu_widgets.config(font=("Arial", 13,"underline"), fg = 'red')
    elif window == "\u2190,daily_report":
        label_sales.config(font=("Arial", 25,"underline"))
def label_leave(event):
    global window
    if window == "Forgot Password":
        label.config(font=("Arial", 14))
    elif window == "\u2190,sales":
        label_sales.config(font=("Arial", 25))
    elif window == "LOG OUT,menu":
        label_menu_widgets.config(font=("Arial", 13), fg = 'blue')
    elif window == "\u2190,daily_report":
        label_sales.config(font=("Arial", 25))
#this function displays widgets in the window
isDone,fromMenu,fromCreate = False,False,False
password_q = ""
def opening_menu_widgets():
    global password_text,user_name_text,label,fromMenu,fromCreate,fromForgot,password_q    
    fromForgot,fromMenu,fromCreate=False,True,False
    clear()
    Label(frame, text = "INVENTOPROFIT", font = ("Arial", 20, 'bold')).pack(pady=15)
    Label(frame, text = "INVENTORY AND SALES FOR RAMIRES SUPPLIES STORE", font = ("Arial", 15, 'bold')).pack()  
    Label(frame, text = "USER NAME: ", font = ("Arial", 10, 'bold')).place(x = 200, y = 200)
    Label(frame, text = "PASSWORD: ", font = ("Arial", 10, 'bold')).place(x = 200, y = 250)  
    user_name_text = Text(frame, width = 40, height = 1)
    password_text = Entry(frame,width=53,show = "*")
    def user_name_def():  
        if user_name_text.get("1.0", "end-1c") == "Username" or user_name_text.get("1.0", "end-1c") == "":
            user_name_text.delete("1.0", "end-1c") 
            user_name_text.insert(END, "Username")
            user_name_text.config(fg='grey')
        user_name_text.place(x = 300, y = 200)
        def on_entry_click(event):      
            if user_name_text.get("1.0", "end-1c") == "Username": 
                user_name_text.delete("1.0", "end-1c")  
                user_name_text.config(fg='black')
                password_def()
            elif user_name_text.get("1.0", "end-1c") != "Username" or user_name_text.get("1.0", "end-1c") != "":
                password_text = Entry(frame,width=53,show = "*")
                password = password_text.get()
                try:
                    password_text.delete(0,END) 
                    if password_text.get() == "Password" or password_text.get() == "":
                        password_text.insert(END, "Password")
                        password_text.config(fg='grey')
                    else:
                        password_text.insert(END, f"{password}")
                        password_text.config(fg='black') 
                except:
                    pass 
        user_name_text.bind('<FocusIn>', on_entry_click)   
    def password_def():
        if password_text.get() == "Password" or password_text.get() == "" :
            password_text.delete(0,END)  
            password_text.insert(END, "Password")
            password_text.config(fg='grey')
        password_text.place(x = 300, y = 250)
        def on_entry_click1(event):
            if password_text.get() == "Password":
               password_text.delete(0,END)  
               password_text.config(fg='black')
               user_name_def()
            elif password_text.get() != "Password" or password_text.get() != "":
                user_name_text = Text(frame, width = 40, height = 1)
                user_name_text = user_name_text.get("1.0", "end-1c") 
                try:
                    user_name_text.delete("1.0", "end-1c")
                    if user_name_text.get("1.0", "end-1c") == "Username" or user_name_text.get("1.0", "end-1c") == "":
                        user_name_text.insert(END, "Username")
                        user_name_text.config(fg='grey')
                    else:
                        user_name_text.insert(END, f"{user_name_text}")
                        user_name_text.config(fg='black')   
                except:
                    pass
        password_text.bind('<FocusIn>', on_entry_click1)
    user_name_def()
    password_def()
    def on_enter_press(event):
        handle_texts(fromCreate)
    user_name_text.bind("<Return>", on_enter_press)
    password_text.bind("<Return>", on_enter_press)
    sign_in_but = Button(frame, text = "SIGN IN", font = ("Arial", 12, 'bold'), command = lambda:handle_texts(fromCreate), bd = 3)
    sign_in_but.place(x = 300, y = 300)   
    Button(frame, text = "CREATE NEW ACCOUNT", font = ("Arial", 12, 'bold'), command = create_new_account, bd = 3).place(x = 330, y = 500)
    label = Label(frame, text="Forgot Password", font=("Arial", 14), fg="blue")
    label.place(x = 470,y=310)
    # Use the bind method to bind the click event to the label
    global window
    window = "Forgot Password"
    label.bind("<Button-1>", label_clicked)
    label.bind("<Enter>", label_enter)
    label.bind("<Leave>", label_leave)
    date_label = Label(frame, font = ("Arial", 10))
    date_label.place(x = 10, y=520)
    time_label = Label(frame, font = ("Arial", 10))
    time_label.place(x = 10, y=540)
    update_date(date_label)
    update_time(time_label)
    def handle_keypress(event):
        if event.keysym == "Return":
            return "break"  # Prevents the default behavior of the Enter key
        else:
            # Perform any other desired actions
            pass
    user_name_text.bind("<KeyPress>", handle_keypress)
    password_text.bind("<KeyPress>", handle_keypress)
def handle_texts(fromCreate):
    global user_name,password,isDone,fromMenu,fromForgot,current_user,current_user_name,role
    user_name = user_name_text.get(1.0, "end-1c")
    password = password_text.get()
    file = open("./texts/accounts_lists.txt",'r')
    lines = file.readlines()
    file.close()
    name,password1,role,fields = [],[],[],[]
    
    for x in lines:
        fields = x.split(",")
        name.append(fields[0])
        password1.append(fields[1])
        role.append(fields[2].replace("\n",""))
    
    User,Pass = False,False
    if (user_name == "Username" and password == "Password") or(user_name == "" and password == "Password") or (user_name == "Username" and password == "" ) or (user_name == "" and password == ""):
        tkinter.messagebox.showinfo("NOTICE","Empty Username and Password!")
        isDone = False
    elif (user_name == "Username" and password != "Password") or(user_name == "" and password != "Password") :
        isDone = False
        tkinter.messagebox.showinfo("NOTICE","Empty Username!")
    elif (user_name != "Username" and password == "Password") or(user_name != "Username" and password == ""):
        isDone = False
        tkinter.messagebox.showinfo("NOTICE","Empty Password!")
    else:  
        if fromMenu == True:
            if user_name in name:
                for i in range(len(name)):
                    if user_name == name[i] and password == password1[i]:
                        isDone,current_user,current_user_name = True,role[i],name[i]           
            else:
                isDone = False 
            for i in range(len(name)):
                if user_name == name[i] and password != password1[i]:
                    User,Pass = True,False
                elif user_name != name[i] and password == password1[i]:
                    User,Pass = False,True
            if isDone==False and User == False and Pass == True :
                tkinter.messagebox.showinfo("NOTICE", "Username Doesn't Exist")
                clear()
                opening_menu()
            elif User == True and Pass == False:
                tkinter.messagebox.showinfo("NOTICE", "Wrong Password")
                clear()
                opening_menu()
            elif isDone==False and User == False and Pass == False:
                tkinter.messagebox.showinfo("NOTICE", "Account Doesn't Exist")
                clear()
                opening_menu()
            else:
                fromMenu,isDone = False,True
                menu()
        elif fromCreate == True:
            if user_name in name or (user_name in name and password not in password1):
                
                tkinter.messagebox.showinfo("NOTICE", "Username Already Exist")
                create_new_account()
            else:
                isDone,fromCreate = True,False
                admin_assistant()          
        elif fromForgot == True:
            print(user_name,password)
            print(name,password1)
            isDone = False
            for i in range(len(name)):
                if user_name == name[i] and password != password1[i]:
                    isDone = True
               
            if isDone == True:
                file = open("./texts/accounts_lists.txt","r")
                lines = file.readlines()
                file.close()
                name,password1,role1,fields = [],[],[],[]
                for x in lines:
                    fields = x.split(",")
                    name.append(fields[0])
                    password1.append(fields[1])
                    role1.append(fields[2].replace("\n",""))
                file = open("./texts/accounts_lists.txt","w")
                file.write("")
                file.close()
                for i in range(len(name)):
                    if user_name == name[i]:
                        name[i],password1[i] = user_name,password
                    file = open("./texts/accounts_lists.txt","a")
                    file.write(f"{name[i]},{password1[i]},{role1[i]}\n")
                    file.close()
                opening_menu()   
            else:
                isDone,fromForgot,alreadyPass = False,False,False
                for i in range(len(name)):
                    if user_name == name[i] and password == password1[i]:
                        alreadyPass = True
                if alreadyPass == True:
                    tkinter.messagebox.showinfo("NOTICE","This is Already Your Password")
                else: 
                    tkinter.messagebox.showinfo("NOTICE","Username Doesn't Exist")
                sign_up_widgets()        
        else: 
            opening_menu()
            
def create_new_account():
    global user_name_text,password_text,isDone,fromMenu,fromCreate,fromForgot,isDone
    clear()
    isDone,fromMenu,fromCreate,fromForgot = False,False,True,False
    root.geometry("500x300")
    Label(frame, text = "CREATE ACCOUNT: ", font = ("Arial", 15, 'bold')).pack(pady=10)
    Label(frame, text = "USER NAME: ", font = ("Arial", 10, 'bold')).place(x = 10, y = 100)
    Label(frame, text = "NEW\nPASSWORD: ", font = ("Arial", 10, 'bold'),justify = "left").place(x = 10, y = 150)
    user_name_text = Text(frame, width = 40, height = 1)   
    password_text = Entry(frame,width=53,show = "*")
    def user_name_def():
        if user_name_text.get("1.0", "end-1c") == "Username" or user_name_text.get("1.0", "end-1c") == "":
            user_name_text.delete("1.0", "end-1c") 
            user_name_text.insert(END, "Username")
            user_name_text.config(fg='grey')   
        def on_entry_click(event):  
            if user_name_text.get("1.0", "end-1c") == "Username": 
                user_name_text.delete("1.0", "end-1c")  
                user_name_text.config(fg='black')
                password_def()
            elif user_name_text.get("1.0", "end-1c") != "Username" or user_name_text.get("1.0", "end-1c") != "":
                password_text = Entry(frame,width=53,show = "*")
                password = password_text.get()
                try:
                    password_text.delete(0,END)   
                    if password_text.get() == "Password" or password_text.get() == "":
                        password_text.insert(END, "Password")
                        password_text.config(fg='grey')
                    else:
                        password_text.insert(END, f"{password}")
                        password_text.config(fg='black')
                except:
                    pass 
        user_name_text.bind('<FocusIn>', on_entry_click)        
    def password_def():
        if password_text.get() == "Password" or password_text.get() == "" :
            password_text.delete(0,END)  
            password_text.insert(END, "Password")
            password_text.config(fg='grey')
        def on_entry_click1(event):
            if password_text.get() == "Password":
               password_text.delete(0,END)  
               password_text.config(fg='black')
               user_name_def()
            elif password_text.get() != "Password" or password_text.get() != "":
                user_name_text = Text(frame, width = 40, height = 1)
                user_name_text = user_name_text.get("1.0", "end-1c") 
                try:
                    user_name_text.delete("1.0", "end-1c") 
                    if user_name_text.get("1.0", "end-1c") == "Username" or user_name_text.get("1.0", "end-1c") == "":
                        user_name_text.insert(END, "Username")
                        user_name_text.config(fg='grey')
                    else:
                        user_name_text.insert(END, f"{user_name_text}")
                        user_name_text.config(fg='black')
                except:
                    pass
        password_text.bind('<FocusIn>', on_entry_click1)
    user_name_def()
    password_def()
    user_name_text.place(x = 100, y = 100)
    password_text.place(x = 100, y = 150)
    Button(frame, text = "SIGN UP", font = ("Arial", 12, 'bold'), command = lambda: handle_texts(fromCreate), bd = 3).place(x = 200, y = 200)
    Button(frame, text = "CANCEL", font = ("Arial", 10, 'bold'), command = opening_menu, bd = 3).place(x = 400, y = 250)
    def handle_keypress(event):
        if event.keysym == "Return":
            return "break"  # Prevents the default behavior of the Enter key
        else:
            # Perform any other desired actions
            pass

    user_name_text.bind("<KeyPress>", handle_keypress)
    password_text.bind("<KeyPress>", handle_keypress)
    def on_enter_press(event):
        handle_texts(fromCreate)
    user_name_text.bind("<Return>", on_enter_press)
    password_text.bind("<Return>", on_enter_press)
fromForgot = False
def admin_assistant():
    clear()
    root.geometry("400x200")
    def adm():
        file = open("./texts/accounts_lists.txt","r")
        lines = file.readlines()
        file.close()
        user_role,fields = [],[]
        for x in lines:
            fields = x.split(",")
            user_role.append(fields[2].replace("\n",""))
        len_user_role = 0
        for x in user_role:
            if x == "admin":
                len_user_role+=1
        if len_user_role<2:
            role = admin_but.cget("text").lower()
            file = open("./texts/accounts_lists.txt","a")
            file.write(f"{user_name},{password},{role}\n")
            file.close()
            opening_menu()
        else:
            tkinter.messagebox.showinfo("NOTICE","Only 2 ADMINS are allowed")
            admin_assistant()
    def assis():
        role = assistant_but.cget("text").lower()
        file = open("./texts/accounts_lists.txt","a")
        file.write(f"{user_name},{password},{role}\n")
        file.close()
        opening_menu()
    Label(frame, text = "Choose A Role",font = ("Arial", 20, 'bold'), bd = 3).pack(pady = 7)
    admin_but = Button(frame, text = "Admin",font = ("Arial", 15), bd = 3,command = lambda :adm())
    admin_but.pack(pady = 7)
    assistant_but = Button(frame, text = "Cashier",font = ("Arial", 15), bd = 3,command = lambda :assis())
    assistant_but.pack(pady = 7)

def opening_forgot():
    global fromCreate,fromMenu,fromForgot,password_q
    fromCreate,fromMenu,fromForgot = False,False,True
    handle_texts("")
    if isDone == True:
        clear()
        opening_menu()
    else:
        pass
def reseter():
    global d,item_name
    item_name = file_opener()
    for i in range(len(item_name)):    
        d[item_name[i]] = 0
def update_final_item_amount_():
    global final_item_amount_
    final_item_amount_ = []
    for i in range(len(item_name)):
        final_item_amount_.append(0)
final_item_amount_ = []     
update_final_item_amount_()
def adder_multi(data,a,amount,window):
    global months_lists,final_item_amount_,d,date,item_name,unit,quantity,critical_value,orig_price,mark_up,selling_price,item_amount_
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    second = datetime.datetime.now().second
    month = datetime.datetime.now().month
    for i in range(12):
        if  month == i+1:
            month = months_lists[i]
    day = datetime.datetime.now().day
    year = datetime.datetime.now().year
    reseter()
    item_name = file_opener()
    file = open("./texts/items_name_price_stock.txt", 'w')
    file.write("")
    file.close()
    final_amount = []
    for i in range(len(item_name)):
        final_amount.append(0)
    for i in range(len(item_name)):
        final_amount[i] = int(quantity[i])-amount[i]
        if a == item_name[i]:
            d[item_name[i]]+= amount[i]        
        file = open("./texts/items_name_price_stock.txt", 'a')
        file.write(f"{date[i]},{item_name[i]},{unit[i]},{final_amount[i]},{critical_value[i]},{orig_price[i]},{mark_up[i]},{selling_price[i]}\n")
        file.close()
    date = f"{month}:{day}:{year}"
    time = f"{hour}:{minute}:{second}"
    for i in range(len(item_name)):  
        item_amount_[i] = d[item_name[i]]
    if window == "sales" or window == "menu_widgets":
        update_final_item_amount_()
    else:
        pass
    update_final_item_amount_()
    for i in range(len(item_name)):
        final_item_amount_[i]+=item_amount_[i]    
    for i in range(len(item_name)):
        if data == item_name[i]:
            file = open("./texts/items_preferences.txt", 'a')
            file.write(f"{item_name[i]},{item_amount_[i]},{date},{time}\n")
            file.close()
    clear()
    if window == "menu_widgets":
        
        menu_widgets("")
    elif window == "product_inventory":
        product_inventory()
    elif window == "sales":
        item_sales_monthly,sales_ = [],0
        for i in range(len(item_name)):
            sales_ = final_item_amount_[i]*selling_price[i]
            item_sales_monthly.append("%.2f"%sales_)
        
        for i in range(len(item_name)):
            if item_sales_monthly[i] != "%.2f"%0:
                file = open("./texts/items_sales_per_month.txt", 'a')
                file.write(f"{item_name[i]},{item_sales_monthly[i]},{month}\n")
                file.close()
        
        sales()
fromScan,amount = False,0
def scan_widget(window):
    global data,win,frame_win,amount,a
    item_name = file_opener()
    item_name_archive = file_opener_archive()
    
    if data:
        if data in item_name:   
            for i in range(len(item_name)):
                if item_name[i] == data:
                    if int(quantity[i]) > 0:
                        cv2.destroyAllWindows()
                        win = Tk()
                        win.title('InventoProfit')
                        win.geometry("500x120")
                        win.attributes('-topmost', True)
                        win.resizable(False,False)
                        frame_win = Frame(win)
                        frame_win.pack(fill = BOTH,expand = True)     
                        label = Label(frame_win, text = f"Quantity of {data}", font = ("Arial", 20))
                        label.pack()  
                        text = Text(frame_win, width = 20, height = 1)
                        text.pack(pady = 5)
                        def on_enter_press(event):
                            gets_amount()
                        text.bind("<Return>", on_enter_press)
                        def gets_amount():
                            global data,quantity,item_name,item_amount_
                            item_amount_ = []
                            for i in range(len(item_name)):
                                item_amount_.append(0)
                            try:
                                amount = text.get(1.0, "end-1c")
                            except:
                                print(e,"multi_scan")
                                amount = amount
                            try:
                                amount = int(amount)
                                for i in range(len(item_name)):
                                    if data == item_name[i]:                             
                                        item_amount_[i] =  int(amount)
                                        
                                        if item_amount_[i] > int(quantity[i]):
                                            tkinter.messagebox.showinfo("ERROR",  "Stocks Are Not Enough!")     
                                        else:
                                            win.destroy()
                                            adder_multi(data, a, item_amount_,window)                  
                            except Exception as e:
                                print(e,"multi_scan1111")
                                e = str(e)
                                if "invalid literal for int() with base 10: ''" == e:
                                    tkinter.messagebox.showinfo("ERROR",  "Empty Input!")
                                    win.destroy()
                                    scan_widget(window)
                                elif f"invalid literal for int() with base 10: '{text.get(1.0, 'end-1c')}'" == e:
                                    tkinter.messagebox.showinfo("ERROR",  "Input Must Be Integer!")
                                    win.destroy()
                                    scan_widget(window)         
                        but_done = Button(frame_win, text = "Done",bd = 3, font = ("Arial",15), command= gets_amount)
                        but_done.pack()
                        win.mainloop()
                    else:
                        tkinter.messagebox.showinfo("ERROR",  "Stock Has Reached Its LIMIT !")         
        else:
            if data in item_name_archive:
                tkinter.messagebox.showinfo("ERROR", "ITEM IS IN ARCHIVE")
            else:
                tkinter.messagebox.showinfo("ERROR", "QR CODE DOES NOT EXIST! ")
    def handle_keypress(event):
        if event.keysym == "Return":
            return "break"  # Prevents the default behavior of the Enter key
        else:
            # Perform any other desired actions
            pass
    text.bind("<KeyPress>", handle_keypress)
def multi_scan(window):
    global win,frame_win,d,item_name,quantity,data,fromScan,a
    fromScan = True
    item_name = file_opener()
    cv2.namedWindow('qrcodescanner app: press q to close', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('qrcodescanner app: press q to close',cv2.WND_PROP_TOPMOST,cv2.WINDOW_FULLSCREEN)
    while True:
        _,img = cap.read()
        data, one,  _= detector.detectAndDecode(img)
        if data:
            a = data
            break
        cv2.imshow('qrcodescanner app: press q to close', img)
        if (cv2.waitKey(1) == ord('q')) or (cv2.waitKey(1) == ord('Q')):
            cv2.destroyAllWindows()
            break
    scan_widget(window)   

months_lists = ["January","February","March","April","May","June","July","August","September","October","November","December"]

total_sales_daily = []

def choose_day():
    global win, frame_win, months_lists,names3,my_listbox3,my_listbox2, names2,months_lists,selected_month
    try:
        selected_choose_day = my_listbox2.curselection()
        my_listbox2 = my_listbox2
    
        selected_choose_day = str(selected_choose_day).replace(",)","").replace("(","")
    except:
        selected_choose_day = selected_choose_day
    d = {}
    for i in range(len(months_lists)):
        d[i] = months_lists[i]
    selected_month = d[int(selected_choose_day)]

    
    pass
    clear_win()
    win.geometry("350x120")
    canvas = Canvas(frame_win)
    
    label = Label(frame_win, text = "Choose The Day", font = ("Arial", 20))
    label.pack()
    label1 = Label(frame_win,text = "Choose a Day...", bg = "white",font = ("Courier", 10)).pack(pady=5)
    def toggle_size():
        global is_large
        if not is_large:
            win.geometry("350x400")
            is_large = True
        else:
            win.geometry("350x120")
            is_large = False      
    button = Button(frame_win, text="...", font = 'bold', height = 1,relief = SUNKEN,command=toggle_size)
    button.place(x = 250,y = 42)
    but_done = Button(frame_win, text = "Done",bd = 3, font = ("Arial",15), command = choose_year)
    but_done.pack()
    canvas.pack(side = BOTTOM,expand = 1)
    scrollbar = Scrollbar(canvas)
    scrollbar.pack(side=RIGHT, fill=Y)
    my_listbox3 = Listbox(canvas,yscrollcommand=scrollbar.set, width = 200,height = 400,font = ("Arial",20),selectmode = SINGLE)
    names3 = []
    if selected_month == "April" or selected_month == "June" or selected_month == "September" or selected_month == "November":
        days_count = 30
        for i in range(days_count):
            names3.append(i+1)
            my_listbox3.insert(END, f"{i+1}")
        my_listbox3.pack(side=LEFT)
        scrollbar.config(command=my_listbox3.yview)
        
    elif selected_month == "February":
        days_count = 29
        for i in range(days_count):
            names3.append(i+1)
            my_listbox3.insert(END, f"{i+1}")
        my_listbox3.pack(side=LEFT)
        scrollbar.config(command=my_listbox3.yview)
    else:
        days_count = 31
        for i in range(days_count):
            names3.append(i+1)
            my_listbox3.insert(END, f"{i+1}")
        my_listbox3.pack(side=LEFT)
        scrollbar.config(command=my_listbox3.yview)
    
def choose_year_weekly():
    global win, all_year,frame_win, months_lists,names5,my_listbox5,my_listbox4, names4,selected_month_weekly,selected_week,dic
    global fromChooseYearWeekly
    fromChooseYearWeekly = True
    try:
        selected_choose_year_weekly = my_listbox4.curselection()
        my_listbox4 = my_listbox4
    
        selected_choose_year_weekly = str(selected_choose_year_weekly).replace(",)","").replace("(","")
    except:
        selected_choose_year_weekly = selected_choose_year_weekly
    d = {}
  
    for i in range(len(week_1_5)):
        d[i] = week_1_5[i]
    selected_week = d[int(selected_choose_year_weekly)]
    dic = {}
    if selected_month_weekly == "April" or selected_month_weekly == "June" or selected_month_weekly == "September" or selected_month_weekly == "November":
        if selected_week == week_1_5[0]:
            dic[selected_week] = [1,2,3,4,5,6,7]
        elif selected_week == week_1_5[1]:
            dic[selected_week] = [8,9,10,11,12,13,14]
        elif selected_week == week_1_5[2]:
            dic[selected_week] = [15,16,17,18,19,20,21]
        elif selected_week == week_1_5[3]:
            dic[selected_week] = [22,23,24,25,26,27,28]
        elif selected_week == week_1_5[4]:
            dic[selected_week] = [29,30]
    elif selected_month_weekly == "February":
        if selected_week == week_1_5[0]:
            dic[selected_week] = [1,2,3,4,5,6,7]
        elif selected_week == week_1_5[1]:
            dic[selected_week] = [8,9,10,11,12,13,14]
        elif selected_week == week_1_5[2]:
            dic[selected_week] = [15,16,17,18,19,20,21]
        elif selected_week == week_1_5[3]:
            dic[selected_week] = [22,23,24,25,26,27,28]
        elif selected_week == week_1_5[4]:
            dic[selected_week] = [29]
    else:
        if selected_week == week_1_5[0]:
            dic[selected_week] = [1,2,3,4,5,6,7]
        elif selected_week == week_1_5[1]:
            dic[selected_week] = [8,9,10,11,12,13,14]
        elif selected_week == week_1_5[2]:
            dic[selected_week] = [15,16,17,18,19,20,21]
        elif selected_week == week_1_5[3]:
            dic[selected_week] = [22,23,24,25,26,27,28]
        elif selected_week == week_1_5[4]:
            dic[selected_week] = [29,30,31]
    

    pass
    clear_win()
    win.geometry("350x120")
    canvas = Canvas(frame_win, bg = "white")
    
    label = Label(frame_win, text = "Choose The Year", font = ("Arial", 20))
    label.pack()
    label1 = Label(frame_win,text = "Choose a Year...", bg = "white",font = ("Courier", 10)).pack(pady=5)
    def toggle_size():
        global is_large
        if not is_large:
            win.geometry("350x400")
            is_large = True
        else:
            win.geometry("350x120")
            is_large = False      
    button = Button(frame_win, text="...", font = 'bold', height = 1,relief = SUNKEN,command=toggle_size)
    button.place(x = 250,y = 42)
    but_done = Button(frame_win, text = "Done",bd = 3, font = ("Arial",15), command = weekly_report)
    but_done.pack()
    canvas.pack(side = BOTTOM,expand = 1)
    scrollbar = Scrollbar(canvas)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    my_listbox5 = Listbox(canvas,yscrollcommand=scrollbar.set, width = 200,height = 400,font = ("Arial",20),selectmode = SINGLE)
    names5 = []
    all_year = []
    year_start = 2023
    for i in range(20):
        all_year.append(year_start+i)
    for i in range(len(all_year)):
        names5.append(all_year[i])
        my_listbox5.insert(END, f"{all_year[i]}")
    my_listbox5.pack(side=LEFT)
    scrollbar.config(command=my_listbox5.yview)
    win.mainloop()

def choose_week():
    global win, frame_win, months_lists,names4,my_listbox4,my_listbox3, names3,months_lists,win,frame_win,selected_month_weekly,week_1_5
    try:
        selected_choose_week = my_listbox3.curselection()
        my_listbox3 = my_listbox3
    
        selected_choose_week = str(selected_choose_week).replace(",)","").replace("(","")
    except:
        selected_choose_week = selected_choose_week
    d = {}
    for i in range(len(months_lists)):
        d[i] = months_lists[i]
    selected_month_weekly = d[int(selected_choose_week)]

   
    pass
    clear_win()
    win.geometry("350x120")
    
    canvas = Canvas(frame_win, bg = "white")
    
    label = Label(frame_win, text = "Choose The Week", font = ("Arial", 20))
    label.pack()
    label1 = Label(frame_win,text = "Choose a Week...", bg = "white",font = ("Courier", 10)).pack(pady=5)
    def toggle_size():
        global is_large
        if not is_large:
            win.geometry("350x400")
            is_large = True
        else:
            win.geometry("350x120")
            is_large = False      
    button = Button(frame_win, text="...", font = 'bold', height = 1,relief = SUNKEN,command=toggle_size)
    button.place(x = 250,y = 42)
    but_done = Button(frame_win, text = "Done",bd = 3, font = ("Arial",15), command = choose_year_weekly)
    but_done.pack()
    canvas.pack(side = BOTTOM,expand = 1)
    scrollbar = Scrollbar(canvas)
    scrollbar.pack(side=RIGHT, fill=Y)
    my_listbox4 = Listbox(canvas,yscrollcommand=scrollbar.set, width = 200,height = 400,font = ("Arial",20),selectmode = SINGLE)
    names4 = []
    
    if selected_month_weekly == "April" or selected_month_weekly == "June" or selected_month_weekly == "September" or selected_month_weekly == "November":
        week_1_5 = ["Week 1: Day<1-7>", "Week 2: Day<8-14>","Week 3: Day<15-21>","Week 4: Day<22-28>","Week 5: Day<29-30>"]
        for i in range(len(week_1_5)):
            names4.append(week_1_5[i])
            my_listbox4.insert(END, f"{week_1_5[i]}")
        my_listbox4.pack(side=LEFT)
        scrollbar.config(command=my_listbox4.yview)
        
    elif selected_month_weekly == "February":
        week_1_5 = ["Week 1: Day<1-7>", "Week 2: Day<8-14>","Week 3: Day<15-21>","Week 4: Day<22-28>","Week 5: Day<29>"]
        for i in range(len(week_1_5)):
            names4.append(week_1_5[i])
            my_listbox4.insert(END, f"{week_1_5[i]}")
        my_listbox4.pack(side=LEFT)
        scrollbar.config(command=my_listbox4.yview)
    else:
        week_1_5 = ["Week 1: Day<1-7>", "Week 2: Day<8-14>","Week 3: Day<15-21>","Week 4: Day<22-28>","Week 5: Day<29-31>"]
        for i in range(len(week_1_5)):
            names4.append(week_1_5[i])
            my_listbox4.insert(END, f"{week_1_5[i]}")
        my_listbox4.pack(side=LEFT)
        scrollbar.config(command=my_listbox4.yview)
    win.mainloop()
def choose_year_monthly():
    global win, frame_win, months_list,names_monthly,mylistbox_monthly,selected_month_monthly,names_monthly1,mylistbox_monthly1
    global fromChooseYearMonthly
    fromChooseYearMonthly = True
    try:
        selected_choose_year_monthly = mylistbox_monthly.curselection()
        mylistbox_monthly = mylistbox_monthly
    
        selected_choose_year_monthly = str(selected_choose_year_monthly).replace(",)","").replace("(","")
    except:
        selected_choose_year_monthly = selected_choose_year_monthly
    d = {}
    for i in range(len(months_lists)):
        d[i] = months_lists[i]
    selected_month_monthly = d[int(selected_choose_year_monthly)]
    print(selected_month_monthly)
   
    pass
    clear_win()
    win.geometry("350x120")
    
    canvas = Canvas(frame_win, bg = "white")
    
    label = Label(frame_win, text = "Choose The Year", font = ("Arial", 20))
    label.pack()
    label1 = Label(frame_win,text = "Choose a Year...", bg = "white",font = ("Courier", 10)).pack(pady=5)
    def toggle_size():
        global is_large
        if not is_large:
            win.geometry("350x400")
            is_large = True
        else:
            win.geometry("350x120")
            is_large = False      
    button = Button(frame_win, text="...", font = 'bold', height = 1,relief = SUNKEN,command=toggle_size)
    button.place(x = 250,y = 42)
    but_done = Button(frame_win, text = "Done",bd = 3, font = ("Arial",15), command = monthly_report)
    but_done.pack()
    canvas.pack(side = BOTTOM,expand = 1)
    scrollbar = Scrollbar(canvas)
    scrollbar.pack(side=RIGHT, fill=Y)
    mylistbox_monthly1 = Listbox(canvas,yscrollcommand=scrollbar.set, width = 200,height = 400,font = ("Arial",20),selectmode = SINGLE)
    names_monthly1 = []
    
    year_start_monthly = 2023
    for i in range(20):
        names_monthly1.append(year_start_monthly)
        mylistbox_monthly1.insert(END, f"{year_start_monthly}")
        year_start_monthly+=1
    mylistbox_monthly1.pack(side=LEFT)
    scrollbar.config(command=mylistbox_monthly1.yview)
     
    win.mainloop()
    
def choose_month_monthly_report():
    global win, frame_win, months_lists,names_monthly,mylistbox_monthly
    win = Tk()
    win.title('InventoProfit')
    win.geometry("350x120")
    win.attributes('-topmost', True)
    win.resizable(False,False)
    frame_win = Frame(win)
    frame_win.pack(fill = BOTH,expand = 1)
    canvas = Canvas(frame_win, bg = "white")
    
    label = Label(frame_win, text = "Choose The Month", font = ("Arial", 20))
    label.pack()
    label1 = Label(frame_win,text = "Choose a Month...", bg = "white",font = ("Courier", 10)).pack(pady=5)
    def toggle_size():
        global is_large
        if not is_large:
            win.geometry("350x400")
            is_large = True
        else:
            win.geometry("350x120")
            is_large = False      
    button = Button(frame_win, text="...", font = 'bold', height = 1,relief = SUNKEN,command=toggle_size)
    button.place(x = 250,y = 42)
    but_done = Button(frame_win, text = "Done",bd = 3, font = ("Arial",15), command = choose_year_monthly)
    but_done.pack()
    canvas.pack(side = BOTTOM,expand = 1)
    scrollbar = Scrollbar(canvas)
    scrollbar.pack(side=RIGHT, fill=Y)
    mylistbox_monthly = Listbox(canvas,yscrollcommand=scrollbar.set, width = 200,height = 400,font = ("Arial",20),selectmode = SINGLE)
    names_monthly = []
    for i in range(len(months_lists)):
        names_monthly.append(months_lists[i])	
        mylistbox_monthly.insert(END, f"{months_lists[i]}")
    mylistbox_monthly.pack(side=LEFT)
    scrollbar.config(command=mylistbox_monthly.yview)
    win.mainloop()
def choose_month_weekly_report():
    global win, frame_win, months_lists,names3,my_listbox3
    win = Tk()
    win.title('InventoProfit')
    win.geometry("350x120")
    win.attributes('-topmost', True)
    win.resizable(False,False)
    frame_win = Frame(win)
    frame_win.pack(fill = BOTH,expand = 1)
    canvas = Canvas(frame_win, bg = "white")
    
    label = Label(frame_win, text = "Choose The Month", font = ("Arial", 20))
    label.pack()
    label1 = Label(frame_win,text = "Choose a Month...", bg = "white",font = ("Courier", 10)).pack(pady=5)
    def toggle_size():
        global is_large
        if not is_large:
            win.geometry("350x400")
            is_large = True
        else:
            win.geometry("350x120")
            is_large = False      
    button = Button(frame_win, text="...", font = 'bold', height = 1,relief = SUNKEN,command=toggle_size)
    button.place(x = 250,y = 42)
    but_done = Button(frame_win, text = "Done",bd = 3, font = ("Arial",15), command = choose_week)
    but_done.pack()
    canvas.pack(side = BOTTOM,expand = 1)
    scrollbar = Scrollbar(canvas)
    scrollbar.pack(side=RIGHT, fill=Y)
    my_listbox3 = Listbox(canvas,yscrollcommand=scrollbar.set, width = 200,height = 400,font = ("Arial",20),selectmode = SINGLE)
    names3 = []
    for i in range(len(months_lists)):
        names3.append(months_lists[i])
        my_listbox3.insert(END, f"{months_lists[i]}")
    my_listbox3.pack(side=LEFT)
    scrollbar.config(command=my_listbox3.yview)
    win.mainloop()
def choose_month_daily_report():
    global win, frame_win, months_lists,names2,my_listbox2
    win = Tk()
    win.title('InventoProfit')
    win.geometry("350x120")
    win.attributes('-topmost', True)
    win.resizable(False,False)
    frame_win = Frame(win)
    frame_win.pack(fill = BOTH,expand = 1)
    canvas = Canvas(frame_win, bg = "white")
    
    label = Label(frame_win, text = "Choose The Month", font = ("Arial", 20))
    label.pack()
    label1 = Label(frame_win,text = "Choose a Month...", bg = "white",font = ("Courier", 10)).pack(pady=5)
    def toggle_size():
        global is_large
        if not is_large:
            win.geometry("350x400")
            is_large = True
        else:
            win.geometry("350x120")
            is_large = False      
    button = Button(frame_win, text="...", font = 'bold', height = 1,relief = SUNKEN,command=toggle_size)
    button.place(x = 250,y = 42)
    but_done = Button(frame_win, text = "Done",bd = 3, font = ("Arial",15), command = choose_day)
    but_done.pack()
    canvas.pack(side = BOTTOM,expand = 1)
    scrollbar = Scrollbar(canvas)
    scrollbar.pack(side=RIGHT, fill=Y)
    my_listbox2 = Listbox(canvas,yscrollcommand=scrollbar.set, width = 200,height = 400,font = ("Arial",20),selectmode = SINGLE)
    names2 = []
    for i in range(len(months_lists)):
        names2.append(months_lists[i])
        my_listbox2.insert(END, f"{months_lists[i]}")
    my_listbox2.pack(side=LEFT)
    scrollbar.config(command=my_listbox2.yview)
    win.mainloop()
def choose_year():
    global win, all_year,frame_win, months_lists,names3,my_listbox3,my_listbox2, names2,months_lists,win,frame_win,selected_month,selected_day,my_listbox4
    try:
        selected_choose_year = my_listbox3.curselection()
        my_listbox3 = my_listbox3
    
        selected_choose_year = str(selected_choose_year).replace(",)","").replace("(","")
    except:
        selected_choose_year = selected_choose_year
    d = {}
    if selected_month == "April" or selected_month == "June" or selected_month == "September" or selected_month == "November":
        for i in range(30):
            d[i] = i+1
        selected_day = d[int(selected_choose_year)]
    elif selected_month == "February":
        for i in range(29):
            d[i] = i+1
        selected_day = d[int(selected_choose_year)]
    else:
        for i in range(31):
            d[i] = i+1
        selected_day = d[int(selected_choose_year)]
    
    

    pass
    
    clear_win()
    win.geometry("350x120")
    
    canvas = Canvas(frame_win, bg = "white")
    
    label = Label(frame_win, text = "Choose The Year", font = ("Arial", 20))
    label.pack()
    label1 = Label(frame_win,text = "Choose a Year...", bg = "white",font = ("Courier", 10)).pack(pady=5)
    def toggle_size():
        global is_large
        if not is_large:
            win.geometry("350x400")
            is_large = True
        else:
            win.geometry("350x120")
            is_large = False      
    button = Button(frame_win, text="...", font = 'bold', height = 1,relief = SUNKEN,command=toggle_size)
    button.place(x = 250,y = 42)
    but_done = Button(frame_win, text = "Done",bd = 3, font = ("Arial",15), command = daily_report)
    but_done.pack()
    canvas.pack(side = BOTTOM,expand = 1)
    scrollbar = Scrollbar(canvas)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    my_listbox4 = Listbox(canvas,yscrollcommand=scrollbar.set, width = 200,height = 400,font = ("Arial",20),selectmode = SINGLE)
    names4 = []
    all_year = []
    year_start = 2023
    for i in range(20):
        all_year.append(year_start+i)
    for i in range(len(all_year)):
        names4.append(all_year[i])
        my_listbox4.insert(END, f"{all_year[i]}")
    my_listbox4.pack(side=LEFT)
    scrollbar.config(command=my_listbox4.yview)
    win.mainloop()

def auto_daily_report():
    global total_sales_daily,selected_month,selected_day,my_listbox3,all_year,my_listbox4,current_time
    
    
    current_year,current_month,current_day = current_time.year,month_determine(current_time),current_time.day
    item_name = file_opener()
    item_name_archive_text = file_opener_archive()
    
    item_name_list,selling_price_list = [],[]
    for i in range(len(item_name)):
        item_name_list.append(item_name[i])
        selling_price_list.append(selling_price[i])
    for i in range(len(item_name_archive_text)):
        item_name_list.append(item_name_archive_text[i])
        selling_price_list.append(selling_price_archive_text[i])
    clear()
    root.geometry("750x500")
    Label(frame, text = "DAILY SALES", font = ("Arial", 20, 'bold')).pack(pady=15)
  
    mainframe = Frame(frame)
    mainframe.pack(fill = 'both', expand= 0)
    root.title('InventoProfit')
    widest = 0
    for i in range(len(item_name_list)):
        total_sales_daily.append(0)
        if len(item_name_list[i]) > widest:
            widest = len(item_name_list[i])
        else:
            widest = widest
    canvas = Canvas(frame)
    scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.config(yscrollcommand=scrollbar.set)
    canvas.pack(fill=BOTH, expand=1)
    frame1 = Frame(canvas)
    canvas.create_window((0, 0), window=frame1, anchor=NW)
    texts = ['ITEM NAME','PRICE','QUANTITY','TOTAL SALES']
    item_name_pref, sales_quantity, date, _time, fields = [],[],[],[],[]
    file = open("./texts/items_preferences.txt", 'r')
    lines = file.readlines()
    file.close()
    for x in lines:
        fields = x.split(",")
        item_name_pref.append(fields[0])
        sales_quantity.append(int(fields[1]))
        date.append(fields[2])
        _time.append(fields[3].replace("\n",""))
    total_sales_item_amount = []
    
    for i in range(len(item_name_list)):
        total_sales_item_amount.append(0)
        for j in range(len(item_name_pref)):
            if item_name_pref[j] == item_name_list[i] and f"{current_month}:{current_day}:{current_year}" == date[j]:
                total_sales_item_amount[i] += sales_quantity[j]
          
           
    def label_sort(j,i,padx,padx1,padx2,padx3):
        if j==0:
            if i == 0:
                text.grid(row = 0, column=0)
            label.grid(row=i,column=0,padx = padx,pady = 10)
        elif j==1:
            if i == 0:
                text1.grid(row = 0, column=1,padx = 40)
            label1.grid(row=i,column=1,padx = padx1,pady = 10)
        elif j==2:
            if i == 0:
                text2.grid(row = 0, column=2,padx = 40)
            label2.grid(row=i,column=2,padx=padx2,pady = 10)
        elif j==3:
            if i == 0:
                text3.grid(row = 0, column=3,padx = 40)
            label3.grid(row=i,column=3,padx = padx3,pady = 10)
   
    total_sales = 0
    for i in range(len(item_name_list)):
        for j in range(4):
            text = Label(mainframe, text='ITEM NAME', font=('Arial', 15,'bold'))
            text1=Label(mainframe, text='  PRICE', font=('Arial', 15,'bold'))
            text2=Label(mainframe, text=' QUANTITY', font=('Arial', 15,'bold'))
            text3=Label(mainframe, text=' TOTAL SALES', font=('Arial', 15,'bold'))
            text4=Label(mainframe, text=' INCOME', font=('Arial', 15,'bold'))
            label = Label(frame1,text = f"{item_name_list[i]}", font = ("Arial",15),wraplength = 70) 
            label1 = Label(frame1,text = f"{'%.2f'%selling_price_list[i]}.php", font = ("Arial",15),wraplength = 130) 
            label2= Label(frame1,text = f"{total_sales_item_amount[i]}" , font = ("Arial",15),wraplength = 130)
            total_sales_daily[i] = selling_price_list[i]*total_sales_item_amount[i]
            label3 = Label(frame1,text = f"{'%.2f'%total_sales_daily[i]}", font = ("Arial",15),wraplength = 130)

            if widest < 3 :
                label_sort(j,i,20,60,40,80) 
            elif widest > 2 and widest < 5:
                label_sort(j,i,20,60,40,80)
            elif widest > 4 and widest < 7:
                label_sort(j,i,20,60,40,80)
            elif widest > 6 and widest < 9:
                label_sort(j,i,20,60,40,80)
            else:
                label_sort(j,i,20,60,40,80)
    for i in range(len(total_sales_daily)):
        total_sales+=total_sales_daily[i]
    frame1.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
 
    Label(frame, text = f"Date: {current_month}:{current_day}:{current_year}", font = ("Arial", 13)).place(x = 470,y=20)
    Label(frame, text = f"Total Sales of the Day: {'%.2f'%total_sales}", font = ("Arial", 13)).place(x = 470,y=40)
   
    label_sales = Label(frame, text="\u2190", font=("Arial", 25), fg="blue")
    label_sales.place(x = 0,y=0)
    Button(frame,text = "Sales History",bd = 1,command = choose_month_daily_report).place(x=50,y=0)
    global window
    window = "\u2190,daily_report"
    # Use the bind method to bind the click event to the label
    label_sales.bind("<Button-1>", label_clicked)
    label_sales.bind("<Enter>", label_enter)
    label_sales.bind("<Leave>", label_leave)



def daily_report():
    global total_sales_daily,selected_month,selected_day,my_listbox3,all_year,my_listbox4
    global selected_daily_report
    try:
        selected_daily_report = my_listbox4.curselection()
        my_listbox4 = my_listbox4
    
        selected_daily_report = str(selected_daily_report).replace(",)","").replace("(","")
    except:
        selected_daily_report = selected_daily_report
    d = {}
  
    for i in range(len(all_year)):
        d[i] = all_year[i]
    selected_year = d[int(selected_daily_report)]


    win.destroy()
    item_name = file_opener()
    item_name_archive_text = file_opener_archive()
    
    item_name_list,selling_price_list = [],[]
    for i in range(len(item_name)):
        item_name_list.append(item_name[i])
        selling_price_list.append(selling_price[i])
    for i in range(len(item_name_archive_text)):
        item_name_list.append(item_name_archive_text[i])
        selling_price_list.append(selling_price_archive_text[i])
        
    clear()
    root.geometry("750x500")
    Label(frame, text = "DAILY SALES", font = ("Arial", 20, 'bold')).pack(pady=15)
  
    mainframe = Frame(frame)
    mainframe.pack(fill = 'both', expand= 0)
    root.title('InventoProfit')
    widest = 0
    for i in range(len(item_name_list)):
        total_sales_daily.append(0)
        if len(item_name_list[i]) > widest:
            widest = len(item_name_list[i])
        else:
            widest = widest
    canvas = Canvas(frame)
    scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.config(yscrollcommand=scrollbar.set)
    canvas.pack(fill=BOTH, expand=1)
    frame1 = Frame(canvas)
    canvas.create_window((0, 0), window=frame1, anchor=NW)
    texts = ['ITEM NAME','PRICE','QUANTITY','TOTAL SALES']
    item_name_pref, sales_quantity, date, _time, fields = [],[],[],[],[]
    file = open("./texts/items_preferences.txt", 'r')
    lines = file.readlines()
    file.close()
    for x in lines:
        fields = x.split(",")
        item_name_pref.append(fields[0])
        sales_quantity.append(int(fields[1]))
        date.append(fields[2])
        _time.append(fields[3].replace("\n",""))
    total_sales_item_amount = []
    
    
    for i in range(len(item_name_list)):
        total_sales_item_amount.append(0)
        for j in range(len(item_name_pref)):
            if item_name_pref[j] == item_name_list[i] and f"{selected_month}:{selected_day}:{selected_year}" == date[j]:
                total_sales_item_amount[i] += sales_quantity[j]
          
           
    def label_sort(j,i,padx,padx1,padx2,padx3):
        if j==0:
            if i == 0:
                text.grid(row = 0, column=0)
            label.grid(row=i,column=0,padx = padx,pady = 10)
        elif j==1:
            if i == 0:
                text1.grid(row = 0, column=1,padx = 40)
            label1.grid(row=i,column=1,padx = padx1,pady = 10)
        elif j==2:
            if i == 0:
                text2.grid(row = 0, column=2,padx = 40)
            label2.grid(row=i,column=2,padx=padx2,pady = 10)
        elif j==3:
            if i == 0:
                text3.grid(row = 0, column=3,padx = 40)
            label3.grid(row=i,column=3,padx = padx3,pady = 10)
    
    total_sales = 0
    for i in range(len(item_name_list)):
        for j in range(4):
            text = Label(mainframe, text='ITEM NAME', font=('Arial', 15,'bold'))
            text1=Label(mainframe, text='  PRICE', font=('Arial', 15,'bold'))
            text2=Label(mainframe, text=' QUANTITY', font=('Arial', 15,'bold'))
            text3=Label(mainframe, text=' TOTAL SALES', font=('Arial', 15,'bold'))
            text4=Label(mainframe, text=' INCOME', font=('Arial', 15,'bold'))
            label = Label(frame1,text = f"{item_name_list[i]}", font = ("Arial",15),wraplength = 70) 
            label1 = Label(frame1,text = f"{'%.2f'%selling_price_list[i]}.php", font = ("Arial",15),wraplength = 130) 
            label2= Label(frame1,text = f"{total_sales_item_amount[i]}" , font = ("Arial",15),wraplength = 130)
            total_sales_daily[i] = selling_price_list[i]*total_sales_item_amount[i]
            label3 = Label(frame1,text = f"{'%.2f'%total_sales_daily[i]}", font = ("Arial",15),wraplength = 130)

            if widest < 3 :
                label_sort(j,i,20,60,40,80) 
            elif widest > 2 and widest < 5:
                label_sort(j,i,20,60,40,80)
            elif widest > 4 and widest < 7:
                label_sort(j,i,20,60,40,80)
            elif widest > 6 and widest < 9:
                label_sort(j,i,20,60,40,80)
            else:
                label_sort(j,i,20,60,40,80)
    for i in range(len(total_sales_daily)):
        total_sales+=total_sales_daily[i]
    frame1.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
 
    Label(frame, text = f"Date: {selected_month}:{selected_day}:{selected_year}", font = ("Arial", 13)).place(x = 470,y=20)
    Label(frame, text = f"Total Sales of the Day: {'%.2f'%total_sales}", font = ("Arial", 13)).place(x = 470,y=40)
   
    label_sales = Label(frame, text="\u2190", font=("Arial", 25), fg="blue")
    label_sales.place(x = 0,y=0)
    Button(frame,text = "Sales History",bd = 1,command = choose_month_daily_report).place(x=50,y=0)
    global window
    window = "\u2190,daily_report"
    # Use the bind method to bind the click event to the label
    label_sales.bind("<Button-1>", label_clicked)
    label_sales.bind("<Enter>", label_enter)
    label_sales.bind("<Leave>", label_leave)


def a():
    pass
def auto_monthly_report():
    global selected_month_monthly,names_monthly1,mylistbox_monthly1,selected_year_monthly,selected_week,selected,month,current_time
    global fromAutoMonthlyReport,fromAutoMonthlyReport
    fromAutoMonthlyReport,fromMonthlyReport = True,False
    
    current_year,current_month,current_day = current_time.year,month_determine(current_time),current_time.day
    item_name = file_opener()
    item_name_archive_text = file_opener_archive()
    
    item_name_list,selling_price_list = [],[]
    for i in range(len(item_name)):
        item_name_list.append(item_name[i])
        selling_price_list.append(selling_price[i])
    for i in range(len(item_name_archive_text)):
        item_name_list.append(item_name_archive_text[i])
        selling_price_list.append(selling_price_archive_text[i])
    clear()
    root.geometry("950x500")
    Label(frame, text = "MONTHLY SALES", font = ("Arial", 20, 'bold')).pack(pady=15)
  
    mainframe = Frame(frame)
    mainframe.pack(fill = 'both', expand= 0)
    root.title('InventoProfit')
    widest = 0
    for i in range(len(item_name_list)):
        total_sales_daily.append(0)
        if len(item_name_list[i]) > widest:
            widest = len(item_name_list[i])
        else:
            widest = widest
    canvas = Canvas(frame)
    scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.config(yscrollcommand=scrollbar.set)
    canvas.pack(fill=BOTH, expand=1)
    frame1 = Frame(canvas)
    canvas.create_window((0, 0), window=frame1, anchor=NW)
  
    item_name_pref, sales_quantity, date, _time, fields = [],[],[],[],[]
    file = open("./texts/items_preferences.txt", 'r')
    lines = file.readlines()
    file.close()
    for x in lines:
        fields = x.split(",")
        item_name_pref.append(fields[0])
        sales_quantity.append(int(fields[1]))
        date.append(fields[2])
        _time.append(fields[3].replace("\n",""))
    day_monthly,year_monthly,field = [],[],[]
    
    dic_for_sales_each_week = {}
    dic_for_selling_price = {}
    
    weeks = ["Week1","Week2","Week3","Week4","Week5"]
    for i in range(len(weeks)):
        dic_for_sales_each_week[weeks[i]] = 0
    for i in range(len(item_name_list)):
        dic_for_selling_price[item_name_list[i]] = selling_price_list[i]
        
    holder_sales_each_item = []
    total_sales_monthly= 0
    day = []
    year =[]
    month = []
    for i in range(len(item_name_pref)):
        x = date[i].split(":")
        day.append(x[1])
        year.append(x[2])
        month.append(x[0])
        holder_sales_each_item.append(0)
    
        
    if current_month == "June" or current_month == 'April' or current_month == "November" or current_month == "September":
        days_per_week = [[1,2,3,4,5,6,7],[8,9,10,11,12,13,14],[15,16,17,18,19,20,21],[22,23,24,25,26,27,28],[29,30]]
        for i in range(len(item_name_pref)):
            for j in range(len(item_name_list)):
      
                if (item_name_pref[i] == item_name_list[j]) and (int(year[i]) == int(current_year))and (month[i] == current_month):
                    holder_sales_each_item[i] = sales_quantity[i]*dic_for_selling_price[item_name_pref[i]]
                    for k in range(len(days_per_week)):
                        if int(day[i]) in days_per_week[k]:
                            
                            dic_for_sales_each_week[weeks[k]] +=holder_sales_each_item[i]
                
        
    elif current_month == "February":
        days_per_week = [[1,2,3,4,5,6,7],[8,9,10,11,12,13,14],[15,16,17,18,19,20,21],[22,23,24,25,26,27,28],[29]]
        for i in range(len(item_name_pref)):
            for j in range(len(item_name_list)):
      
                if (item_name_pref[i] == item_name_list[j]) and (int(year[i]) == int(current_year))and (month[i] == current_month):
                    holder_sales_each_item[i] = sales_quantity[i]*dic_for_selling_price[item_name_pref[i]]
                    for k in range(len(days_per_week)):
                        if int(day[i]) in days_per_week[k]:
                            
                            dic_for_sales_each_week[weeks[k]] +=holder_sales_each_item[i]
            
                            
    else:
        days_per_week = [[1,2,3,4,5,6,7],[8,9,10,11,12,13,14],[15,16,17,18,19,20,21],[22,23,24,25,26,27,28],[29,30,31]]
        for i in range(len(item_name_pref)):
            for j in range(len(item_name_list)):
      
                if (item_name_pref[i] == item_name_list[j]) and (int(year[i]) == int(current_year))and (month[i] == current_month):
                    holder_sales_each_item[i] = sales_quantity[i]*dic_for_selling_price[item_name_pref[i]]
                    for k in range(len(days_per_week)):
                        if int(day[i]) in days_per_week[k]:
                            
                            dic_for_sales_each_week[weeks[k]] +=holder_sales_each_item[i]
   
    def label_sort(i,j,padx,padx1):
        if j==0:
            if i == 0:
                text.grid(row = 0, column=0,padx=15)
            label.grid(row=i,column=0,padx = padx,pady = 10)
        elif j==1:
            if i == 0:
                text1.grid(row = 0, column=1,padx = 40)
            label1.grid(row=i,column=1,padx = padx1,pady = 10)
    
    

    for i in range(len(weeks)):
        for j in range(2):
            
            
            text=Label(mainframe, text=' DATE', font=('Arial', 15,'bold'))
            text1=Label(mainframe, text=' TOTAL SALES', font=('Arial', 15,'bold'))
            
            label = Label(frame1,text = f"{weeks[i]}", font = ("Arial",15),wraplength = 70)
            label1 = Label(frame1,text = f"{'%.2f'%dic_for_sales_each_week[weeks[i]]}", font = ("Arial",15),wraplength = 130)
          
            
            if widest < 3 :
                label_sort(i,j,20,20) 
            elif widest > 2 and widest < 5:
                label_sort(i,j,20,20)
            elif widest > 4 and widest < 7:
                label_sort(i,j,20,20)
            elif widest > 6 and widest < 9:
                label_sort(i,j,20,20)
            else:
                label_sort(i,j,20,20)
    total_sales_monthly = 0
    for i in range(len(dic_for_sales_each_week)):
        total_sales_monthly+=dic_for_sales_each_week[weeks[i]]
    
    lines,fields,expense_list_from_text_monthly,expense_from_text_monthly,date_monthly = [],[],[],[],[]
    file = open("./texts/monthly_expense_list.txt",'r')
    lines = file.readlines()
    file.close()
    for x in lines:
        fields = x.split(",")
        expense_list_from_text_monthly.append(fields[0])
        expense_from_text_monthly.append(fields[1])
        date_monthly.append(str(fields[2].replace("\n","")))
    
    current_date = f"{current_month}:{current_year}"
    total_expense_per_month_from_text = 0
    for i in range(len(date_monthly)):
        if date_monthly[i] == current_date:
            total_expense_per_month_from_text+=float(expense_from_text_monthly[i])
    net_profit_monthly = float(total_sales_monthly) - float(total_expense_per_month_from_text)
    
    frame1.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    
    without_mark_up = total_sales_monthly*.3
    gross_profit_monthly = total_sales_monthly - without_mark_up
    net_profit_monthly = float(gross_profit_monthly) - float(total_expense_per_month_from_text)
    total_expense_per_month_from_text = str('%.2f'%total_expense_per_month_from_text)
    net_profit_monthly = str('%.2f'%net_profit_monthly)
    without_mark_up = str('%.2f'%without_mark_up)
    total_sales_monthly = str('%.2f'%total_sales_monthly)
    gross_profit_monthly = str('%.2f'%gross_profit_monthly)

    
    Label(frame, text = f"Date: {current_month}:{current_year}", font = ("Arial", 13)).place(x = 620,y=20)
    Label(frame, text = f"Total Sales of the Month: {total_sales_monthly}", font = ("Arial", 13)).place(x = 620,y=40)
    Label(frame, text = f"Net Profit of the Month: {net_profit_monthly}", font = ("Arial", 13)).place(x = 620,y=60)
    Label(frame, text = "NET PROFIT FORMULA: ", font = ("Arial", 15)).place(x = 500,y=120)
    Label(frame, text = f"TOTAL SALES = {total_sales_monthly}", font = ("Arial", 12)).place(x = 500,y=160)
    Label(frame, text = f"TOTAL EXPENSES = {total_expense_per_month_from_text} ", font = ("Arial", 12)).place(x = 500,y=180)
    Label(frame, text = "GROSS PROFIT = TOTAL SALES - TOTAL SALES(30%) ", font = ("Arial", 12)).place(x = 500,y=200)
    Label(frame, text = "NET PROFIT = GROSS PROFIT - TOTAL EXPENSES ", font = ("Arial", 12)).place(x = 500,y=220)

    Label(frame, text = f"GROSS PROFIT = {total_sales_monthly} - {without_mark_up} = {gross_profit_monthly} ", font = ("Arial", 12)).place(x = 500,y=260)
    Label(frame, text = f"GROSS PROFIT =", font = ("Arial", 12)).place(x = 500,y=280)
    Label(frame, text = f"{gross_profit_monthly}", font = ("Arial", 12,'bold')).place(x = 630,y=280)
    Label(frame, text = f"NET PROFIT = {gross_profit_monthly} - {total_expense_per_month_from_text} = {net_profit_monthly} ", font = ("Arial", 12)).place(x = 500,y=300)
    Label(frame, text = f"NET PROFIT =", font = ("Arial", 12)).place(x = 500,y=320)
    Label(frame, text = f"{net_profit_monthly}", font = ("Arial", 12,'bold')).place(x = 620,y=320)
    
    Button(frame, text = "Monthly Expenses", bd = 1, command = lambda: monthly_expenses(current_month,current_year)).place(x = 50,y = 10)
    label_sales = Label(frame, text="\u2190", font=("Arial", 25), fg="blue")
    label_sales.place(x = 0,y=0)
    Button(frame,text = "Sales History",bd = 1,command = choose_month_monthly_report).place(x=160,y=10)
    global window
    window = "\u2190,daily_report"
    # Use the bind method to bind the click event to the label
    label_sales.bind("<Button-1>", label_clicked)
    label_sales.bind("<Enter>", label_enter)
    label_sales.bind("<Leave>", label_leave)

    
fromMonthlyReport,fromAutoMonthlyReport,fromChooseYearMonthly = False,False,False

def monthly_report():
    global total_sales_daily,selected_month_monthly,names_monthly1,mylistbox_monthly1,selected_year_monthly,selected_week,selected
    global fromAutoMonthlyReport,fromMonthlyReport,fromChooseYearMonthly
    fromAutoMonthlyReport,fromMonthlyReport = False,True
    if fromChooseYearMonthly == True:
        try:
            selected_monthly_report = mylistbox_monthly1.curselection()
            mylistbox_monthly1 = mylistbox_monthly1
        
            selected_monthly_report = str(selected_monthly_report).replace(",)","").replace("(","")
        except:
            selected_monthly_report = selected_monthly_report
        d = {}
        year_start_monthly = 2023
        all_year = []
        for i in range(20):
            all_year.append(year_start_monthly)
            year_start_monthly+=1
        for i in range(20):
            d[i] = all_year[i]
        selected_year_monthly = d[int(selected_monthly_report)]
        fromChooseYearMonthly = False
    else:
        selected_year_monthly = selected_year_monthly
    win.destroy()
    item_name = file_opener()
    item_name_archive_text = file_opener_archive()

    item_name_list,selling_price_list = [],[]
    for i in range(len(item_name)):
        item_name_list.append(item_name[i])
        selling_price_list.append(selling_price[i])
    for i in range(len(item_name_archive_text)):
        item_name_list.append(item_name_archive_text[i])
        selling_price_list.append(selling_price_archive_text[i])

    clear()
    root.geometry("950x500")
    Label(frame, text = "MONTHLY SALES", font = ("Arial", 20, 'bold')).pack(pady=15)
  
    mainframe = Frame(frame)
    mainframe.pack(fill = 'both', expand= 0)
    root.title('InventoProfit')
    widest = 0
    for i in range(len(item_name_list)):
        total_sales_daily.append(0)
        if len(item_name_list[i]) > widest:
            widest = len(item_name_list[i])
        else:
            widest = widest
    canvas = Canvas(frame)
    scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.config(yscrollcommand=scrollbar.set)
    canvas.pack(fill=BOTH, expand=1)
    frame1 = Frame(canvas)
    canvas.create_window((0, 0), window=frame1, anchor=NW)
  
    item_name_pref, sales_quantity, date, _time, fields = [],[],[],[],[]
    file = open("./texts/items_preferences.txt", 'r')
    lines = file.readlines()
    file.close()
    for x in lines:
        fields = x.split(",")
        item_name_pref.append(fields[0])
        sales_quantity.append(int(fields[1]))
        date.append(fields[2])
        _time.append(fields[3].replace("\n",""))
    day_monthly,year_monthly,field = [],[],[]
   
    dic_for_sales_each_week = {}
    dic_for_selling_price = {}
    
    weeks = ["Week1","Week2","Week3","Week4","Week5"]
    for i in range(len(weeks)):
        dic_for_sales_each_week[weeks[i]] = 0
    for i in range(len(item_name_list)):
        dic_for_selling_price[item_name_list[i]] = selling_price_list[i]
        
    holder_sales_each_item = []
    total_sales_monthly= 0
    day = []
    year =[]
    month = []
    for i in range(len(item_name_pref)):
        x = date[i].split(":")
        day.append(x[1])
        year.append(x[2])
        month.append(x[0])
        holder_sales_each_item.append(0)
    
        
    if selected_year_monthly == "June" or selected_year_monthly == 'April' or selected_year_monthly == "November" or selected_year_monthly == "September":
        days_per_week = [[1,2,3,4,5,6,7],[8,9,10,11,12,13,14],[15,16,17,18,19,20,21],[22,23,24,25,26,27,28],[29,30]]
        for i in range(len(item_name_pref)):
            for j in range(len(item_name_list)):
      
                if (item_name_pref[i] == item_name_list[j]) and (int(year[i]) == int(selected_year_monthly))and (month[i] == selected_month_monthly):
                    holder_sales_each_item[i] = sales_quantity[i]*dic_for_selling_price[item_name_pref[i]]
                    for k in range(len(days_per_week)):
                        if int(day[i]) in days_per_week[k]:
                            
                            dic_for_sales_each_week[weeks[k]] +=holder_sales_each_item[i]
                
        
    elif selected_year_monthly == "February":
        days_per_week = [[1,2,3,4,5,6,7],[8,9,10,11,12,13,14],[15,16,17,18,19,20,21],[22,23,24,25,26,27,28],[29]]
        for i in range(len(item_name_pref)):
            for j in range(len(item_name_list)):
      
                if (item_name_pref[i] == item_name_list[j]) and (int(year[i]) == int(selected_year_monthly))and (month[i] == selected_month_monthly):
                    holder_sales_each_item[i] = sales_quantity[i]*dic_for_selling_price[item_name_pref[i]]
                    for k in range(len(days_per_week)):
                        if int(day[i]) in days_per_week[k]:
                            
                            dic_for_sales_each_week[weeks[k]] +=holder_sales_each_item[i]
            
                            
    else:
        days_per_week = [[1,2,3,4,5,6,7],[8,9,10,11,12,13,14],[15,16,17,18,19,20,21],[22,23,24,25,26,27,28],[29,30,31]]
        for i in range(len(item_name_pref)):
            for j in range(len(item_name_list)):
      
                if (item_name_pref[i] == item_name_list[j]) and (int(year[i]) == int(selected_year_monthly))and (month[i] == selected_month_monthly):
                    holder_sales_each_item[i] = sales_quantity[i]*dic_for_selling_price[item_name_pref[i]]
                    for k in range(len(days_per_week)):
                        if int(day[i]) in days_per_week[k]:
                            
                            dic_for_sales_each_week[weeks[k]] +=holder_sales_each_item[i]
    
    def label_sort(i,j,padx,padx1):
        if j==0:
            if i == 0:
                text.grid(row = 0, column=0,padx=15)
            label.grid(row=i,column=0,padx = padx,pady = 10)
        elif j==1:
            if i == 0:
                text1.grid(row = 0, column=1,padx = 40)
            label1.grid(row=i,column=1,padx = padx1,pady = 10)
    
    

    for i in range(len(weeks)):
        for j in range(2):
            
            
            text=Label(mainframe, text=' DATE', font=('Arial', 15,'bold'))
            text1=Label(mainframe, text=' TOTAL SALES', font=('Arial', 15,'bold'))
            
            label = Label(frame1,text = f"{weeks[i]}", font = ("Arial",15),wraplength = 70)
            label1 = Label(frame1,text = f"{'%.2f'%dic_for_sales_each_week[weeks[i]]}", font = ("Arial",15),wraplength = 130)
          
            
            if widest < 3 :
                label_sort(i,j,20,20) 
            elif widest > 2 and widest < 5:
                label_sort(i,j,20,20)
            elif widest > 4 and widest < 7:
                label_sort(i,j,20,20)
            elif widest > 6 and widest < 9:
                label_sort(i,j,20,20)
            else:
                label_sort(i,j,20,20)
    total_sales_monthly = 0
    for i in range(len(weeks)):
        total_sales_monthly+=dic_for_sales_each_week[weeks[i]]
    
    lines,fields,expense_list_from_text_monthly,expense_from_text_monthly,date_monthly = [],[],[],[],[]
    file = open("./texts/monthly_expense_list.txt",'r')
    lines = file.readlines()
    file.close()
    for x in lines:
        fields = x.split(",")
        expense_list_from_text_monthly.append(fields[0])
        expense_from_text_monthly.append(fields[1])
        date_monthly.append(str(fields[2].replace("\n","")))
   
    current_date = f"{selected_month_monthly}:{selected_year_monthly}"
    total_expense_per_month_from_text = 0
    for i in range(len(date_monthly)):
        if date_monthly[i] == current_date:
            total_expense_per_month_from_text+=float(expense_from_text_monthly[i])
    net_profit_monthly = float(total_sales_monthly) - float(total_expense_per_month_from_text)
    
    frame1.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    
    without_mark_up = total_sales_monthly*.3
    gross_profit_monthly = total_sales_monthly - without_mark_up
    net_profit_monthly = float(gross_profit_monthly) - float(total_expense_per_month_from_text)
    total_expense_per_month_from_text = str('%.2f'%total_expense_per_month_from_text)
    net_profit_monthly = str('%.2f'%net_profit_monthly)
    without_mark_up = str('%.2f'%without_mark_up)
    total_sales_monthly = str('%.2f'%total_sales_monthly)
    gross_profit_monthly = str('%.2f'%gross_profit_monthly)

    
    Label(frame, text = f"Date: {selected_month_monthly}:{selected_year_monthly}", font = ("Arial", 13)).place(x = 620,y=20)
    Label(frame, text = f"Total Sales of the Month: {total_sales_monthly}", font = ("Arial", 13)).place(x = 620,y=40)
    Label(frame, text = f"Net Profit of the Month: {net_profit_monthly}", font = ("Arial", 13)).place(x = 620,y=60)
    Label(frame, text = "NET PROFIT FORMULA: ", font = ("Arial", 15)).place(x = 500,y=120)
    Label(frame, text = f"TOTAL SALES = {total_sales_monthly}", font = ("Arial", 12)).place(x = 500,y=160)
    Label(frame, text = f"TOTAL EXPENSES = {total_expense_per_month_from_text} ", font = ("Arial", 12)).place(x = 500,y=180)
    Label(frame, text = "GROSS PROFIT = TOTAL SALES - TOTAL SALES(30%) ", font = ("Arial", 12)).place(x = 500,y=200)
    Label(frame, text = "NET PROFIT = GROSS PROFIT - TOTAL EXPENSES ", font = ("Arial", 12)).place(x = 500,y=220)

    Label(frame, text = f"GROSS PROFIT = {total_sales_monthly} - {without_mark_up} = {gross_profit_monthly} ", font = ("Arial", 12)).place(x = 500,y=260)
    Label(frame, text = f"GROSS PROFIT =", font = ("Arial", 12)).place(x = 500,y=280)
    Label(frame, text = f"{gross_profit_monthly}", font = ("Arial", 12,'bold')).place(x = 630,y=280)
    Label(frame, text = f"NET PROFIT = {gross_profit_monthly} - {total_expense_per_month_from_text} = {net_profit_monthly} ", font = ("Arial", 12)).place(x = 500,y=300)
    Label(frame, text = f"NET PROFIT =", font = ("Arial", 12)).place(x = 500,y=320)
    Label(frame, text = f"{net_profit_monthly}", font = ("Arial", 12,'bold')).place(x = 620,y=320)
    
    Button(frame, text = "Monthly Expenses", bd = 1, command = lambda: monthly_expenses(selected_month_monthly,selected_year_monthly)).place(x = 50,y = 10)
    label_sales = Label(frame, text="\u2190", font=("Arial", 25), fg="blue")
    label_sales.place(x = 0,y=0)
    Button(frame,text = "Sales History",bd = 1,command = choose_month_monthly_report).place(x=160,y=10)
    global window
    window = "\u2190,daily_report"
    # Use the bind method to bind the click event to the label
    label_sales.bind("<Button-1>", label_clicked)
    label_sales.bind("<Enter>", label_enter)
    label_sales.bind("<Leave>", label_leave)


expense_list = ['Food','Water','Rent','Electricity','Miscellanous']
expense_amount = []

all_year_weekly = 20
year_start_weekly = 2023

weeks = ['Week1','Week2','Week3','Week4','Week5']
months_lists = ["January","February","March","April","May","June","July","August","September","October","November","December"]


def text_weekly_expense_list_edit(expenses,current_expense,current_date,current_expense_list):
    global expense_list,expense_amount,all_year_weekly,year_start_weekly,months_lists,weeks,expense_from_text,dates
    

    lines,fields,expense_from_text,expense_list_from_text = [],[],[],[]
    dates = []
    file = open("./texts/weekly_expense_list.txt",'r')
    lines = file.readlines()
    file.close()
    for x in lines:
        fields = x.split(",")
        expense_list_from_text.append(fields[0])
        expense_from_text.append(fields[1])
    
    file = open("./texts/weekly_expense_list.txt",'w')
    file.write("")
    file.close()
    
    for i in range(all_year_weekly):
            for j in range(len(weeks)):
                for k in range(len(months_lists)):
                    dates.append(f"{months_lists[k]}:{weeks[j]}:{year_start_weekly}")
            year_start_weekly+=1
    dates_with_expenses = []
    for i in range(len(dates)):
        for j in range(len(expense_list)):
            dates_with_expenses.append(dates[i])
    
    year_start_weekly = 2023
    
    if expenses != None:
        
        for i in range(len(dates_with_expenses)):
            
            if dates_with_expenses[i] == current_date:
                
                if expense_list_from_text[i] == current_expense_list:
                    
                    expense_from_text[i] = expenses
                    print(expense_list_from_text[i],expense_from_text[i],dates_with_expenses[i])
            file = open("./texts/weekly_expense_list.txt",'a')
            file.write(f"{expense_list_from_text[i]},{expense_from_text[i]},{dates_with_expenses[i]}\n")
            file.close()
    else:
        try:
            
            for i in range(len(dates_with_expenses)):
                
                file = open("./texts/weekly_expense_list.txt",'a')
                file.write(f"{expense_list_from_text[i]},{expense_from_text[i]},{dates_with_expenses[i]}\n")
                file.close()
                        
        
        except:
            for i in range(len(dates)):
                for l in range(len(expense_list)):
                    file = open("./texts/weekly_expense_list.txt",'a')
                    file.write(f"{expense_list[l]},0,{dates[i]}\n")
                    file.close()
                    
                    
   
text_weekly_expense_list_edit(None,None,None,None)
year_start_monthly = 2023
def text_monthly_expense_list_edit(expenses_monthly,current_expense,current_date,current_expense_list):
    global expense_list,expense_amount,all_year_monthly,year_start_monthly,months_lists,weeks,expense_from_text_monthly,dates_monthly
    
    all_year_monthly = 20
    lines,fields,expense_from_text_monthly,expense_list_from_text_monthly = [],[],[],[]
    date_from_text = []
    file = open("./texts/monthly_expense_list.txt",'r')
    lines = file.readlines()
    file.close()
    for x in lines:
        fields = x.split(",")
        expense_list_from_text_monthly.append(fields[0])
        expense_from_text_monthly.append(fields[1])
        date_from_text.append(fields[2].replace("\n",""))
    file = open("./texts/monthly_expense_list.txt",'w')
    file.write("")
    file.close()
    dates_monthly = []
    for i in range(all_year_monthly):
        for j in range(len(months_lists)):
                
            dates_monthly.append(f"{months_lists[j]}:{year_start_monthly}")
        year_start_monthly+=1
    year_start_monthly = 2023
    dates_with_expenses = []
    for i in range(len(dates_monthly)):
        for j in range(len(expense_list)):
            dates_with_expenses.append(dates_monthly[i])
    if expenses_monthly != None:
        pass
        
        for i in range(len(dates_with_expenses)):
            
            if dates_with_expenses[i] == current_date:
                
                if expense_list_from_text_monthly[i] == current_expense_list:
                    
                    expense_from_text_monthly[i] = expenses_monthly
                    
            file = open("./texts/monthly_expense_list.txt",'a')
            file.write(f"{expense_list_from_text_monthly[i]},{expense_from_text_monthly[i]},{date_from_text[i]}\n")
            file.close()
    else:
       
        file = open("./texts/monthly_expense_list.txt",'r')
        lines = file.readlines()
        file.close()
        
        try:
            
            for i in range(len(dates_with_expenses)):
                file = open("./texts/monthly_expense_list.txt",'a')
                file.write(f"{expense_list_from_text_monthly[i]},{expense_from_text_monthly[i]},{date_from_text[i]}\n")
                file.close()
                        
        
        except:
            for i in range(len(dates_monthly)):
                for l in range(len(expense_list)):
                    file = open("./texts/monthly_expense_list.txt",'a')
                    file.write(f"{expense_list[l]},0,{dates_monthly[i]}\n")
                    file.close()
 
text_monthly_expense_list_edit(None,None,None,None)
def monthly_expenses(selected_month_monthly,selected_year_monthly):
    user_role = define_user_role()
    if user_role == 'admin':
        global win, frame_win,expense_list,expense_amount
        lines,fields,expense_from_text_monthly,date_monthly,expense_list_from_text_monthly = [],[],[],[],[]
        
        file = open("./texts/monthly_expense_list.txt",'r')
        lines = file.readlines()
        file.close()
        
        for x in lines:
            fields = x.split(",")
            expense_list_from_text_monthly.append(fields[0])
            expense_from_text_monthly.append(fields[1])
            date_monthly.append(str(fields[2].replace("\n","")))
        
        current_date = f"{selected_month_monthly}:{selected_year_monthly}"
        current_expense_list,current_expense,current_date_monthly = [],[],[]
        
        for i in range(len(date_monthly)):
            if str(date_monthly[i]) == str(current_date):
               
                current_expense.append(expense_from_text_monthly[i])
        for i in range(len(expense_list)):
            d[expense_list[i]] =current_expense[i] 
        
        
        global item_name
        item_name = file_opener()
        win = Tk()
        win.title('InventoProfit')
        win.geometry('400x500')
        win.attributes('-topmost', True)
        win.resizable(False,False)
        frame_win = Frame(win)
        frame_win.pack(fill = BOTH,expand = 1)
        mainframe = Frame(frame_win)
        mainframe.pack(fill = 'both', expand= 0)
        root.title('InventoProfit')
        canvas = Canvas(frame_win)
        scrollbar = Scrollbar(frame_win, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.config(yscrollcommand=scrollbar.set)
        canvas.pack(fill=BOTH, expand=1)
        frame1 = Frame(canvas)
        canvas.create_window((0, 0), window=frame1, anchor=NW)
        
        def create_button(i):
            global expense_list
            global button
            button = Button(frame1, text=f"{expense_list[i]}", font = ("Arial", 15),bd = 1,command=lambda: input_user(i))
            button.grid(row = i, column = 0,pady=10)
            for j in range(len(expense_list)):
                for k in range(2):
                    if j == 0:
                        Label(mainframe,text = f"  LIST 	        EXPENSES",font = ("Arial", 15)).grid(row = j)
                    Label(frame1,text = f"{d[expense_list[i]]}",font = ("Arial", 15),bd = 1).grid(row = i, column = 1,pady=10,padx=40)
        for i in range(len(expense_list)):
            create_button(i)
        def input_user(i):
            clear_win()
            win.geometry("450x120")
            win.attributes('-topmost', True)
            win.resizable(False,False)
            label = Label(frame_win, text = f"{expense_list[i].title()} Monthly Expenses", font = ("Arial", 20))
            label.pack()
            text = Text(frame_win, width = 20, height = 1)
            text.pack(pady = 5)
            def handle_keypress(event):
                if event.keysym == "Return":
                    return "break"  # Prevents the default behavior of the Enter key
                else:
                    # Perform any other desired actions
                    pass
            text.bind("<KeyPress>", handle_keypress)
            def gets_expenses():
                global expenses,months_lists,selected_monthly_report,fromAutoMonthlyReport,fromMonthlyReport
                global expense_list,year_start_weekly,expense_from_text,d
                nonlocal i,current_expense,current_date
                year_start_weekly = 2023
                expenses = text.get(1.0,"end-1c")  
                try:       
                    expenses =  float(expenses)
                    text_monthly_expense_list_edit(expenses,current_expense[i],current_date,expense_list[i])
                    print(fromMonthlyReport,fromAutoMonthlyReport)
                    if fromMonthlyReport == True and fromAutoMonthlyReport == False:
                        monthly_report()
                    elif fromMonthlyReport == False and fromAutoMonthlyReport == True:
                        auto_monthly_report()
                    
                    win.destroy()
                except Exception as e:
                    print(e,"monthly_expenses")
                    handler = f"could not convert string to float: '{expense_from_text_monthly}'"
                    e = str(e)
                    if handler == e:
                        tkinter.messagebox.showinfo("ERROR",  "Input Must Be NUMBER!")
                        input_user(i)         
            but_done = Button(frame_win, text = "Done",bd = 3, font = ("Arial",15), command = gets_expenses)
            but_done.pack() 
        frame1.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
    else:
        tkinter.messagebox.showinfo("NOTICE","ONLY ADMIN CAN ACCESS")
def auto_weekly_report():
    global current_year,current_time,selected_month,selected_day_weekly,my_listbox5,week_1_5,selected_month_weekly,selected_week,selected_year_weekly,dic,selected
    global fromAutoWeeklyReport,fromWeeklyReport
    fromAutoWeeklyReport = True
    fromWeeklyReport = False
    
    array_days_of_week = []
    current_year,current_month,current_day = current_time.year,month_determine(current_time),current_time.day
    current_week = ""
    
    if current_day in [1,2,3,4,5,6,7]:
        array_days_of_week = [1,2,3,4,5,6,7]
        current_week = "Week 1: Day<1-7>"
    elif current_day in [8,9,10,11,12,13,14]:
        array_days_of_week = [8,9,10,11,12,13,14]
        current_week = "Week 2: Day<8-14>"
    elif current_day in [15,16,17,18,19,20,21]:
        array_days_of_week = [15,16,17,18,19,20,21]
        current_week = "Week 3: Day<15-21>"
    elif current_day in [22,23,24,25,26,27,28]:
        array_days_of_week = [22,23,24,25,26,27,28]
        current_week = "Week 4: Day<22-28>"
   
    if current_month == "November" or current_month == "June" or current_month == "September" or current_month == "April":
        if current_day in [1,2,3,4,5,6,7]:
            array_days_of_week = [1,2,3,4,5,6,7]
            
        elif current_day in [8,9,10,11,12,13,14]:
            array_days_of_week = [8,9,10,11,12,13,14]
        elif current_day in [15,16,17,18,19,20,21]:
            array_days_of_week = [15,16,17,18,19,20,21]
        elif current_day in [22,23,24,25,26,27,28]:
            array_days_of_week = [22,23,24,25,26,27,28]
        elif current_day in [29,30]:
            array_days_of_week = [29,30]
            
    elif current_month == "February":
        if current_day in [1,2,3,4,5,6,7]:
            array_days_of_week = [1,2,3,4,5,6,7]
        elif current_day in [8,9,10,11,12,13,14]:
            array_days_of_week = [8,9,10,11,12,13,14]
        elif current_day in [15,16,17,18,19,20,21]:
            array_days_of_week = [15,16,17,18,19,20,21]
        elif current_day in [22,23,24,25,26,27,28]:
            array_days_of_week = [22,23,24,25,26,27,28]
        elif current_day in [29]:
            array_days_of_week = [29]
           
    else:
        if current_day in [1,2,3,4,5,6,7]:
            array_days_of_week = [1,2,3,4,5,6,7]
        elif current_day in [8,9,10,11,12,13,14]:
            array_days_of_week = [8,9,10,11,12,13,14]
        elif current_day in [15,16,17,18,19,20,21]:
            array_days_of_week = [15,16,17,18,19,20,21]
        elif current_day in [22,23,24,25,26,27,28]:
            array_days_of_week = [22,23,24,25,26,27,28]
        elif current_day in [29,30,31]:
            array_days_of_week = [29,30,31]
            
            
    
    item_name = file_opener()
    item_name_archive_text = file_opener_archive()
    
    item_name_list,selling_price_list = [],[]
    for i in range(len(item_name)):
        item_name_list.append(item_name[i])
        selling_price_list.append(selling_price[i])
    for i in range(len(item_name_archive_text)):
        item_name_list.append(item_name_archive_text[i])
        selling_price_list.append(selling_price_archive_text[i])
    clear()
    root.geometry("950x500")
    Label(frame, text = "WEEKLY SALES", font = ("Arial", 20, 'bold')).pack(pady=15)
  
    mainframe = Frame(frame)
    mainframe.pack(fill = 'both', expand= 0)
    root.title('InventoProfit')
    widest = 0
    for i in range(len(item_name_list)):
        total_sales_daily.append(0)
        if len(item_name_list[i]) > widest:
            widest = len(item_name_list[i])
        else:
            widest = widest
    canvas = Canvas(frame)
    scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.config(yscrollcommand=scrollbar.set)
    canvas.pack(fill=BOTH, expand=1)
    frame1 = Frame(canvas)
    canvas.create_window((0, 0), window=frame1, anchor=NW)
 
    item_name_pref, sales_quantity, date, _time, fields = [],[],[],[],[]
    file = open("./texts/items_preferences.txt", 'r')
    lines = file.readlines()
    file.close()
    for x in lines:
        fields = x.split(",")
        item_name_pref.append(fields[0])
        sales_quantity.append(int(fields[1]))
        date.append(fields[2])
        _time.append(fields[3].replace("\n",""))
    
    dic_for_selling_price = {}
    dic_for_total_sales_each_day = {}
    for i in range(len(array_days_of_week)):
        dic_for_total_sales_each_day[array_days_of_week[i]] = 0
    holder_sales_each_item = []
    holder_sales_each_day = []
    total_sales_per_day = []
    total_sales_weekly= 0
    for i in range(len(item_name_list)):
        dic_for_selling_price[item_name_list[i]] = selling_price_list[i]
    day = []
    year =[]
    month = []
    for i in range(len(item_name_pref)):
        x = date[i].split(":")
        day.append(x[1])
        year.append(x[2])
        month.append(x[0])
        holder_sales_each_item.append(0)
        holder_sales_each_day.append(0)
    for i in range(len(array_days_of_week)):
        total_sales_per_day.append(0)
    for i in range(len(item_name_pref)):
        for j in range(len(item_name_list)):
  
            if (item_name_pref[i] == item_name_list[j]) and (int(day[i]) in array_days_of_week) and (int(year[i]) == int(current_year) )and (month[i] == current_month):
                
                holder_sales_each_item[i] = sales_quantity[i]*dic_for_selling_price[item_name_pref[i]]
                for k in range(len(array_days_of_week)):
                    if day[i] == array_days_of_week[k]:
                        holder_sales_each_day[i] = dic_for_selling_price[item_name_pref[i]]*sales_quantity[i]
                    
    for i in range(len(item_name_pref)):
        for j in range(len(array_days_of_week)):
            if int(day[i]) == array_days_of_week[j] and (int(year[i]) == int(current_year) )and (month[i] == current_month):
                
                holder_sales_each_day[i] = dic_for_selling_price[item_name_pref[i]]*sales_quantity[i]
                dic_for_total_sales_each_day[array_days_of_week[j]]+=holder_sales_each_day[i]
                    
    for i in range(len(holder_sales_each_item)):
        total_sales_weekly +=holder_sales_each_item[i]
    
    
    def label_sort(i,j,padx,padx1):
        if j==0:
            if i == 0:
                text.grid(row = 0, column=0,padx=15)
            label.grid(row=i,column=0,padx = padx,pady = 10)
        elif j==1:
            if i == 0:
                text1.grid(row = 0, column=1,padx = 40)
            label1.grid(row=i,column=1,padx = padx1,pady = 10)
       
    
    for i in range(len(array_days_of_week)):
        for j in range(2):
            
            
            text=Label(mainframe, text=' DATE', font=('Arial', 15,'bold'))
            text1=Label(mainframe, text=' TOTAL SALES', font=('Arial', 15,'bold'))
            
            label = Label(frame1,text = f"Day:{array_days_of_week[i]}", font = ("Arial",15),wraplength = 70)
            label1 = Label(frame1,text = f"{'%.2f'%dic_for_total_sales_each_day[array_days_of_week[i]]}", font = ("Arial",15),wraplength = 130)
          
            
            if widest < 3 :
                label_sort(i,j,20,20) 
            elif widest > 2 and widest < 5:
                label_sort(i,j,20,20)
            elif widest > 4 and widest < 7:
                label_sort(i,j,20,20)
            elif widest > 6 and widest < 9:
                label_sort(i,j,20,20)
            else:
                label_sort(i,j,20,20)
    
    lines,fields,expense_list_from_text,expense_from_text,date = [],[],[],[],[]
    file = open("./texts/weekly_expense_list.txt",'r')
    lines = file.readlines()
    file.close()
    for x in lines:
        fields = x.split(",")
        expense_list_from_text.append(fields[0])
        expense_from_text.append(fields[1])
        date.append(str(fields[2].replace("\n","")))
    
    week_field = []
    week_field = current_week.split(":")
    current_week_for_comparison = week_field[0].replace(" ","")
    current_date = f"{current_month}:{current_week_for_comparison}:{current_year}"
    total_expense_per_week_from_text = 0
    for i in range(len(date)):
        if date[i] == current_date:
            total_expense_per_week_from_text+=float(expense_from_text[i])
    
    
    without_mark_up = total_sales_weekly*.3
    gross_profit_weekly = total_sales_weekly - without_mark_up
    net_profit_weekly = float(gross_profit_weekly) - float(total_expense_per_week_from_text)
    total_expense_per_week_from_text = str('%.2f'%total_expense_per_week_from_text)
    net_profit_weekly = str('%.2f'%net_profit_weekly)
    without_mark_up = str('%.2f'%without_mark_up)
    total_sales_weekly = str('%.2f'%total_sales_weekly)
    gross_profit_weekly = str('%.2f'%gross_profit_weekly)
    frame1.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    
    
    
    Label(frame, text = f"Date: {current_month}:{current_week}:{current_year}", font = ("Arial", 13)).place(x = 620,y=20)
    Label(frame, text = f"Total Sales of the Week: {total_sales_weekly}", font = ("Arial", 13)).place(x = 620,y=40)
    Label(frame, text = f"Net Profit of the Week: {net_profit_weekly}", font = ("Arial", 13)).place(x = 620,y=60)
    Label(frame, text = "NET PROFIT FORMULA: ", font = ("Arial", 15)).place(x = 500,y=120)
    Label(frame, text = f"TOTAL SALES = {total_sales_weekly}", font = ("Arial", 12)).place(x = 500,y=160)
    Label(frame, text = f"TOTAL EXPENSES = {total_expense_per_week_from_text} ", font = ("Arial", 12)).place(x = 500,y=180)
    Label(frame, text = "GROSS PROFIT = TOTAL SALES - TOTAL SALES(30%) ", font = ("Arial", 12)).place(x = 500,y=200)
    Label(frame, text = "NET PROFIT = GROSS PROFIT - TOTAL EXPENSES ", font = ("Arial", 12)).place(x = 500,y=220)
    
    Label(frame, text = f"GROSS PROFIT = {total_sales_weekly} - {without_mark_up} = {gross_profit_weekly} ", font = ("Arial", 12)).place(x = 500,y=260)
    Label(frame, text = f"GROSS PROFIT =", font = ("Arial", 12)).place(x = 500,y=280)
    Label(frame, text = f"{gross_profit_weekly}", font = ("Arial", 12,'bold')).place(x = 630,y=280)
    Label(frame, text = f"NET PROFIT = {gross_profit_weekly} - {total_expense_per_week_from_text} = {net_profit_weekly} ", font = ("Arial", 12)).place(x = 500,y=300)
    Label(frame, text = f"NET PROFIT =", font = ("Arial", 12)).place(x = 500,y=320)
    Label(frame, text = f"{net_profit_weekly}", font = ("Arial", 12,'bold')).place(x = 620,y=320)
    Button(frame, text = "Weekly Expenses", bd = 1, command = lambda: weekly_expenses(current_month,current_week,current_year)).place(x = 50,y = 10)
    label_sales = Label(frame, text="\u2190", font=("Arial", 25), fg="blue")
    label_sales.place(x = 0,y=0)
    Button(frame,text = "Sales History",bd = 1,command = choose_month_weekly_report).place(x=150,y=10)
    global window
    window = "\u2190,daily_report"
    # Use the bind method to bind the click event to the label
    label_sales.bind("<Button-1>", label_clicked)
    label_sales.bind("<Enter>", label_enter)
    label_sales.bind("<Leave>", label_leave)

fromWeeklyReport,fromAutoWeeklyReport,fromChooseYearWeekly = False,False,False
def weekly_report():
    global selected_month,selected_day_weekly,my_listbox5,week_1_5,selected_month_weekly,selected_week,selected_year_weekly,dic,selected
    global fromWeeklyReport,fromAutoWeeklyReport,fromChooseYearWeekly
    fromAutoWeeklyReport = False
    fromWeeklyReport = True
    if fromChooseYearWeekly == True:
        try:
            selected_weekly_report = my_listbox5.curselection()
            my_listbox5 = my_listbox5
            
            selected_weekly_report = str(selected_weekly_report).replace(",)","").replace("(","")
        except Exception as e:
            print(e,"weekly_report")
            selected_weekly_report = selected_weekly_report
     
        d = {}
        
        for i in range(20):
            all_year.append(i)
        for i in range(len(all_year)):
            d[i] = all_year[i]
        
        selected_year_weekly = d[int(selected_weekly_report)]
        fromChooseYearWeekly = False
    else:
        selected_year_weekly = selected_year_weekly
        
    win.destroy()
    item_name = file_opener()
    item_name_archive_text = file_opener_archive()
    
    item_name_list,selling_price_list = [],[]
    for i in range(len(item_name)):
        item_name_list.append(item_name[i])
        selling_price_list.append(selling_price[i])
    for i in range(len(item_name_archive_text)):
        item_name_list.append(item_name_archive_text[i])
        selling_price_list.append(selling_price_archive_text[i])
    clear()
    root.geometry("950x500")
    Label(frame, text = "WEEKLY SALES", font = ("Arial", 20, 'bold')).pack(pady=15)
  
    mainframe = Frame(frame)
    mainframe.pack(fill = 'both', expand= 0)
    root.title('InventoProfit')
    widest = 0
    for i in range(len(item_name_list)):
        total_sales_daily.append(0)
        if len(item_name_list[i]) > widest:
            widest = len(item_name_list[i])
        else:
            widest = widest
    canvas = Canvas(frame)
    scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.config(yscrollcommand=scrollbar.set)
    canvas.pack(fill=BOTH, expand=1)
    frame1 = Frame(canvas)
    canvas.create_window((0, 0), window=frame1, anchor=NW)
 
    item_name_pref, sales_quantity, date, _time, fields = [],[],[],[],[]
    file = open("./texts/items_preferences.txt", 'r')
    lines = file.readlines()
    file.close()
    for x in lines:
        fields = x.split(",")
        item_name_pref.append(fields[0])
        sales_quantity.append(int(fields[1]))
        date.append(fields[2])
        _time.append(fields[3].replace("\n",""))
    dic_for_selling_price = {}
    dic_for_total_sales_each_day = {}
    for i in range(len(dic[selected_week])):
        dic_for_total_sales_each_day[dic[selected_week][i]] = 0
        
    holder_sales_each_item = []
    holder_sales_each_day = []
    total_sales_per_day = []
    total_sales_weekly= 0
    net_profit_weekly = 0
    for i in range(len(item_name_list)):
        dic_for_selling_price[item_name_list[i]] = selling_price_list[i]
    day = []
    year =[]
    month = []
    for i in range(len(item_name_pref)):
        x = date[i].split(":")
        day.append(x[1])
        year.append(x[2])
        month.append(x[0])
        holder_sales_each_item.append(0)
        holder_sales_each_day.append(0)
   
    
    for i in range(len(dic[selected_week])):
        total_sales_per_day.append(0)
    for i in range(len(item_name_pref)):
        for j in range(len(item_name_list)):
            try:
                if (item_name_pref[i] == item_name_list[j]) and int(day[i]) in dic[selected_week] and int(year[i]) == int(selected_year_weekly) and str(month[i]) == str(selected_month_weekly):
                    
                    holder_sales_each_item[i] = sales_quantity[i]*dic_for_selling_price[item_name_pref[i]]
                    for k in range(len(dic[selected_week])):
                        if day[i] == dic[selected_week][k]:
                            holder_sales_each_day[i] = dic_for_selling_price[item_name_pref[i]]*sales_quantity[i]
            except Exception as e:
                print(e)
    for i in range(len(item_name_pref)):
        for j in range(len(dic[selected_week])):
            if int(day[i]) == dic[selected_week][j] and int(year[i]) == int(selected_year_weekly) and (month[i] == selected_month_weekly):
                
                holder_sales_each_day[i] = dic_for_selling_price[item_name_pref[i]]*sales_quantity[i]
                dic_for_total_sales_each_day[dic[selected_week][j]]+=holder_sales_each_day[i]
                    
    for i in range(len(holder_sales_each_item)):
        total_sales_weekly +=holder_sales_each_item[i]
    
    def label_sort(i,j,padx,padx1):
        if j==0:
            if i == 0:
                text.grid(row = 0, column=0,padx=15)
            label.grid(row=i,column=0,padx = padx,pady = 10)
        elif j==1:
            if i == 0:
                text1.grid(row = 0, column=1,padx = 40)
            label1.grid(row=i,column=1,padx = padx1,pady = 10)
       
 
    
    for i in range(len(dic[selected_week])):
        for j in range(2):
            
            
            text=Label(mainframe, text=' DATE', font=('Arial', 15,'bold'))
            text1=Label(mainframe, text=' TOTAL SALES', font=('Arial', 15,'bold'))
            
            label = Label(frame1,text = f"Day:{dic[selected_week][i]}", font = ("Arial",15),wraplength = 70)
            label1 = Label(frame1,text = f"{'%.2f'%dic_for_total_sales_each_day[dic[selected_week][i]]}", font = ("Arial",15),wraplength = 130)
          
            
            if widest < 3 :
                label_sort(i,j,20,20) 
            elif widest > 2 and widest < 5:
                label_sort(i,j,20,20)
            elif widest > 4 and widest < 7:
                label_sort(i,j,20,20)
            elif widest > 6 and widest < 9:
                label_sort(i,j,20,20)
            else:
                label_sort(i,j,20,20)
    
    lines,fields,expense_list_from_text,expense_from_text,date = [],[],[],[],[]
    file = open("./texts/weekly_expense_list.txt",'r')
    lines = file.readlines()
    file.close()
    for x in lines:
        fields = x.split(",")
        expense_list_from_text.append(fields[0])
        expense_from_text.append(fields[1])
        date.append(str(fields[2].replace("\n","")))
    week_field = []
    
    week_field = selected_week.split(":")
    selected_week_for_comparison = week_field[0].replace(" ","")
    current_date = f"{selected_month_weekly}:{selected_week_for_comparison}:{selected_year_weekly}"
    total_expense_per_week_from_text = 0
    for i in range(len(date)):
        if date[i] == current_date:
            total_expense_per_week_from_text+=float(expense_from_text[i])
    
    
    without_mark_up = total_sales_weekly*.3
    gross_profit_weekly = total_sales_weekly - without_mark_up
    net_profit_weekly = float(gross_profit_weekly) - float(total_expense_per_week_from_text)
    total_expense_per_week_from_text = str('%.2f'%total_expense_per_week_from_text)
    net_profit_weekly = str('%.2f'%net_profit_weekly)
    without_mark_up = str('%.2f'%without_mark_up)
    total_sales_weekly = str('%.2f'%total_sales_weekly)
    gross_profit_weekly = str('%.2f'%gross_profit_weekly)
    frame1.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    
    
    
    Label(frame, text = f"Date: {selected_month_weekly}:{selected_week}:{selected_year_weekly}", font = ("Arial", 13)).place(x = 620,y=20)
    Label(frame, text = f"Total Sales of the Week: {total_sales_weekly}", font = ("Arial", 13)).place(x = 620,y=40)
    Label(frame, text = f"Net Profit of the Week: {net_profit_weekly}", font = ("Arial", 13)).place(x = 620,y=60)
    Label(frame, text = "NET PROFIT FORMULA: ", font = ("Arial", 15)).place(x = 500,y=120)
    Label(frame, text = f"TOTAL SALES = {total_sales_weekly}", font = ("Arial", 12)).place(x = 500,y=160)
    Label(frame, text = f"TOTAL EXPENSES = {total_expense_per_week_from_text} ", font = ("Arial", 12)).place(x = 500,y=180)
    Label(frame, text = "GROSS PROFIT = TOTAL SALES - TOTAL SALES(30%) ", font = ("Arial", 12)).place(x = 500,y=200)
    Label(frame, text = "NET PROFIT = GROSS PROFIT - TOTAL EXPENSES ", font = ("Arial", 12)).place(x = 500,y=220)
    
    Label(frame, text = f"GROSS PROFIT = {total_sales_weekly} - {without_mark_up} = {gross_profit_weekly} ", font = ("Arial", 12)).place(x = 500,y=260)
    Label(frame, text = f"GROSS PROFIT =", font = ("Arial", 12)).place(x = 500,y=280)
    Label(frame, text = f"{gross_profit_weekly}", font = ("Arial", 12,'bold')).place(x = 630,y=280)
    Label(frame, text = f"NET PROFIT = {gross_profit_weekly} - {total_expense_per_week_from_text} = {net_profit_weekly} ", font = ("Arial", 12)).place(x = 500,y=300)
    Label(frame, text = f"NET PROFIT =", font = ("Arial", 12)).place(x = 500,y=320)
    Label(frame, text = f"{net_profit_weekly}", font = ("Arial", 12,'bold')).place(x = 620,y=320)
    Button(frame, text = "Weekly Expenses", bd = 1, command = lambda: weekly_expenses(selected_month_weekly,selected_week,selected_year_weekly)).place(x = 50,y = 10)
    label_sales = Label(frame, text="\u2190", font=("Arial", 25), fg="blue")
    label_sales.place(x = 0,y=0)
    Button(frame,text = "Sales History",bd = 1,command = choose_month_weekly_report).place(x=150,y=10)
    global window
    window = "\u2190,daily_report"
    # Use the bind method to bind the click event to the label
    label_sales.bind("<Button-1>", label_clicked)
    label_sales.bind("<Enter>", label_enter)
    label_sales.bind("<Leave>", label_leave)


def weekly_expenses(selected_month_weekly,selected_week,selected_year_weekly):
    user_role = define_user_role()
    if user_role == 'admin':
            
        global win, frame_win,expense_list,expense_amount,expense_list
        lines,fields,expense_from_text,date,expense_list_from_text = [],[],[],[],[]
        
        file = open("./texts/weekly_expense_list.txt",'r')
        lines = file.readlines()
        file.close()
        
        for x in lines:
            fields = x.split(",")
            expense_list_from_text.append(fields[0])
            expense_from_text.append(fields[1])
            date.append(str(fields[2].replace("\n","")))
        
        week_field = []
        week_field = selected_week.split(":")
        selected_week_for_comparison = week_field[0].replace(" ","")
        current_date = f"{selected_month_weekly}:{selected_week_for_comparison}:{selected_year_weekly}"
        current_expense_list,current_expense,current_date_2 = [],[],[]
        
        for i in range(len(date)):
            if str(date[i]) == str(current_date):
                current_expense.append(expense_from_text[i])
            
        print(expense_list,current_expense,d)
        for i in range(len(expense_list)):
            d[expense_list[i]] =current_expense[i] 
        
        
        global item_name
        item_name = file_opener()
        win = Tk()
        win.title('InventoProfit')
        win.geometry('400x500')
        win.attributes('-topmost', True)
        win.resizable(False,False)
        frame_win = Frame(win)
        frame_win.pack(fill = BOTH,expand = 1)
        mainframe = Frame(frame_win)
        mainframe.pack(fill = 'both', expand= 0)
        root.title('InventoProfit')
        canvas = Canvas(frame_win)
        scrollbar = Scrollbar(frame_win, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.config(yscrollcommand=scrollbar.set)
        canvas.pack(fill=BOTH, expand=1)
        frame1 = Frame(canvas)
        canvas.create_window((0, 0), window=frame1, anchor=NW)
        
        def create_button(i):
            global expense_list
            global button
            button = Button(frame1, text=f"{expense_list[i]}", font = ("Arial", 15),bd = 1,command=lambda: input_user(i))
            button.grid(row = i, column = 0,pady=10)
            for j in range(len(expense_list)):
                for k in range(2):
                    if j == 0:
                        Label(mainframe,text = f"  LIST 	        EXPENSES",font = ("Arial", 15)).grid(row = j)
                    Label(frame1,text = f"{d[expense_list[i]]}",font = ("Arial", 15),bd = 1).grid(row = i, column = 1,pady=10,padx=40)
        for i in range(len(expense_list)):
            create_button(i)
        def input_user(i):
            clear_win()
            win.geometry("450x120")
            win.attributes('-topmost', True)
            win.resizable(False,False)
            label = Label(frame_win, text = f"{expense_list[i].title()} Week Expenses", font = ("Arial", 20))
            label.pack()
            text = Text(frame_win, width = 20, height = 1)
            text.pack(pady = 5)
            def handle_keypress(event):
                if event.keysym == "Return":
                    return "break"  # Prevents the default behavior of the Enter key
                else:
                    # Perform any other desired actions
                    pass
            text.bind("<KeyPress>", handle_keypress)
            def gets_expenses():
                global expenses,monthly_earnings,months_lists,fromAutoWeeklyReport,fromWeeklyReport
                global sales_per_month,expense_list,year_start_weekly,expense_from_text,d
                nonlocal i,current_expense,current_date
                year_start_weekly = 2023
                expenses = text.get(1.0,"end-1c")  
                try:       
                    expenses =  float(expenses)
                    
                    text_weekly_expense_list_edit(expenses,current_expense[i],current_date,expense_list[i])
                    if fromWeeklyReport == True and fromAutoWeeklyReport == False:
                        weekly_report()
                    elif fromWeeklyReport == False and fromAutoWeeklyReport == True:
                        auto_weekly_report()
                    win.destroy()
                except Exception as e:
                    print(e,"weekly_expenses")
                    handler = f"could not convert string to float: '{expense_from_text}'"
                    e = str(e)
                    if handler == e:
                        tkinter.messagebox.showinfo("ERROR",  "Input Must Be NUMBER!")
                        input_user(i)         
            but_done = Button(frame_win, text = "Done",bd = 3, font = ("Arial",15), command = gets_expenses)
            but_done.pack() 
        frame1.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
    else:
        tkinter.messagebox.showinfo("NOTICE","ONLY ADMIN CAN ACCESS")
fromSeeArchive = False
def file_opener_text():
    global date_archive_text1,item_name_archive_text1,unit_archive_text1,quantity_archive_text1,critical_value_archive_text1,orig_price_archive_text1,mark_up_archive_text1,selling_price_archive_text1
    fields,date_archive_text1,item_name_archive_text1,unit_archive_text1,quantity_archive_text1,critical_value_archive_text1,orig_price_archive_text1,mark_up_archive_text1,selling_price_archive_text1= [],[],[],[],[],[],[],[],[]
    
    
    file = open("./texts/items_archive.txt", 'r')
    lines = file.readlines()
    file.close()
    for x in lines:
        fields = x.split(",")
        date_archive_text1.append(fields[0])
        item_name_archive_text1.append(fields[1])
        unit_archive_text1.append(fields[2])
        quantity_archive_text1.append(int(fields[3]))
        critical_value_archive_text1.append(float(fields[4]))
        orig_price_archive_text1.append(float(fields[5]))
        mark_up_archive_text1.append(float(fields[6]))
        selling_price_archive_text1.append(float(fields[7]))
    return item_name_archive_text1
def file_open_see_archive():
    global fromArchive,my_listbox,names,item_name_archive,win,item_archive,fromSeeArchive,fromMainMenu,fromAdd
    fields,date_archive_text1,item_name_archive_text1,unit_archive_text1,quantity_archive_text1,critical_value_archive_text1,orig_price_archive_text1,mark_up_archive_text1,selling_price_archive_text1= [],[],[],[],[],[],[],[],[]
    
    
    file = open("./texts/items_archive.txt", 'r')
    lines = file.readlines()
    file.close()
    for x in lines:
        fields = x.split(",")
        date_archive_text1.append(fields[0])
        item_name_archive_text1.append(fields[1])
        unit_archive_text1.append(fields[2])
        quantity_archive_text1.append(int(fields[3]))
        critical_value_archive_text1.append(float(fields[4]))
        orig_price_archive_text1.append(float(fields[5]))
        mark_up_archive_text1.append(float(fields[6]))
        selling_price_archive_text1.append(float(fields[7]))
  
    selected_file_open_see_archive = my_listbox.curselection()
    if len(selected_file_open_see_archive) > 0:
        index = selected_file_open_see_archive[0]
        item_archive = my_listbox.get(index)#
        src_path = f"./ARCHIVED_ITEMS/{item_archive}.png"
        dst_path = "./QR_CODES/"
        
        try:
            shutil.move(src_path, dst_path)
        except:
            print("The PNG image file exists.")
        my_listbox.delete(index)
        names.remove(item_archive)
        
    file = open("./texts/items_archive.txt", 'w')
    file.write("")
    file.close()
    
    for i in range(len(item_name_archive_text1)):
        if item_name_archive_text1[i] in names:
            file = open("./texts/items_archive.txt", 'a')
            file.write(f"{date_archive_text1[i]},{item_name_archive_text1[i]},{unit_archive_text1[i]},{quantity_archive_text1[i]},{critical_value_archive_text1[i]},{orig_price_archive_text1[i]},{mark_up_archive_text1[i]},{selling_price_archive_text1[i]}\n")
            file.close()
        else:
            file = open("./texts/items_name_price_stock.txt", 'a')
            file.write(f"{date_archive_text1[i]},{item_name_archive_text1[i]},{unit_archive_text1[i]},{quantity_archive_text1[i]},{critical_value_archive_text1[i]},{orig_price_archive_text1[i]},{mark_up_archive_text1[i]},{selling_price_archive_text1[i]}\n")
            file.close()
        
    item_name_archive_text1 = file_opener_text()
    clear()
    fromArchive,fromSeeArchive,fromAdd,fromMainMenu = False,True,False,False
    product_inventory()
    win.destroy()
    
def See_archive():
    global fromSeeArchive,fromAdd,my_listbox,names,win,frame_win,fromMainMenu
    #date_archive,item_name_archive,unit_archive,quantity_archive,critical_value_archive,orig_price_archive,mark_up_archive,selling_price_archive
    fromSeeArchive,fromMainMenu = True,False
   
    item_name_archive_text1 = file_opener_text()
 
    win = Tk()
    win.title('InventoProfit')
    win.geometry("350x120")
    win.attributes('-topmost', True)
    win.resizable(False,False)
    frame_win = Frame(win)
    frame_win.pack(fill = BOTH,expand = 1)
    canvas = Canvas(frame_win, bg = "white")
    label = Label(frame_win, text = "Item Name to Be Restored", font = ("Arial", 20))
    label.pack()
    label1 = Label(frame_win,text = "Choose an Item...", bg = "white",font = ("Courier", 10)).pack(pady=5)
    def toggle_size():
        global is_large
        if not is_large:
            win.geometry("350x400")
            is_large = True
        else:
            win.geometry("350x120")
            is_large = False
    button = Button(frame_win, text="...", font = 'bold', height = 1,relief = SUNKEN,command=toggle_size)
    button.place(x = 250,y = 42)
    but_done = Button(frame_win, text = "Done",bd = 3, font = ("Arial",15), command = file_open_see_archive)
    but_done.pack()
    canvas.pack(side = BOTTOM,expand = 1)
    scrollbar = Scrollbar(canvas)
    scrollbar.pack(side=RIGHT, fill=Y)
    my_listbox = Listbox(canvas,yscrollcommand=scrollbar.set, width = 200,height = 400,font = ("Arial",20),selectmode = SINGLE)
    names = []
    for i in range(len(item_name_archive_text1)):
        names.append(item_name_archive_text1[i])
        my_listbox.insert(END, f"{item_name_archive_text1[i]}")
    my_listbox.pack(side=LEFT)
    scrollbar.config(command=my_listbox.yview)
    win.mainloop()

def sales():
    global label_sales,name,fromScan
    clear()
    root.geometry("900x600")
    define_user_role()
    Label(frame, text = f"User Role: {user_role_}", font = ("Arial", 10)).place(x = 10,y=520)
    Label(frame, text = "INVENTOPROFIT", font = ("Arial", 20, 'bold')).pack(pady=15)
    Label(frame, text = "INVENTORY AND SALES FOR RAMIRES SUPPLIES STORE", font = ("Arial", 15, 'bold')).pack()
    Label(frame, text = f"User Account: {current_user_name}", font = ("Arial", 10)).place(x = 10,y=500)
    date_label = Label(frame, font = ("Arial", 10))
    date_label.place(x = 10, y=540)
    time_label = Label(frame, font = ("Arial", 10))
    time_label.place(x = 10, y=560)
    update_date(date_label)
    update_time(time_label) 
    Label(frame, text = "REPORTS", font = ("Arial", 15, 'bold')).place(x = 405, y = 200)
    Button(frame,text = "DAILY REPORTS", bd = 3,font = ("Arial",15),command = auto_daily_report).place(x = 90, y =240)
    
    Button(frame,text = "WEEKLY REPORTS", bd = 3,font = ("Arial",15),command = auto_weekly_report).place(x = 320, y =240)
    Button(frame,text = "MONTHLY REPORTS", bd = 3,font = ("Arial",15),command = auto_monthly_report).place(x = 570, y =240)

    label_sales = Label(frame, text="\u2190", font=("Arial", 25), fg="blue")
    label_sales.place(x = 0,y=0)
    global window
    window = "\u2190,sales"
    # Use the bind method to bind the click event to the label
    label_sales.bind("<Button-1>", label_clicked)
    label_sales.bind("<Enter>", label_enter)
    label_sales.bind("<Leave>", label_leave)
    
user_role_ = ""
def define_user_role():
    global user_role_,user_name
    file = open("./texts/accounts_lists.txt","r")
    lines = file.readlines()
    file.close()
    fields,user_role,user = [],[],[]
    for x in lines:
        fields = x.split(",")
        user.append(fields[0])
        user_role.append(fields[2].replace("\n",""))
    
    for i in range(len(user)):
        if user[i] == user_name:
            user_role_ = user_role[i]
    return user_role_

def menu_widgets(name):
    global fromSeeArchive,user_role_,role,label_menu_widgets,month,final_item_amount_,item_amount_,quantity_scan,fromScan,date_archive_cancel,item_name_archive_cancel,unit_archive_cancel,quantity_archive_cancel,critical_value_archive_cancel,orig_price_archive_cancel,mark_up_archive_cancel,selling_price_archive_cancel,fromArchive,quantity_restock,date,unit,quantity,critical_value,orig_price,mark_up,selling_price,fromRestock,current_user,fromMainMenu,fromMenu,fromAdd,date_cancel,item_name_cancel,unit_cancel,quantity_cancel,critical_value_cancel,orig_price_cancel,mark_up_cancel,selling_price_cancel
    global item_name_archive_text1,fields,date_archive_text,item_name_archive_text,unit_archive_text,quantity_archive_text,critical_value_archive_text,orig_price_archive_text,mark_up_archive_text,selling_price_archive_text
    name = name
 
        
    if fromScan == True and name == "Cancel":
        file = open("./texts/items_name_price_stock.txt",'w')
        file.write("")
        file.close()
        for i in range(len(item_name)):
            file = open(f"./texts/items_name_price_stock.txt",'a')
            file.write(f"{date[i]},{item_name[i]},{unit[i]},{quantity_scan[i]},{critical_value[i]},{orig_price[i]},{mark_up[i]},{selling_price[i]}\n")
            file.close()
    elif fromScan == True and name == "Save":
        file = open("./texts/items_name_price_stock.txt",'w')
        file.write("")
        file.close()
        for i in range(len(item_name)):
            file = open(f"./texts/items_name_price_stock.txt",'a')
            file.write(f"{date[i]},{item_name[i]},{unit[i]},{quantity[i]},{critical_value[i]},{orig_price[i]},{mark_up[i]},{selling_price[i]}\n")
            file.close()
       
    if fromRestock == True and name == "Cancel": 
        file = open("./texts/items_name_price_stock.txt",'w')
        file.write("")
        file.close()
        for i in range(len(item_name)):
            file = open(f"./texts/items_name_price_stock.txt",'a')
            file.write(f"{date[i]},{item_name[i]},{unit[i]},{quantity_restock[i]},{critical_value[i]},{orig_price[i]},{mark_up[i]},{selling_price[i]}\n")
            file.close()
    elif fromRestock == True and name == "Save":
        file = open("./texts/items_name_price_stock.txt",'w')
        file.write("")
        file.close()
        for i in range(len(item_name)):
            file = open(f"./texts/items_name_price_stock.txt",'a')
            file.write(f"{date[i]},{item_name[i]},{unit[i]},{quantity[i]},{critical_value[i]},{orig_price[i]},{mark_up[i]},{selling_price[i]}\n")
            file.close()
    
    try:
        print(item_name_archive_cancel,item_name_archive_text,item_name)
    except:
        item_name_archive_cancel,item_name_archive_text = None,None
        print(item_name_archive_cancel,item_name)
    print(f"fromArchive: {fromArchive}, fromSeeArchive:{fromSeeArchive}, menu_widgets")
    if fromArchive == True and name == "Cancel" and fromSeeArchive == False:
    
        file = open("./texts/items_name_price_stock.txt",'w')
        file.write("")
        file.close()
        file = open("./texts/items_archive.txt", 'w')
        file.write("")
        file.close()
        if item_name_archive_text != []:
            for i in range(len(item_name_archive_text)):
               
                file = open("./texts/items_archive.txt", 'a')
                file.write(f"{date_archive_text[i]},{item_name_archive_text[i]},{unit_archive_text[i]},{quantity_archive_text[i]},{critical_value_archive_text[i]},{orig_price_archive_text[i]},{mark_up_archive_text[i]},{selling_price_archive_text[i]}\n")
                file.close()
        else:
            pass
        for i in range(len(item_name_archive_cancel)):
            file = open(f"./texts/items_name_price_stock.txt",'a')
            file.write(f"{date_archive_cancel[i]},{item_name_archive_cancel[i]},{unit_archive_cancel[i]},{quantity_archive_cancel[i]},{critical_value_archive_cancel[i]},{orig_price_archive_cancel[i]},{mark_up_archive_cancel[i]},{selling_price_archive_cancel[i]}\n")
            file.close()
        folder_path = "./ARCHIVED_ITEMS/"
        file_list = os.listdir(folder_path)
        dst_path = "./QR_CODES/"
        for file_name in file_list:
            src_path = os.path.join(folder_path, file_name)
            try:
                shutil.move(src_path, dst_path)
            except:
                print("The PNG image file exists.")
    elif fromArchive == True and name == "Save" and fromSeeArchive == False:
        file = open("./texts/items_name_price_stock.txt",'w')
        file.write("")
        file.close()
        for i in range(len(item_name)):
            file = open(f"./texts/items_name_price_stock.txt",'a')
            file.write(f"{date[i]},{item_name[i]},{unit[i]},{quantity[i]},{critical_value[i]},{orig_price[i]},{mark_up[i]},{selling_price[i]}\n")
            file.close()   
        folder_path = "./ARCHIVED_ITEMS/" 
        file_list = os.listdir(folder_path)
        dst_path = "./QR_CODES/"
        for file_name in file_list:
            src_path = os.path.join(folder_path, file_name)
            try:
                shutil.move(src_path, dst_path)
            except:
                print("The PNG image file exists.")
    elif fromSeeArchive == True and name == "Cancel" and fromArchive == False:
        
        file = open("./texts/items_archive.txt", 'w')
        file.write("")
        file.close()
        file = open("./texts/items_name_price_stock.txt",'w')
        file.write("")
        file.close()
        if item_name_archive_cancel != []:
            for i in range(len(item_name_archive_cancel)):
               
                file = open(f"./texts/items_name_price_stock.txt",'a')
                file.write(f"{date_archive_cancel[i]},{item_name_archive_cancel[i]},{unit_archive_cancel[i]},{quantity_archive_cancel[i]},{critical_value_archive_cancel[i]},{orig_price_archive_cancel[i]},{mark_up_archive_cancel[i]},{selling_price_archive_cancel[i]}\n")
                file.close()
        else:
            pass
        for i in range(len(item_name_archive_text)):
            file = open("./texts/items_archive.txt", 'a')
            file.write(f"{date_archive_text[i]},{item_name_archive_text[i]},{unit_archive_text[i]},{quantity_archive_text[i]},{critical_value_archive_text[i]},{orig_price_archive_text[i]},{mark_up_archive_text[i]},{selling_price_archive_text[i]}\n")
            file.close()
        folder_path = "./ARCHIVED_ITEMS/"
        file_list = os.listdir(folder_path)
        dst_path = "./QR_CODES/"
        for file_name in file_list:
            src_path = os.path.join(folder_path, file_name)
            try:
                shutil.move(src_path, dst_path)
            except:
                print("The PNG image file exists.")
    elif fromSeeArchive == True and name == "Save"  and fromArchive == False:
        file = open("./texts/items_name_price_stock.txt",'w')
        file.write("")
        file.close()
        for i in range(len(item_name)):
            file = open(f"./texts/items_name_price_stock.txt",'a')
            file.write(f"{date[i]},{item_name[i]},{unit[i]},{quantity[i]},{critical_value[i]},{orig_price[i]},{mark_up[i]},{selling_price[i]}\n")
            file.close()   
        folder_path = "./ARCHIVED_ITEMS/" 
        file_list = os.listdir(folder_path)
        dst_path = "./QR_CODES/"
        for file_name in file_list:
            src_path = os.path.join(folder_path, file_name)
            try:
                shutil.move(src_path, dst_path)
            except:
                print("The PNG image file exists.")
    
    if fromAdd == True:
        fromMainMenu = False
    else:
        fromMainMenu = True   
    if fromMainMenu == False:
        if name == "Save":
            pass
        elif name == "Cancel":
            folder_path = "QR_CODES"  # replace with the actual path to your folder
            # use os.listdir to get a list of all files in the folder
            folder_contents = os.listdir(folder_path)
            # loop through the list and print each file name
            qr_names,file_names = [],[]
            for file_name in folder_contents:
                file_names.append(file_name)
                file_name = file_name.replace(".png","")
                qr_names.append(file_name)
            for i in range(len(file_names)):
                if qr_names[i] not in item_name_cancel:
                    os.remove(f"./QR_CODES/{file_names[i]}")
            file = open("./texts/items_name_price_stock.txt",'w')
            file.write("")
            file.close()      
            for i in range(len(item_name_cancel)):
                file = open(f"./texts/items_name_price_stock.txt",'a')
                file.write(f"{date[i]},{item_name_cancel[i]},{unit_cancel[i]},{quantity_cancel[i]},{critical_value_cancel[i]},{orig_price_cancel[i]},{mark_up_cancel[i]},{selling_price_cancel[i]}\n")
                file.close() 
    clear()
    root.geometry("900x600")
    Label(frame, text = "INVENTOPROFIT", font = ("Arial", 20, 'bold')).pack(pady=15)
    Label(frame, text = "INVENTORY AND SALES FOR RAMIRES SUPPLIES STORE", font = ("Arial", 15, 'bold')).pack()
    label_menu_widgets = Label(frame, text="LOG OUT", font=("Arial", 13), fg="blue")
    label_menu_widgets.place(x = 800,y=550)
    global window
    window = "LOG OUT,menu"
    define_user_role()
    Label(frame, text = f"User Role: {user_role_}", font = ("Arial", 10)).place(x = 10,y=520)
    # Use the bind method to bind the click event to the label
    label_menu_widgets.bind("<Button-1>", label_clicked)
    label_menu_widgets.bind("<Enter>", label_enter)
    label_menu_widgets.bind("<Leave>", label_leave)
    Label(frame, text = f"User Account: {current_user_name}", font = ("Arial", 10)).place(x = 10,y=500)
    date_label = Label(frame, font = ("Arial", 10))
    date_label.place(x = 10, y=540)
    time_label = Label(frame, font = ("Arial", 10))
    time_label.place(x = 10, y=560)
    update_date(date_label)
    update_time(time_label) 
    Button(frame,text = "SCAN ITEMS", bd = 3, font = ("Arial",15),command = lambda: multi_scan("menu_widgets")).place(x = 50, y = 200)
    Button(frame,text = "PRODUCT INVENTORY", bd = 3,font = ("Arial",15),command = product_inventory).place(x = 300, y =200)
    Button(frame,text = "SALES", bd = 3,font = ("Arial",15),command = sales).place(x = 700, y =200)
    fromRestock,fromArchive,fromAdd,fromScan,fromSeeArchive = False,False,False,False,False
    update_final_item_amount_()
    
    
def file_open_archive():
    global my_listbox,names,item_name,win,fromSeeArchive,fromArchive,fromAdd,fromMainMenu
    fields,date,item_name,unit,quantity,critical_value,orig_price,mark_up,selling_price= [],[],[],[],[],[],[],[],[]
    file = open("./texts/items_name_price_stock.txt", 'r')
    lines = file.readlines()
    file.close()
    for x in lines:
        fields = x.split(",")
        date.append(fields[0])
        item_name.append(fields[1])
        unit.append(fields[2])
        quantity.append(int(fields[3]))
        critical_value.append(float(fields[4]))
        orig_price.append(float(fields[5]))
        mark_up.append(float(fields[6]))
        selling_price.append(float(fields[7])) 
    selected_file_open_archive = my_listbox.curselection()
    if len(selected_file_open_archive) > 0:
        index = selected_file_open_archive[0]
        item_archive = my_listbox.get(index)
        src_path = f"./QR_CODES/{item_archive}.png"
        dst_path = "./ARCHIVED_ITEMS/"
        try:
            shutil.move(src_path, dst_path)
        except:
            print("The PNG image file exists.")
        
        my_listbox.delete(index)
        names.remove(item_archive)

    file = open("./texts/items_name_price_stock.txt", 'w')
    file.write("")
    file.close()

    for i in range(len(item_name)):
        if item_name[i] in names:
            file = open("./texts/items_name_price_stock.txt", 'a')
            file.write(f"{date[i]},{item_name[i]},{unit[i]},{quantity[i]},{critical_value[i]},{orig_price[i]},{mark_up[i]},{selling_price[i]}\n")
            file.close()
        else:
            file = open("./texts/items_archive.txt", 'a')
            file.write(f"{date[i]},{item_name[i]},{unit[i]},{quantity[i]},{critical_value[i]},{orig_price[i]},{mark_up[i]},{selling_price[i]}\n")
            file.close()
            
    item_name = file_opener()
    clear()
    fromSeeArchive,fromArchive,fromAdd,fromMainMenu = False,True,False,False
    product_inventory()
    win.destroy()
    
def Archive():
    global item_name,my_listbox,names,win,frame_win,fromArchive,fromMainMenu,item_name_archive
    
    fromArchive = True
    item_name = file_opener()
    win = Tk()
    win.title('InventoProfit')
    win.geometry("350x120")
    win.attributes('-topmost', True)
    win.resizable(False,False)
    frame_win = Frame(win)
    frame_win.pack(fill = BOTH,expand = 1)
    canvas = Canvas(frame_win, bg = "white")
    label = Label(frame_win, text = "Item Name to Be archived", font = ("Arial", 20))
    label.pack()
    label1 = Label(frame_win,text = "Choose an Item...", bg = "white",font = ("Courier", 10)).pack(pady=5)
    def toggle_size():
        global is_large
        if not is_large:
            win.geometry("350x400")
            is_large = True
        else:
            win.geometry("350x120")
            is_large = False
    button = Button(frame_win, text="...", font = 'bold', height = 1,relief = SUNKEN,command=toggle_size)
    button.place(x = 250,y = 42)
    but_done = Button(frame_win, text = "Done",bd = 3, font = ("Arial",15), command = file_open_archive)
    but_done.pack()
    canvas.pack(side = BOTTOM,expand = 1)
    scrollbar = Scrollbar(canvas)
    scrollbar.pack(side=RIGHT, fill=Y)
    my_listbox = Listbox(canvas,yscrollcommand=scrollbar.set, width = 200,height = 400,font = ("Arial",20),selectmode = SINGLE)
    names = []
    for i in range(len(item_name)):
        names.append(item_name[i])
        my_listbox.insert(END, f"{item_name[i]}")
    my_listbox.pack(side=LEFT)
    scrollbar.config(command=my_listbox.yview)
    win.mainloop()
item_amount_ = 0
def file_opener_archive_cancel():
    global fromMainMenu,fields,date_archive_cancel,item_name_archive_cancel,unit_archive_cancel,quantity_archive_cancel,critical_value_archive_cancel,orig_price_archive_cancel,mark_up_archive_cancel,selling_price_archive_cancel,lines
    fromMainMenu = False
    fields,date_archive_cancel,item_name_archive_cancel,unit_archive_cancel,quantity_archive_cancel,critical_value_archive_cancel,orig_price_archive_cancel,mark_up_archive_cancel,selling_price_archive_cancel= [],[],[],[],[],[],[],[],[]
    file = open("./texts/items_name_price_stock.txt", 'r')
    lines = file.readlines()
    file.close()
    for x in lines:
        fields = x.split(",")
        date_archive_cancel.append(fields[0])
        item_name_archive_cancel.append(fields[1])
        unit_archive_cancel.append(fields[2])
        quantity_archive_cancel.append(int(fields[3]))
        critical_value_archive_cancel.append(float(fields[4]))
        orig_price_archive_cancel.append(float(fields[5]))
        mark_up_archive_cancel.append(float(fields[6]))
        selling_price_archive_cancel.append(float(fields[7]))  
    return item_name_archive_cancel
def product_inventory():
    global fromSeeArchive,critical_value, user_name,item_amount_,quantity_scan,win,date_archive_cancel,item_name_archive_cancel,unit_archive_cancel,quantity_archive_cancel,critical_value_archive_cancel,orig_price_archive_cancel,mark_up_archive_cancel,selling_price_archive_cancel,fromArchive,fromRestock,quantity_restock,name,current_user_name,current_time,month,fromMainMenu,item_name_cancel,fromAdd,date_cancel,item_name_cancel,unit_cancel,quantity_cancel,critical_value_cancel,orig_price_cancel,mark_up_cancel,selling_price_cancel,name
    global item_name_archive_text1,date_archive_text,item_name_archive_text,unit_archive_text,quantity_archive_text,critical_value_archive_text,orig_price_archive_text,mark_up_archive_text,selling_price_archive_text
    if (fromMainMenu == True and fromAdd == False) or (fromMainMenu == False and fromAdd == False):
        item_name = file_opener() 
        date_cancel,item_name_cancel,unit_cancel,quantity_cancel,critical_value_cancel,orig_price_cancel,mark_up_cancel,selling_price_cancel = date,item_name,unit,quantity,critical_value,orig_price,mark_up,selling_price
    if (fromMainMenu == True and fromRestock == False) or (fromMainMenu == False and fromRestock == False) or fromAdd == True:
        item_name = file_opener() 
        quantity_restock = quantity
 
    if (fromMainMenu == True and fromScan == False) or (fromMainMenu == False and fromScan == False) or fromAdd == True:
        item_name = file_opener() 
        quantity_scan = quantity
    
    if (fromMainMenu == True and fromArchive == False and fromSeeArchive == False) or (fromMainMenu == False and fromArchive == False and fromSeeArchive == False) or fromAdd == True:
        item_name_archive_cancel = file_opener_archive_cancel()
        item_name_archive_text = file_opener_archive()
        
        date_archive_text,item_name_archive_text,unit_archive_text,quantity_archive_text,critical_value_archive_text,orig_price_archive_text,mark_up_archive_text,selling_price_archive_text=date_archive_text,item_name_archive_text,unit_archive_text,quantity_archive_text,critical_value_archive_text,orig_price_archive_text,mark_up_archive_text,selling_price_archive_text
        date_archive_cancel,item_name_archive_cancel,unit_archive_cancel,quantity_archive_cancel,critical_value_archive_cancel,orig_price_archive_cancel,mark_up_archive_cancel,selling_price_archive_cancel = date_archive_cancel,item_name_archive_cancel,unit_archive_cancel,quantity_archive_cancel,critical_value_archive_cancel,orig_price_archive_cancel,mark_up_archive_cancel,selling_price_archive_cancel
        
    elif (fromMainMenu == True and fromArchive == True and fromSeeArchive == True) or (fromMainMenu == False and fromArchive == True and fromSeeArchive == True) or fromAdd == True:
        item_name_archive_cancel = file_opener_archive()
        item_name_archive_text = file_opener_archive_cancel()
        date_archive_cancel,item_name_archive_cancel,unit_archive_cancel,quantity_archive_cancel,critical_value_archive_cancel,orig_price_archive_cancel,mark_up_archive_cancel,selling_price_archive_cancel =date_archive_text,item_name_archive_text,unit_archive_text,quantity_archive_text,critical_value_archive_text,orig_price_archive_text,mark_up_archive_text,selling_price_archive_text
        date_archive_text,item_name_archive_text,unit_archive_text,quantity_archive_text,critical_value_archive_text,orig_price_archive_text,mark_up_archive_text,selling_price_archive_text=date_archive_cancel,item_name_archive_cancel,unit_archive_cancel,quantity_archive_cancel,critical_value_archive_cancel,orig_price_archive_cancel,mark_up_archive_cancel,selling_price_archive_cancel
        
    item_name = file_opener()
    item_name_archive_text1 = file_opener_text()
    clear()
    root.geometry("1590x600")
    Label(frame, text = "INVENTOPROFIT", font = ("Arial", 20, 'bold')).pack(pady=15)
    Label(frame, text = "INVENTORY AND SALES FOR RAMIRES SUPPLIES STORE", font = ("Arial", 15, 'bold')).pack()
    Label(frame, text = "PRODUCT INVENTORY", font = ("Arial", 15, 'bold')).pack(pady=5)
    current_month = month_determine(current_time)
    Label(frame, text = f"User Account: {current_user_name}", font = ("Arial", 15)).place(x = 10,y=10)
    Label(frame, text = f"Date: {current_month}-{current_time.day}-{current_time.year}", font = ("Arial", 15)).place(x = 10,y=40)
    mainframe = Frame(frame)
    mainframe.pack(fill = 'both', expand= 0)
    root.title('InventoProfit')
    widest = 0
    for i in range(len(item_name)):
        if len(item_name[i]) > widest:
            widest = len(item_name[i])
        else:
            widest = widest
    canvas = Canvas(frame)
    scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.config(yscrollcommand=scrollbar.set)
    canvas.pack(fill=BOTH, expand=1)
    frame1 = Frame(canvas)
    canvas.create_window((0, 0), window=frame1, anchor=NW)
    texts = ['DATE','QR CODE','ITEM NAME','UNITS','QUANTITY','CRITICAL VALUE','ORIGINAL PRICE','MARK UP(%)','SELLING PRICE']
    update_quantity_cancel = []
    for i in range(len(item_name)):
        update_quantity_cancel
    def label_sort(j,i,padx1,padx2,padx3,padx4,padx5,padx6,padx7,padx8):
        if j==0:
            if i == 0:
                text.grid(row = 0, column=0)
            label.grid(row=i,column=0,pady = 10)
        elif j==1:
            if i == 0:
                text1.grid(row = 0, column=1,padx = 30)
            label1.grid(row=i,column=1,padx = padx1,pady = 10)
        elif j==2:
            if i == 0:
                text2.grid(row = 0, column=2,padx = 10)
            label2.grid(row=i,column=2,padx=padx2,pady = 10)
        elif j==3:
            if i == 0:
                text3.grid(row = 0, column=3,padx = 30)
            label3.grid(row=i,column=3,padx = padx3,pady = 10)
        elif j==4:
            if i == 0:
                text4.grid(row = 0, column=4,padx = 15)
            label4.grid(row=i,column=4,padx = padx4,pady = 10)
        elif j==5:
            if i == 0:
                item_amount_text.grid(row = 0, column=5,padx = 30)
            label5.grid(row=i,column=5,padx = padx5,pady = 10)
        elif j==6:
            if i == 0:
                text6.grid(row = 0, column=6,padx = 30)
            label6.grid(row=i,column=6,padx = padx6,pady = 10)
        elif j==7:
            if i == 0:
                text7.grid(row = 0, column=7,padx = 30)
            label7.grid(row=i,column=7,padx = padx7,pady = 10)
        elif j==8:
            if i == 0:
                text8.grid(row = 0, column=8,padx = 30)
            label8.grid(row=i,column=8,padx = padx8,pady = 10)
        
    for i in range(len(item_name)):
        for j in range(9):
            image = Image.open(f"./QR_CODES/{item_name[i]}.png")
            image = image.resize((100, 100))
            text = Label(mainframe, text='DATE', font=('Arial', 15,'bold'))
            text1=Label(mainframe, text='  QR CODE', font=('Arial', 15,'bold'))
            text2=Label(mainframe, text=' ITEM NAME', font=('Arial', 15,'bold'))
            text3=Label(mainframe, text=' UNITS', font=('Arial', 15,'bold'))
            text4=Label(mainframe, text=' QUANTITY', font=('Arial', 15,'bold'))
            item_amount_text=Label(mainframe, text=' CRITICAL VALUE', font=('Arial', 15,'bold'))
            text6=Label(mainframe, text=' ORIGINAL PRICE', font=('Arial', 15,'bold'))
            text7=Label(mainframe, text=' MARK UP(%)', font=('Arial', 15,'bold'))
            text8=Label(mainframe, text=' SELLING PRICE', font=('Arial', 15,'bold'))
            tk_image = ImageTk.PhotoImage(image)
            label1 = Label(frame1, image=tk_image)
            label = Label(frame1,text = f"{date[i]}", font = ("Arial",15),wraplength = 70) 
            label1.image = tk_image
            label2 = Label(frame1,text = f"{item_name[i]} ", font = ("Arial",15),wraplength = 130) 
            label3= Label(frame1,text = f"{unit[i]}" , font = ("Arial",15),wraplength = 70)
            label4 = Label(frame1,text = f"{quantity[i]}", font = ("Arial",15),wraplength = 70)
            label5= Label(frame1,text = f"{int(critical_value[i])}", font = ("Arial",15),wraplength = 70)
            label6 = Label(frame1,text = f"{orig_price[i]}php", font = ("Arial",15),wraplength = 130)
            label7= Label(frame1,text = f"{mark_up[i]}%", font = ("Arial",15),wraplength = 70)
            label8 = Label(frame1,text = f"{selling_price[i]}php", font = ("Arial",15),wraplength = 130)
            if widest < 3 :
                label_sort(j,i,30,40,60,30,90,100,80,30) 
            elif widest > 2 and widest < 5:
                label_sort(j,i,30,30,60,15,105,90,80,40)
            elif widest > 4 and widest < 7:
                label_sort(j,i,30,20,50,25,105,90,80,40)
            elif widest > 6 and widest < 9:
                label_sort(j,i,30,20,40,35,105,80,80,40)
            else:
                label_sort(j,i,10,40,15,55,90,95,45,100)
    frame1.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    file = open("./texts/accounts_lists.txt","r")
    lines = file.readlines()
    file.close()
    user_name_list,fields= [],[]
    for x in lines:
        fields = x.split(",")
        user_name_list.append(fields[0])
    for i in range(len(user_name_list)):
        if user_name_list[i] == user_name:           
            if role[i] == "admin":
                Button(frame, text = "Add", font = ("Arial", 15),bd = 3,command = Add).place(x =106,y=70)
                Button(frame, text = "Restock", font = ("Arial", 15),bd = 3,command = Restock).place(x = 165,y=70)
                Button(frame, text = "Archive", font = ("Arial", 15),bd = 3,command = Archive).place(x = 260,y=70)
                Button(frame, text = "See Archive", font = ("Arial", 15),bd = 3,command = See_archive).place(x = 365,y=70)
            else:
                Button(frame, text = "Add", font = ("Arial", 15),bd = 3,command = pop_info).place(x =106,y=70)
                Button(frame, text = "Restock", font = ("Arial", 15),bd = 3,command = pop_info).place(x = 165,y=70)
                Button(frame, text = "Archive", font = ("Arial", 15),bd = 3,command = pop_info).place(x = 260,y=70)
                Button(frame, text = "See Archive", font = ("Arial", 15),bd = 3,command = pop_info).place(x = 365,y=70)
    Button(frame, text = "Scan", font = ("Arial", 15),bd = 3,command = lambda: multi_scan("product_inventory")).place(x = 10,y=70)
    name = ["Save", "Cancel"]
    x = 0
    for name in name:
        button = Button(frame,text = name,font = ("Arial", 15),bd = 3,command = lambda name = name: menu_widgets(name))
        if name == "Save":
            x = 1400
        elif name == "Cancel":
            x = 1470
        button.place(x=x,y=10)
    for i in range(len(item_name)):
        if quantity[i] == critical_value[i] or quantity[i] <= critical_value[i]:
            tkinter.messagebox.showinfo("NOTICE",f"{item_name[i]} Reached Its Critical Value")
            
def pop_info():
    tkinter.messagebox.showinfo("NOTICE", "Only Admin Can Access Here")
is_large = False
def qr_generator(name):
    qr = pyqrcode.create(name)
    qr.png(f"./QR_CODES/{name}.png", scale = 6)
def gets_name():
    global win,text1,text,item_name1,frame_win
    item_name,item_name_archive,fields = [],[],[]
    file = open("./texts/items_name_price_stock.txt", 'r')
    lines = file.readlines()
    file.close()
    
    for x in lines:
        fields = x.split(",")
        item_name.append(fields[1])
    file = open("./texts/items_archive.txt", 'r')
    lines = file.readlines()
    file.close()
    
    for x in lines:
        fields = x.split(",")
        item_name_archive.append(fields[1])
    
    try:
        try:
            item_name1 = text.get(1.0, "end-1c")
            
        except Exception as e:
            print(e,"gets_name")
            item_name1 = item_name1
            
        clear_win()
        win.geometry("640x120")
        text1 = Text(frame_win, width = 20, height = 1)
        
        if item_name1 in item_name:
            win.destroy()
            tkinter.messagebox.showinfo("NOTICE",  f"{item_name1} Already In The List")
            Add()
        elif item_name1 in item_name_archive:
            win.destroy()
            tkinter.messagebox.showinfo("NOTICE",  f"{item_name1} Already In The Archive")
            Add()
        else:     
            if item_name1 == "" or item_name1 == "Input an Item":
                win.destroy()
                tkinter.messagebox.showinfo("NOTICE", "Empty Input")
                Add()
            else:
                clear_win()
                win.geometry("640x120")
                label = Label(frame_win, text = f"Supplier Price of {item_name1} In Pesos", font = ("Arial", 20))
                label.pack()
                text1 = Text(frame_win, width = 20, height = 1)
                text1.pack(pady = 5)
                if item_name1 not in item_name and item_name1 != "":
                    but_done = Button(frame_win, text = "Done",bd = 3, font = ("Arial",15), command =  gets_price)
                    but_done.pack()
                else:
                    but_done = Button(frame_win, text = "Done",bd = 3, font = ("Arial",15), command =  gets_name)
                    but_done.pack()    
    except Exception as e:
        
        e = str(e)
        print(e,"gets_name")
        if e == 'invalid command name ".!frame.!text"' or e == "can't invoke \"destroy\" command: application has been destroyed":
            print(e,"gets_name")
            gets_name()
    def handle_keypress(event):
        if event.keysym == "Return":
            return "break"  # Prevents the default behavior of the Enter key
        else:
            # Perform any other desired actions
            pass
    text1.bind("<KeyPress>", handle_keypress)
    def on_enter_press(event):
        gets_price()
    text1.bind("<Return>", on_enter_press)

    
def gets_price():
    global win,text3,text1,supplier_price,frame_win,item_name1
    try:
        supplier_price = text1.get(1.0, "end-1c")
    except:
        supplier_price = supplier_price
        
    clear_win()
    win.geometry("500x120")
    if supplier_price != "":  
        try:
            supplier_price = float(supplier_price)
            clear_win()
            win.geometry("500x120")
            label = Label(frame_win, text = f"Quantity of {item_name1}", font = ("Arial", 20))
            label.pack() 
            text3 = Text(frame_win, width = 20, height = 1)
            text3.pack(pady = 5)  
            but_done = Button(frame_win, text = "Done",bd = 3, font = ("Arial",15), command = gets_stock)
            but_done.pack()
            def handle_keypress(event):
                if event.keysym == "Return":
                    return "break"  # Prevents the default behavior of the Enter key
                else:
                    # Perform any other desired actions
                    pass

            text3.bind("<KeyPress>", handle_keypress)
            def on_enter_press(event):
                gets_stock()
            text3.bind("<Return>", on_enter_press)
           
        except Exception as e:
            print(e,"gets_price")
            handler = f"could not convert string to float: '{supplier_price}'"
            e = str(e)
            if handler == e:
                tkinter.messagebox.showinfo("ERROR",  "Input Must Be NUMBER!")
                gets_name()
    else:
        tkinter.messagebox.showinfo("ERROR",  "Empty Input!")
        
        gets_name()
def gets_stock():
    global win,my_listbox,text3,units,stock,frame_win,item_name1
    
    try:
        stock = text3.get(1.0, "end-1c")
    except:
        if type(stock) != str:
            stock = stock
        else:
            stock = "1"
    clear_win()
    win.geometry("450x120")
    if stock != "":
        try: 
            stock = int(stock)
            clear_win()
            win.geometry("450x120")
            canvas1 = Canvas(frame_win, bg = "white")
            label = Label(frame_win, text = f"Unit of {item_name1}", font = ("Arial", 20))
            label.pack()
            label1 = Label(frame_win,text = "Choose an Item...", bg = "white",font = ("Courier", 10)).pack(pady=5)
            def toggle_size():
                global is_large
                if not is_large:
                    win.geometry("450x400")
                    is_large = True
                else:
                    win.geometry("450x120")
                    is_large = False
            
            button = Button(frame_win, text="...", font = 'bold', height = 1,relief = SUNKEN,command=toggle_size)
            button.place(x = 300,y = 42)
            scrollbar = Scrollbar(canvas1)
            my_listbox,units,names = Listbox(canvas1,yscrollcommand=scrollbar.set, width = 200,height = 400,font = ("Arial",20),selectmode = SINGLE),["pieces","dozens","cases"],[]
            for i in range(len(units)):
                names.append(units[i])
                my_listbox.insert(END, f"{units[i]}")
            my_listbox.pack(side=LEFT)
            but_done = Button(frame_win, text = "Done",bd = 3, font = ("Arial",15),command =  gets_unit)
            but_done.pack() 
            canvas1.pack(side = BOTTOM,expand = 1)  
            scrollbar.pack(side=RIGHT, fill=Y)
            scrollbar.config(command=my_listbox.yview)    
        except Exception as e:
            print(e,"gets_stock")
            handler = f"invalid literal for int() with base 10: '{stock}'"
            e = str(e)
            if handler == e:
                tkinter.messagebox.showinfo("ERROR",  "Input Must Be NUMBER!")
                gets_price()
    else:
        tkinter.messagebox.showinfo("ERROR",  "Empty Input!")
        gets_price()  
def gets_unit():
    global win,text4,my_listbox,units,unit,frame_win,item_name1
    try:
        selected_gets_unit = my_listbox.curselection()
        my_listbox = my_listbox
    
        selected_gets_unit = str(selected_gets_unit).replace(",)","").replace("(","")
    except:
        selected_gets_unit = selected_gets_unit
    d = {}
    for i in range(len(units)):
        d[i] = units[i]
    unit = d[int(selected_gets_unit)]
    clear_win()
    win.geometry("640x120")
    
    label = Label(frame_win, text = f"Critical Value of {item_name1}", font = ("Arial", 20))
    label.pack() 
    text4 = Text(frame_win, width = 20, height = 1)
    text4.pack(pady = 5)
    but_done = Button(frame_win, text = "Done",bd = 3, font = ("Arial",15), command = gets_critical_value)
    but_done.pack()
    def handle_keypress(event):
        if event.keysym == "Return":
            return "break"  # Prevents the default behavior of the Enter key
        else:
            # Perform any other desired actions
            pass

    text4.bind("<KeyPress>", handle_keypress)
    def on_enter_press(event):
        gets_critical_value()
    text4.bind("<Return>", on_enter_press)
def cur_time():
    global current_time,month
    time = f"{month}:{current_time.day}:{current_time.year}"
    return time
def gets_critical_value():   
    global win,text4,item_name1,supplier_price,mark_up,stock,unit,critical_value,fromMainMenu,fromAdd,frame_win
    selling_price = (supplier_price * 30/100) + supplier_price
    selling_price = "%.2f"%selling_price
    try:
        critical_value = text4.get(1.0,"end-1c")
    except:
        critical_value = critical_value
    clear_win()
    win.geometry("350x120")
    if critical_value != "":
        try:
            critical_value = int(critical_value)
            file = open(f"./texts/items_name_price_stock.txt",'a')
            file.write(f"{cur_time()},{item_name1},{unit},{stock},{critical_value},{supplier_price},30,{selling_price}\n")
            file.close()
            win.destroy()
            qr_generator(item_name1)
            clear()
            product_inventory()     
        except Exception as e:
            handler = f"invalid literal for int() with base 10: '{critical_value}'"
            print(e,"gets_critical_value")
            e = str(e)
            if handler == e:
                tkinter.messagebox.showinfo("ERROR",  "Input Must Be NUMBER!")
                gets_unit()   
    else:
        tkinter.messagebox.showinfo("ERROR",  "Empty Input!")
        gets_unit()
def file_open_restock_amount():
    global item_amount_text,item_selected_restock
    global fromMainMenu,fields,date,item_name,unit,quantity,critical_value,orig_price,mark_up,selling_price,name,win,frame_win
    fields,date,item_name,unit,quantity,critical_value,orig_price,mark_up,selling_price= [],[],[],[],[],[],[],[],[]
    file = open("./texts/items_name_price_stock.txt", 'r')
    lines = file.readlines()
    file.close()
    fromMainMenu =False
    for x in lines:
        fields = x.split(",")
        date.append(fields[0])
        item_name.append(fields[1])
        unit.append(fields[2])
        quantity.append(int(fields[3]))
        critical_value.append(float(fields[4]))
        orig_price.append(float(fields[5]))
        mark_up.append(float(fields[6]))
        selling_price.append(float(fields[7])) 
    item_amount = item_amount_text.get(1.0, "end-1c")
    if item_amount != "":
        try:       
            item_amount = int(item_amount)
            file = open("./texts/items_name_price_stock.txt", 'w')
            file.write("")
            file.close()
            
            for i in range(len(item_name)):
                if item_name[i] == item_selected_restock:
                    quantity[i] += item_amount
                
                file = open("./texts/items_name_price_stock.txt", 'a')
                file.write(f"{date[i]},{item_name[i]},{unit[i]},{quantity[i]},{critical_value[i]},{orig_price[i]},{mark_up[i]},{selling_price[i]}\n")
                file.close()
            item_name = file_opener()
            win.destroy()
            clear()
            product_inventory()     
        except Exception as e:
            handler = f"invalid literal for int() with base 10: '{item_amount}'"
            e = str(e)
            if handler == e:
                win.geometry("300x120")
                tkinter.messagebox.showinfo("ERROR",  "Input Must Be Integer!")
                file_open_restock()
    else:
        tkinter.messagebox.showinfo("ERROR",  "Empty Input!")
        file_open_restock()

def file_open_restock():
    global selected,text1,my_listbox1,names1,item_amount_text,item_selected_restock,win,frame_win
    global fields,date,item_name,unit,quantity,critical_value,orig_price,mark_up,selling_price
    fields,date,item_name,unit,quantity,critical_value,orig_price,mark_up,selling_price = [],[],[],[],[],[],[],[],[]
    file = open("./texts/items_name_price_stock.txt", 'r')
    lines = file.readlines()
    file.close()
    for x in lines:
        fields = x.split(",")
        date.append(fields[0])
        item_name.append(fields[1])
        unit.append(fields[2])
        quantity.append(int(fields[3]))
        critical_value.append(float(fields[4]))
        orig_price.append(float(fields[5]))
        mark_up.append(float(fields[6]))
        selling_price.append(float(fields[7]))
    try:
        selected_file_open_restock = my_listbox1.curselection()
        my_listbox1 = my_listbox1
    
        selected_file_open_restock = str(selected_file_open_restock).replace(",)","").replace("(","")
    except:
        selected_file_open_restock = selected_file_open_restock
    d = {}
    for i in range(len(item_name)):
        d[i] = item_name[i]
    item_selected_restock = d[int(selected_file_open_restock)]
 
    clear_win()
    win.geometry("500x120")
    win.attributes('-topmost', True)
    label = Label(frame_win, text = f"Quantity of {item_selected_restock}", font = ("Arial", 20))
    label.pack()
    
    item_amount_text = Text(frame_win, width = 20, height = 1)
    item_amount_text.pack(pady = 5)
    
    but_done = Button(frame_win, text = "Done",bd = 3, font = ("Arial",15), command = file_open_restock_amount)
    but_done.pack()
    item_name = file_opener()
    def handle_keypress(event):
        if event.keysym == "Return":
            return "break"  # Prevents the default behavior of the Enter key
        else:
            # Perform any other desired actions
            pass
    item_amount_text.bind("<KeyPress>", handle_keypress)
    def on_enter_press(event):
        file_open_restock_amount()
    item_amount_text.bind("<Return>", on_enter_press)
name,fromRestock = None,False
def Restock():
    global text4,item_name,my_listbox1,names1,fromRestock,win,frame_win,item_name1
    fromRestock = True
    item_name = file_opener()
    win = Tk()
    win.title('InventoProfit')
    win.geometry("350x120")
    win.attributes('-topmost', True)
    win.resizable(False,False)
    frame_win = Frame(win)
    frame_win.pack(fill = BOTH,expand = 1)
    canvas = Canvas(frame_win, bg = "white")
    
    label = Label(frame_win, text = "Item Name to Be Restocked", font = ("Arial", 20))
    label.pack()
    label1 = Label(frame_win,text = "Choose an Item...", bg = "white",font = ("Courier", 10)).pack(pady=5)
    def toggle_size():
        global is_large
        if not is_large:
            win.geometry("350x400")
            is_large = True
        else:
            win.geometry("350x120")
            is_large = False      
    button = Button(frame_win, text="...", font = 'bold', height = 1,relief = SUNKEN,command=toggle_size)
    button.place(x = 250,y = 42)
    but_done = Button(frame_win, text = "Done",bd = 3, font = ("Arial",15), command = file_open_restock)
    but_done.pack()
    canvas.pack(side = BOTTOM,expand = 1)
    scrollbar = Scrollbar(canvas)
    scrollbar.pack(side=RIGHT, fill=Y)
    my_listbox1 = Listbox(canvas,yscrollcommand=scrollbar.set, width = 200,height = 400,font = ("Arial",20),selectmode = SINGLE)
    names1 = []
    for i in range(len(item_name)):
        names1.append(item_name[i])
        my_listbox1.insert(END, f"{item_name[i]}")
    my_listbox1.pack(side=LEFT)
    scrollbar.config(command=my_listbox1.yview)
    win.mainloop()
def Add():
    global frame_win,win,item_name,is_large,date,unit,quantity,critical_value,orig_price,mark_up,selling_price,text,fromMainMenu,fromAdd
    fromMainMenu = False
    fromAdd = True
    item_name = file_opener()
    win = Tk()
    win.title('InventoProfit')
    win.geometry("350x120")
    win.attributes('-topmost', True)
    win.resizable(False,False)
    frame_win = Frame(win)
    frame_win.pack(fill = BOTH,expand = 1)
    canvas = Canvas(frame_win, bg = "white")
    label = Label(frame_win, text = "Name of The Item", font = ("Arial", 20))
    label.pack()
    text = Text(frame_win, width=30, height=1, bg='white', fg='black', highlightthickness=0)
    text.insert(END, "Input an Item")
    text.config(fg='grey') 
    def on_entry_click(event):
        if text.get("1.0", "end-1c") == "Input an Item":
           text.delete("1.0", "end-1c")  
           text.config(fg='black')
    text.bind('<FocusIn>', on_entry_click)
    text.pack(pady = 5)
    def handle_keypress(event):
        if event.keysym == "Return":
            return "break"  
        else:
            pass
    text.bind("<KeyPress>", handle_keypress)
    def on_enter_press(event):
        gets_name()
    text.bind("<Return>", on_enter_press)  
    
    but_done = Button(frame_win, text = "Done",bd = 3, font = ("Arial",15), command = gets_name)
    but_done.pack()
    canvas.pack(side = BOTTOM,expand = 1)
    scrollbar = Scrollbar(canvas)
    scrollbar.pack(side=RIGHT, fill=Y)
    my_listbox = Listbox(canvas,yscrollcommand=scrollbar.set, width = 200,height = 400,font = ("Arial",20))
    my_listbox.pack(side=LEFT)
    scrollbar.config(command=my_listbox.yview) 
    win.mainloop()
fromAdd = False
def menu():    
    if isDone == True:
        clear()
        menu_widgets("")
    else:
        pass       
def opening_menu():
    global fromMenu,fromCreate,fromForgot
    fromForgot,fromMenu,fromCreate = False,True,False
    clear()
    root.geometry("900x600")
    opening_menu_widgets()
opening_menu()
root.mainloop()
cap.release()

folder_path = "./ARCHIVED_ITEMS/" 
file_list = os.listdir(folder_path)
for file_name in file_list:
    file_path = os.path.join(folder_path, file_name)
    os.remove(file_path)



