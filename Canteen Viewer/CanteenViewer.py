import tkinter as tk
import RetrieveFunction as rf
from datetime import datetime as dt
from functools import partial
from tkcalendar import Calendar
from tkinter import PhotoImage

root = tk.Tk()#creates the root for the screen
root.title("Canteen Viewer")
root.iconbitmap("./Gui_Images/CanteenViewer.ico")


def backgroundSet(): #Populate child. Creates the background image #Srishti
    imageBackground = tk.PhotoImage(file="./Gui_Images/background.gif") #background
    w = imageBackground.width() 
    h = imageBackground.height()
    if root.winfo_x() == 0:
        x = 200
        y = 600
        root.lift()
    else:
        x = int(root.winfo_x())
        y = int(root.winfo_y())
    root.geometry("%dx%d+%d+%d" % (w, h, x, y))
    main_Panel = tk.Label(root, image = imageBackground)
    main_Panel.pack(side="top", fill="both", expand="yes")
    main_Panel.image = imageBackground
    now = dt.now()
    rightnow = now.strftime("%d/%m/%Y %H:%M:%S")
    
    label_datetime = tk.Label(main_Panel, text=rightnow, font=("Bookman Old Style", 14, "bold"),
                              foreground="white", background="black",
                              relief="groove",
                              padx=5, pady=5)#label for date and time
    label_datetime.pack()
    label_datetime.place(relx=0.5, rely=1, anchor="s") 

    rawImg_Exit = tk.PhotoImage(file="./Gui_Images/exit.gif") #exit button
    imageExit = rawImg_Exit.subsample(6,6)
    w_exit = imageExit.width()
    h_exit = imageExit.height()
    button_Exit = tk.Button(main_Panel, width=w_exit, height=h_exit,
                            image=imageExit, command=lambda: rf.exitprog(root))
    button_Exit.image = imageExit
    button_Exit.pack()
    button_Exit.place(relx=0, rely=1, anchor="sw")
    
    return main_Panel
 
    
def kill_all_children(root): #Delete all child #Srishti
    _list = root.winfo_children()
    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())
    for item in _list:
        item.pack_forget()

def kill_all_window(window): #Delete all child (window) #Srishti
    _list = window.winfo_children()
    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())
    for item in _list:
        item.pack_forget()

def StartPage(): #First Page #Srishti
    kill_all_children(root)
    main_Panel = backgroundSet()
    
    label_Welcome = tk.Label(main_Panel, text="Welcome to Canteen Viewer",
                             font=("Bookman Old Style", 30, "bold"), foreground="#654321",
                             background="WHITE", padx=10, pady=5, relief="groove") #Welcome user
    label_Welcome.pack()
    label_Welcome.place(relx=0.5, rely=0.2, anchor="center")
    
    button_ViewToday = tk.Button(main_Panel, text="View Today's Stall",
                                 font=("Bookman Old Style", 14, "bold"), foreground="white",
                                 background="#654321", padx=5, pady=5,
                                 highlightthickness = 5,
                                 borderwidth=4,
                                 command=lambda: ViewToday()) #View Today's Stall Button
    button_ViewToday.pack()
    button_ViewToday.place(relx=0.5, rely=0.4, anchor="center")

    button_Calendar = tk.Button(main_Panel, text="View Stall by Date",
                                 font=("Bookman Old Style", 14, "bold"), foreground="white",
                                 background="#654321", padx=5, pady=5,
                                 highlightthickness = 5,
                                 borderwidth=4,
                                 command=lambda: ViewCalendar()) #View Stall by Date Button
    button_Calendar.pack()
    button_Calendar.place(relx=0.5, rely=0.6, anchor="center")


