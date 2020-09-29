import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import urllib.request, urllib.parse, urllib.error
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from tkinter import ttk

HEIGHT = 500
WIDTH = 600
#Web scrapper function

# mtg_cards function prints to excel
def mtg_cards(link):
    #https://stackoverflow.com/questions/16627227/http-error-403-in-python-3-web-scraping
    #The website blocked the normal urllib request function so had to use FancyURLopener
    #solution is in the comment above
    class AppURLopener(urllib.request.FancyURLopener):
        version = "Mozilla/5.0"
    opener = AppURLopener()
    response = opener.open(link)
    soup = BeautifulSoup(response, 'html.parser')
    label_list = []
    condition = {0:"NM",1:"EX",2:"VG",3:"G"}
    count = 0
    name = []
    edition = []
    name_index = 0
    #Creating and writing to a csv file
    filename = "mtg.csv"
    f = open(filename, "w")
    headers = "card, edition, quanity, condition, price\n"
    f.write(headers)

    #lets me find the bit of HTML that has the card names, edition, quality, price
    #and quanity
    item_wrapper = soup.findAll("div",{"class":"itemContentWrapper"})
    cart_wrapper = soup.findAll("div",{"class":"amtAndPrice"})

    #Loops each card name and edition and puts them into seperate lists so I can
    #Print them out with the proper price below
    for item_wrap in item_wrapper:
        name.append(item_wrap.td.span.text.strip())
        edition.append(item_wrap.div.text.strip())

    #Prints each price and condition for the correpsonding card name and edition
    #Used a counter with a list for the condition since for the website I am trying
    #scrap has a standardized format
    for cart_wrap in cart_wrapper:
        if count == 4:
            count = 0
            name_index += 1
        f.write(name[name_index]+","+edition[name_index]+","+cart_wrap.text.strip() +"," + condition[count] +","+"\n")
        label_list.append(name[name_index]+" "+edition[name_index]+","+cart_wrap.text.strip() +" " + condition[count] +"\n")
        count += 1

    listbox = Listbox(root)
    listbox.place(relx=0.5, rely=0.25,relwidth=.75, relheight=.6, anchor='n')

    for item in label_list:
        listbox.insert(END, item)
    label_list = []

    f.close()
# mtg_url functions is to get the URL for mtg_cards function
def mtg_url():
    url = entry.get()
    mtg_cards(url)
#-------------------------------------------------------------------------------
#this is code for the GUI
root = tk.Tk()
#text is a keyword argument
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()
#you can pass in paths here or just put the file name if it is where your code is saved
background_image = tk.PhotoImage(file='mtg_background.png')
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1,relheight=1)

frame_input = tk.Frame(root, bg='#80c1ff', bd=5)
frame_input.place(relx=0.5, rely=0.1,relwidth=.75, relheight=.1, anchor='n')

button = tk.Button(frame_input, text='Enter link', command = lambda: mtg_url())
button.place(relx=.7, relheight=1, relwidth=.30)

entry = tk.Entry(frame_input, font='40')
entry.place(relwidth=.65, relheight=1)

root.mainloop()
