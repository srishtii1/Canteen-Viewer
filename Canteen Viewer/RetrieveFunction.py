import tkinter as tk                 
from datetime import datetime as dt   
from tkinter import *
import datetime
from tkinter import messagebox  
import calendar
import time

#-------------RETRIEVE ALL STALLS FROM STALL.TXT-------------------------

def retrieveAllStall():  #Bernard  
    with open('Stall.txt','r') as stallFile:
        stall = {}
        for line in stallFile:
            x = line.strip().split(',')
            stallKey = x[0]    #1
            stallName = x[1]   #Chinese Cuisine
            startHour = x[2]   #0800
            endHour = x[3]     #1500
            waitingTime = x[4] #5
    
            stallInfo = [stallName, startHour, endHour, waitingTime]
            stall[stallKey] = stallInfo     
    return stall

# eg.stall = {'1' : [Chinese Cuisine, 0800, 1500, 5],
#             '2' : [Malay Cuisine, 0800, 1600, 6],
#             '3' : [Noodle and Soup, 0700, 1700, 5] }
#      'stallKey' : [stallName, startHour, endHour, waitingTime]

def retrieveStallInfo(key):   #Bernard    
    with open('Stall.txt','r') as stallFile:
        stall = {}
        for line in stallFile:
            x = line.strip().split(',')
            stallKey = x[0]
            if stallKey == key:
                stallName = x[1]
                startHour = x[2]
                endHour = x[3]
                waitingTime = x[4]

                stallInfo = [stallName, startHour, endHour, waitingTime]
                stall[stallKey] = stallInfo
    return stall


#---------------RETRIEVE ALL MENU OF ALL STALLS FROM MENU.TXT------------------
def retrieveAllMenu():   #Bernard 
    with open('Menu.txt','r') as menuFile:
        menu = {}
        itemKey = 1    #To be used for dictionary key for each menu item.
        for line in menuFile:
            x = line.strip().split(',')
            itemName = x[0]            #Chicken Rice
            stallKey = x[1]            #1
            availability = x[2]        #Everyday
            startAvailableHour = x[3]  #0800
            endAvailableHour = x[4]    #1500
            itemPrice = x[5]           #3.5

            menuItem = [itemName, stallKey, availability, startAvailableHour, endAvailableHour, itemPrice]
            menu[itemKey] = menuItem
            itemKey += 1
    return menu

# eg.menu = {'1' : [Chicken Rice, 1, Everyday, 0800, 1500, 3.5]}
#      'itemKey' : [itemName, stallKey, avaialbility, startAvailableHour, endAvailableHour, itemPrice]





#---------------RETRIEVE ALL THE MENU OF A SPECIFIC STALL BY COMPARING THE STALLKEY (INNER JOIN)----------

def displayStallMenu(stallKey,menu):     #Bernard 
    stallMenu = {} #All the menu item of a specific stall
    count = 1      #To be used for dictionary key for each menu item within the stall menu
    for key, itemInfo in menu.items():  # key = dictionary's key, itemInfo = value(eg. [list])
        menu_stallKey = itemInfo[1]     
        if menu_stallKey == stallKey:   # if menu's stallKey is the same as the given parameter of the specific store, then continue        
            menuItem = [itemInfo[0],itemInfo[1],itemInfo[2],itemInfo[3],itemInfo[4],itemInfo[5]]
            stallMenu[count] = menuItem
            count += 1
    return stallMenu
# eg.stallMenu = {'1' : [Chicken Rice, 1, Everyday, 0800, 1500, 3.5] }
#             'count' : [itemName, stallKey, availability, startAvailableHour, endAvailableHour, itemPrice]


#OPTION 1-------------RETRIEVE ALL THE MENU OF A SPECIFIC STALL BASED ON CURRENT SYSTEM TIME---------------