def ViewToday(): #View Today's Stall #Srishti and Bernard
    kill_all_children(root)
    main_Panel = backgroundSet()
    
    rawImg_Back = tk.PhotoImage(file="./Gui_Images/back.gif") #Back Button
    imageBack = rawImg_Back.subsample(25,25)
    w = imageBack.width()
    h = imageBack.height()
    button_Back = tk.Button(main_Panel, width=w, height=w,
                            image=imageBack, command=lambda: StartPage())
    button_Back.image = imageBack
    button_Back.pack()
    button_Back.place(relx=1, rely=1, anchor="se")

    label_ViewToday = tk.Label(main_Panel, text="Stalls Available Today",
                             font=("Bookman Old Style", 20, "bold"), foreground="white",
                             background="#654321", padx=50, pady=5, relief="groove") #Heading "Stalls Available Today"
    label_ViewToday.pack()
    label_ViewToday.grid(row=0,column=2, columnspan=3, pady=10, sticky="w")
    
    stall = rf.retrieveAllStall()
    rowcount = 1
    for key, itemInfo in stall.items(): #Populate all stalls
        stallName = itemInfo[0]
        filename = './Images/' + key + ".png"
        rawImg = PhotoImage(file = filename)
        nImg = rawImg.subsample(1,1)
        op = "0"
        button_Stall = tk.Button(main_Panel, width=250, height=150, anchor="center",
                                 image=nImg, background="white",
                                 command=partial(TodayStallMenu, key, stallName,op)) #Button to view that stall's menu
        button_Stall.image = nImg

        label_Stall = tk.Label(main_Panel, width=19, anchor="center", font=("Bookman Old Style", 15, "bold"),
                                text=stallName, background="black", foreground="white") #Stall's Name
        columncount = int(key)

        
        if int(key) > 3: #Position and organzie each stall
            columncount = int(key)%3
            if columncount != 0:
                columncount = columncount
            else:
                columncount = 3
        else:
            columncount = columncount
                     
        if int(key)%3 == 1 and int(key) != 1:
            rowcount += 1
        else:
            rowcount = rowcount
        label_Stall.grid(row=rowcount,column=columncount, sticky="n",pady=20)    
        button_Stall.grid(row=rowcount,column=columncount,padx=27,pady=40, sticky="n")

def ViewCalendar(): #Pop Calendar Function #Srishti
    cal_window = tk.Tk()
    cal_window.title("Canteen Viewer Calendar")
    cal_window.iconbitmap("./Gui_Images/CanteenViewer.ico")
    cal_window.resizable(False,False)
    
    todaydate = dt.today()
    label_Select = tk.Label(cal_window, text="Please Choose A Date and Enter A Time",
                             font="Verdana 15 bold", foreground="white",
                             background="black", padx=5, pady=5, relief="groove") #Heading "Please Choose A Date and Enter A Time"
    label_Select.pack()
    
    cal = Calendar(cal_window, font="Verdana 12 bold", selectmode="day",
                   curcor="hand1", background="gray", foreground="white",
                   year=todaydate.year, month=todaydate.month,
                   day=todaydate.day,) #Calendar Picker
    cal.pack(fill="both")

    userEntry = tk.Entry(cal_window, text="HHMM",font="Verdana 18") #Entry Box to input time
    userEntry.pack()


    
    button_Select = tk.Button(cal_window, text="Enter",
                              font="Verdana 11 bold", foreground="black",
                              background="white", padx=5,
                              command=lambda:SelectedDayStall(userEntry.get(), cal.selection_get(), cal_window)) #Confirm date and time selected
    button_Select.pack()
    button_Select.place(relx=0.99, rely=0.995, anchor="se")

    label_HHMM = tk.Label(cal_window, text="HHMM >", font="Verdana 11 bold", foreground="black",
                          background="white") #Label "HHMM"
    label_HHMM.pack()
    label_HHMM.place(relx=0, rely=0.98, anchor="sw")



