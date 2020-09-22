import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

url = 'https://www.newegg.com/p/pl?d=gaming+monitors&N=600554755%20100898493'
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, 'html.parser')
containers = soup.findAll("div",{"class":"item-container"})
container = containers[0]

filename = "products.csv"
f = open(filename, "w")
headers = "brand, product_name, shipping\n"
f.write(headers)

for container in containers:
    brand = container.div.div.a.img["alt"]

    title_container = container.findAll("a",{"class":"item-title"})
    product_name = title_container[0].text

    shipping_container = container.findAll("li",{"class":"price-ship"})
    shipping = shipping_container[0].text.strip()

    print("brand: " + brand)
    print("product name: " + product_name)
    print("shipping: " + shipping)
    f.write(brand + "," +product_name.replace(","," ") + "," + shipping + "\n")
f.close()
