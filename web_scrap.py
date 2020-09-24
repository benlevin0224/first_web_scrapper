import urllib.request, urllib.parse, urllib.error
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

#https://stackoverflow.com/questions/16627227/http-error-403-in-python-3-web-scraping
#The website blocked the normal urllib request function so had to use FancyURLopener
#solution is in the comment above
class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"
opener = AppURLopener()
response = opener.open('https://www.cardkingdom.com/catalog/search?search=header&ac=1&filter%5Bname%5D=Mirari%27s%20Wake')
soup = BeautifulSoup(response, 'html.parser')


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
    count += 1
f.close()