def SelectedDayStall(userHour ,userDate, cal_window): #View Selected Date's Stall #Srishti and Bernard
    if userHour.isdigit(): #Error Handling
        intHour = int(userHour)
        if intHour < 0 or intHour > 2359 or len(userHour) > 4 or len(userHour) < 4:
            response = tk.messagebox.showinfo("Error", "Please enter a valid time within 0000 to 2359 in HHMM format!")
            cal_window.lift()
        else:
            kill_all_children(root)
            main_Panel = backgroundSet()
            if cal_window !=0:
                cal_window.destroy()

            rawImg_Back = tk.PhotoImage(file="./Gui_Images/back.gif") #Back Button
            imageBack = rawImg_Back.subsample(25,25)
            w = imageBack.width()
            h = imageBack.height()
            button_Back = tk.Button(main_Panel, width=w, height=w,
                            image=imageBack, command=lambda:StartPage())
            button_Back.image = imageBack
            button_Back.pack()
            button_Back.place(relx=1, rely=1, anchor="se")
            
            hourString = str(userHour[0:2])
            minString = str(userHour[2:4])
            label_Picked = tk.Label(main_Panel, text="Stalls Available for "+ str(userDate) +" , " + hourString +":" +minString,
                             font=("Bookman Old Style", 20, "bold"), foreground="white",
                             background="#654321", padx=5, pady=5, relief="groove") #Heading for the selected date and time
            label_Picked.pack()
            label_Picked.grid(row=0, column=2, columnspan=3, pady=10, sticky="w")

            stall = rf.retrieveAllStall()
            rowcount = 1
            op = "0"
            for key, itemInfo in stall.items(): #Populate all stalls based on selected date and time
                stallName = itemInfo[0]
                filename = './Images/' + key + ".png"
                rawImg = PhotoImage(file = filename)
                nImg = rawImg.subsample(1,1)
                button_Stall = tk.Button(main_Panel, width=250, height=150, anchor="center",
                                 image=nImg, background="white",
                                 command=partial(SelectedStallMenu, key, userHour, userDate, stallName, op)) #Button to view that stall's menu
                button_Stall.image = nImg
                label_Stall = tk.Label(main_Panel, width=19, anchor="center", font=("Bookman Old Style", 15, "bold"),
                                text=stallName, background="black", foreground="white") #Stall name
                columncount = int(key)

        
                if int(key) > 3: #Position and organize each stall
                    columncount = int(key)%3
                    if columncount != 0:
                        columncount = columncount
                    else:
                        columncount = 3
                else:
                    columncount = columncount
                     
                if int(key)%3 == 1 and int(key) != 1:
                    rowcount += 1
                else:
                    rowcount = rowcount
                label_Stall.grid(row=rowcount,column=columncount, sticky="n",pady=20)    
                button_Stall.grid(row=rowcount,column=columncount, padx=27,pady=40, sticky="n")
    else:
        response = tk.messagebox.showinfo("Error","Please enter only number for the time in HHMM format!")
        cal_window.lift()
    

