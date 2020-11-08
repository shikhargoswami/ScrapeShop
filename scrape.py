
import requests
from bs4 import BeautifulSoup



def scrape(url):

    try:
        url = str(url)
        website = url.split("//")[-1].split('/')[0].split('.')[1]
        # Some websites need to have user-agents to show results
        HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0"}
        page = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(page.content, 'html.parser')

    except:
        print("Error Occured")

    if website == 'flipkart':

        title = soup.find("span", attrs={"class": "_35KyD6"}).get_text().strip()
        price = soup.find("div", attrs={"class":"_1vC4OE _3qQ9m1"}).get_text()

     
    elif website == 'amazon':
        title = soup.find(id="productTitle").get_text().strip()
        price = soup.find(id="priceblock_dealprice")

        if price != None:
            price = price.get_text()
        if price == None:
            price = soup.find("span", attrs={"id":"priceblock_ourprice"}).get_text()
        

        
    # print(title)
    # print(price)
    
    return title, int(price[1:].replace(',',''))