def displayMenuBySystem(stallKey,menu):  #Bernard 
    menuList = displayStallMenu(stallKey, menu)  #Retrieve all menu specific to the store
    itemKey = 1 #To be use for dictionary key for each menu item within the available stall's menu
    todaydate = dt.today() #Take the current date of the system
    todayday = calendar.day_name[todaydate.weekday()] #Determine which day it is
    timenow = dt.now() #Get the current of the system
    hr = str(timenow.hour) #Get the hour value
    ma = timenow.minute #Get the minute value
    if ma < 10:
        mm='0'+str(ma)
    else:
        mm=str(ma)
    HHMM = hr+mm #Combine hour and minute value to get HHMM format
    stallMenu = {} #Create a dictionary for the available menu of the specific stall
    for key, itemInfo in menuList.items():
        availabilityList = itemInfo[2].split('+') #Split the available date (eg. Monday+Wednesday > Monday, Wednesday)
        for availabledate in availabilityList: #for each value inside available date, do something
            if availabledate == "Everyday" or availabledate == todayday: #Do something if the value is Everyday or if the value is same as today's day(eg. Monday)
                if int(itemInfo[3])< int(HHMM) and int(HHMM) < int(itemInfo[4]): #Do something if the current time is more than the starting available hour but lesser than the ending available hour of the menu item
                    menuItem = [itemInfo[0],itemInfo[1],itemInfo[5]] #Create a list to store name of the menu item, the stallKey of which stall it belong to, price of the menu item
                    stallMenu[itemKey] = menuItem #Create a dictionary of the available menu item of the specific stall
                    itemKey += 1 #Increment the value to use for next dictionary value
    return stallMenu #Return the every menu item of a specific stall

     
#OPTION 2---------------RETRIEVE ALL THE MENU OF A SPECIFIC STALL BASED ON USER INPUT TIME AND DATE--------------
 
def displayMenuByTime(stallKey,menu,inputdate, HHMM): #inputdate format ('YYYY-MM-DD'), HHMM format ('HHMM') #Bernard
    menuList = displayStallMenu(stallKey, menu)  #Retrieve all menu specific to the store
    itemKey = 1 #To be use for dictionary key for each menu item within the available stall's menu
    year, month, day = (int(x) for x in inputdate.split('-')) #split the date paramter into 3 separate value
    inputdatestring = datetime.date(year,month,day) #create a date object with value YYYY MM DD
    inputday = calendar.day_name[inputdatestring.weekday()] #get the day of the date (eg. monday)
    stallMenu = {} #Create a dictionary for the available menu of the specific stall
    for key, itemInfo in menuList.items():
        availabilityList = itemInfo[2].split('+') #Split the available date (eg. Monday+Wednesday > Monday, Wednesday)
        for availabledate in availabilityList: #for each value inside available date, do something
            if availabledate == "Everyday" or availabledate == inputday: #Do something if the value is Everyday or if the value is same as today's day(eg. Monday)
                if int(itemInfo[3]) <= int(HHMM) and int(HHMM) <= int(itemInfo[4]): #Do something if the current time is more than the starting available hour but lesser than the ending available hour of the menu item
                    menuItem = [itemInfo[0],itemInfo[1],itemInfo[5]] #Create a list to store name of the menu item, the stallKey of which stall it belong to, price of the menu item
                    stallMenu[itemKey] = menuItem #Create a dictionary of the available menu item of the specific stall
                    itemKey += 1 #Increment the value to use for next dictionary value
    return stallMenu #Return the every menu item of a specific stall    




def calculateWaitTime(waitingTime, inputPeople):#Andrel #stallKey is the specific key of the stall, inPeople is user input integer,stall is the dictionary for all the stall
    calculatedTime = waitingTime*inputPeople

    return calculatedTime


def DisplayOperatingHrs(stallKey, stall): #Andrel
    for key, itemInfo in stall.items():
        if key == stallKey:
            openingHr = itemInfo[1] + ' to ' + itemInfo[2]
    return openingHr #Return the string openingHr
    


def retrieveOperatingHours():    #Andrel
    with open('Stall.txt','r') as stallFile:
        stall = {}
        for line in stallFile:
            x = line.strip().split(',')
            stallKey = x[0]    #1
            stallName = x[1]   #Chinese Cuisine
            startHour = x[2]   #0800
            endHour = x[3]     #1500
    
            stallInfo = [stallName, startHour, endHour]
            stall[stallKey] = stallInfo     
    return stall

def exitprog(self): #Andrel 
        response = tk.messagebox.askquestion("Exit Application", "Do you want to exit the application?")
        if response == 'yes':
           self.destroy()
        else:
            tk.messagebox.showinfo('Return','You will now return to the application')