def SelectedStallMenu(key, userHour, userDate, stallName, op): #SELECTED DATE MENU #Srishti and Bernard
    kill_all_children(root)
    main_Panel = backgroundSet()
    stall = rf.retrieveAllStall()
    
    button_Operating = tk.Button(main_Panel,text="View Operating Hrs",
                                 command=partial(refreshSelectMenu, key,userHour,userDate,stallName),
                                 font=("Bookman Old Style", 15), foreground="white", background="black",
                                 height=1) #Button to show operating hours
    button_Operating.place(x=22,y=80)
    
    if op != "0": #To check if operating hour button is clicked
        hr = rf.DisplayOperatingHrs(key,stall)
        label_OperatingHrs = tk.Label(main_Panel, text= "Operating Hrs: "+ hr, font=("Bookman Old Style", 15, "bold"),
                                  background="black", foreground="white") #Display operating hours
        label_OperatingHrs.place(x=20, y=80)
        button_Operating.place_forget()

    rawImg_Back = tk.PhotoImage(file="./Gui_Images/back.gif") #Back Button
    imageBack = rawImg_Back.subsample(25,25)
    cal_window = 0
    w = imageBack.width()
    h = imageBack.height()   
    button_Back = tk.Button(main_Panel, width=w, height=w,
                            image=imageBack, command=lambda: SelectedDayStall(userHour, userDate, cal_window))
    button_Back.image = imageBack
    button_Back.pack()
    button_Back.place(relx=1, rely=1, anchor="se")
    
    hourString = str(userHour[0:2])
    minString = str(userHour[2:4])
    label_SelectedStall = tk.Label(main_Panel, text=stallName +" for "+ str(userDate) +" , " + hourString +":" +minString,
                             font=("Bookman Old Style", 20, "bold"), foreground="white",
                             background="#654321", padx=5, pady=5, relief="groove") #Heading for the selected date and time 
    label_SelectedStall.pack()
    label_SelectedStall.grid(row=0,column=2, columnspan=5, pady=10, sticky="w")


    filename = './Images/' + key + ".png"
    rawImg = PhotoImage(file = filename)
    nImg = rawImg.zoom(1,1)
    w = nImg.width()
    h = nImg.height()
    img_Selected = tk.Label(main_Panel, image=nImg, width=w, height=h, relief="solid")
    img_Selected.image = nImg
    img_Selected.grid(row=2, column=1, rowspan=4, pady=100, padx=50, sticky="w") #Stall's logo
   
    menu = rf.retrieveAllMenu()
    menuList = rf.displayMenuByTime(key,menu,str(userDate),str(userHour))
    if not menuList: #Error Handling if no menu, display this
        label_Unavailable = tk.Label(main_Panel, text="There is no menu available at this timing",
                                     font=("Bookman Old Style", 20), foreground="white",
                                     background="black", padx=5, pady=5, relief="flat")
        label_Unavailable.grid(row=4, column=2, columnspan=2, sticky = "n") 
    else: #Error Handling if got menu, then display the menu
        button_Waiting = tk.Button(main_Panel, text="Calculate waiting time",
                                     font=("Bookman Old Style", 15), foreground="white",
                                     background="#654321", padx=5, pady=5,
                                     command=lambda: waitingTime(key, stallName))
        button_Waiting.grid(row=2, column=1, rowspan=4, sticky="s")
        count = 1
        rowcount = 2
        for menuKey, itemInfo in menuList.items():

            filename = './Menu_Images/' + itemInfo[0] + ".png"
            rawImg = PhotoImage(file = filename)
            nImg = rawImg.subsample(1,1)
            label_Menu = tk.Label(main_Panel, width=200, height=150, anchor="center",
                                 image=nImg, background="white") #Menu's image
            label_Menu.image = nImg
            
            label_Name = tk.Label(main_Panel, width=24, anchor="n", font="Verdana 8 bold",
                                  text=itemInfo[0] + "     $" + itemInfo[2], background="black", foreground="white") #Menu's Name


            
            
            colcount = 0
            
            if count > 3:   #To position and organise menu item
                if count%3 == 1:
                    rowcount += 1
                    colcount = 2
                elif count%3 ==2:
                    rowcount=rowcount
                    colcount = 3
                elif count%3 == 0:
                    rowcount=rowcount
                    colcount = 4
                count += 1
            else:
                colcount = count+1
                rowcount = 2
                count += 1
                
    
            label_Menu.grid(row=rowcount,column=colcount,pady=18,padx=20, sticky="s")
            label_Name.grid(row=rowcount,column=colcount,padx=0, sticky="s")


def refreshTodayMenu(key,stallName): #Refresh Page #Andrel
    op = "1"
    TodayStallMenu(key, stallName, op)

def refreshSelectMenu(key, userHour, userDate, stallName): #Refresh Page #Andrel
    op = "1"
    SelectedStallMenu(key, userHour, userDate, stallName, op)
    
def TodayStallMenu(key, stallName, op): #TODAY MENU #Srishti and Bernard
    kill_all_children(root)
    main_Panel = backgroundSet()
    stall = rf.retrieveAllStall()
    
    button_Operating = tk.Button(main_Panel,text="View Operating Hrs",
                                 command=partial(refreshTodayMenu, key,stallName),
                                 font=("Bookman Old Style", 15), foreground="white", background="black",
                                 height=1) #Button to display operating hours
    button_Operating.place(x=22,y=80)
    
    if op != "0": #To check if operating hour button is clicked
        hr = rf.DisplayOperatingHrs(key,stall)
        label_OperatingHrs = tk.Label(main_Panel, text= "Operating Hrs: "+ hr, font=("Bookman Old Style", 15, "bold"),
                                  background="black", foreground="white")
        label_OperatingHrs.place(x=2, y=80)
        button_Operating.place_forget()
        
        
    rawImg_Back = tk.PhotoImage(file="./Gui_Images/back.gif")
    imageBack = rawImg_Back.subsample(25,25)
    w = imageBack.width()
    h = imageBack.height()
    button_Back = tk.Button(main_Panel, width=w, height=w,
                            image=imageBack, command=lambda: ViewToday()) #Back Button
    button_Back.image = imageBack
    button_Back.pack()
    button_Back.place(relx=1, rely=1, anchor="se")

    



    label_SelectedStall = tk.Label(main_Panel, text=stallName +"'s Menu for the day",
                             font=("Bookman Old Style", 20, "bold"), foreground="white",
                             background="#654321", padx=5, pady=5, relief="groove") #Heading for stall's menu based on the date and time

    label_SelectedStall.grid(row=0,column=2, columnspan=5, pady=10, sticky="w")
    


    
    filename = './Images/' + key + ".png"
    rawImg = PhotoImage(file = filename)
    nImg = rawImg.zoom(1,1)
    w = nImg.width()
    h = nImg.height()
    img_Selected = tk.Label(main_Panel, image=nImg, width=w, height=h, relief="solid")
    img_Selected.image = nImg
    img_Selected.grid(row=2, column=1, rowspan=4, pady=100, padx=50, sticky="n") #Stall's logo
   
    menu = rf.retrieveAllMenu()
    menuList = rf.displayMenuBySystem(key,menu)
    if not menuList: #Error Handling if no menu, display this
        label_Unavailable = tk.Label(main_Panel, text="There is no menu available at this timing",
                                     font=("Bookman Old Style", 20), foreground="white",
                                     background="black", padx=5, pady=5, relief="flat")
        label_Unavailable.grid(row=4, column=2, columnspan=2, sticky = "n")
    else: #Error Handling if got menu, then display the menu
        button_Waiting = tk.Button(main_Panel, text="Calculate waiting time",
                                     font=("Bookman Old Style", 15), foreground="white",
                                     background="#654321", padx=5, pady=5,
                                     command=lambda: waitingTime(key,stallName))
        button_Waiting.grid(row=2, column=1, rowspan=4, sticky="s")
        count = 1
        rowcount = 2
        for menuKey, itemInfo in menuList.items():
            filename = './Menu_Images/' + itemInfo[0] + ".png"
            rawImg = PhotoImage(file = filename)
            nImg = rawImg.subsample(1,1)
            label_Menu = tk.Label(main_Panel, width=200, height=150, anchor="center",
                                 image=nImg, background="white") #Menu's image
            label_Menu.image = nImg
            
            label_Name = tk.Label(main_Panel, width=24, anchor="n", font="Verdana 8 bold",
                                  text=itemInfo[0] + "     $" + itemInfo[2], background="black", foreground="white") #Menu's name


            
            colcount = 0
            
            if count > 3:  #To position and organise menu item
                if count%3 == 1:
                    rowcount += 1
                    colcount = 2
                elif count%3 ==2:
                    rowcount=rowcount
                    colcount = 3
                elif count%3 == 0:
                    rowcount=rowcount
                    colcount = 4
                count += 1
            else:
                colcount = count+1
                rowcount = 2
                count += 1
                
            label_Menu.grid(row=rowcount,column=colcount,pady=18,padx=20, sticky="s")
            label_Name.grid(row=rowcount,column=colcount,padx=0, sticky="s")
    


def waitingTime(key, stallName): #Waiting Time Calculator #Andrel
    window = tk.Tk()
    window.title("Canteen Viewer Calculator")
    window.iconbitmap("./Gui_Images/CanteenViewer.ico")
    stall = rf.retrieveAllStall()
    
    label_Calculate = tk.Label(window, text="Enter No. of People in Queue",
                               font=("Bookman Old Style", 10 ), foreground="black",
                               padx=5, pady=5, relief="flat")
    label_Calculate.grid(row=2, column=1) #Heading for the waiting time calculator
    
    label_Stall = tk.Label(window, text=stallName, font=("Bookman Old Style", 15, "bold"), foreground="white",
                           background="black", padx=5, pady=5, relief="flat")
    label_Stall.grid(row=1, column=1) #Stall's Name
    
    userInput = tk.Entry(window, font=("Bookman Old Style", 10, "bold"))
    userInput.grid(row=3, column=1, pady=10) #Entry box to input number of people in queue
    
    button_CalculateTime = tk.Button(window, text="Calculate",
                                     font=("Bookman Old Style", 10, "bold"), foreground="black",
                                     background="white", padx=5, pady=5,
                                     command=lambda:calculateTime(key,label_Calculate,userInput,button_CalculateTime,window))
    button_CalculateTime.grid(row=4, column=1) #Button to confirm calculate
    
    def calculateTime(key,label_Calculate,userInput,button_CalculateTime,window): #Andrel


        if userInput.get().isdigit(): #Error handling if is all number, continue
            num = int(userInput.get())
            if num <20: #If input is less than 20, continue
                stall = rf.retrieveStallInfo(key)
                waitingTime = stall[key][3]
                calculatedTime = rf.calculateWaitTime(int(waitingTime),int(userInput.get()))
            else: #Else show message that queue is too long
                response = tk.messagebox.showinfo("Oops!","Look like the queue is too long! Recommended to try another stall")
                calculatedTime = 0
                window.lift() 
        
        else: #Error handling if input contain non-number, prompt error
            response = tk.messagebox.showinfo("Error","Please enter a valid number!")
            calculatedTime = 0
            window.lift()
             
            
        kill_all_window(window)
        label_Calculate.grid_forget()
        userInput.grid_forget()
        
        button_CalculateTime.grid_forget()
        label_Calculate = tk.Label(window, text="Enter No. of People in Queue",
                                   font=("Bookman Old Style", 10), foreground="black",
                                   padx=5, pady=5, relief="flat") #Heading for the waiting time calculator
        label_Calculate.grid(row=2, column=1, pady=5, sticky="n")
        
        labelTime = tk.Label(window, text="Estimated Time: " + str(calculatedTime) +" min", font="Verdana 10 bold", foreground="black",
                         padx=5, pady=5, relief="flat") #Result of the calculation
        
        label_Stall = tk.Label(window, text=stallName, font=("Bookman Old Style", 15, "bold"), foreground="white",
                               background="black", padx=5, pady=5, relief="flat") #Stall's Name
        label_Stall.grid(row=1, column=1,pady=10)
        
        labelTime.grid(row=3, column=1)
        
        userInput = tk.Entry(window, font=("Bookman Old Style", 10, "bold"))
        userInput.grid(row=4, column=1, pady=10) #Entry box to input another number of people in queue
        
        button_CalculateTime = tk.Button(window, text="Calculate",
                                          font=("Bookman Old Style", 10, "bold"), foreground="black",
                                         background="white", padx=5, pady=5,
                                         command=lambda:calculateTime(key,label_Calculate,userInput,button_CalculateTime,window))
        button_CalculateTime.grid(row=5, column=1) #Button to try calcualte again
    

            
StartPage()
root.resizable(False, False)
root.mainloop()
