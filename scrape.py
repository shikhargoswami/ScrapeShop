import requests
from bs4 import BeautifulSoup
import threading
import time
import smtplib

class User():

    def __init__(self, email, url, price):

        self.email = email
        self.url = url
        self.price = price
        self.t = None
    
    def start_thread(self, flag=1):

        if flag == 0:

            try:
                self.url = str(self.url)
                website = self.url.split("//")[-1].split('/')[0].split('.')[1]
                # Some websites need to have user-agents to show results
                HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0"}
                page = requests.get(self.url, headers=HEADERS)
                soup = BeautifulSoup(page.content, 'html.parser')
            
            except:
                print("Error Occured!")
                


            if website == 'flipkart':

                title = soup.find("span", attrs={"class": "_35KyD6"}).get_text().strip()
                price = int(soup.find("div", attrs={"class":"_1vC4OE _3qQ9m1"}).get_text()[1:].replace(',', ""))

        
            elif website == 'amazon':

                title = soup.find(id="productTitle").get_text().strip()
                price = soup.find(id="priceblock_dealprice")

                if price != None:
                    price = int(price.get_text()[1:].replace(',', ""))
                if price == None:
                    price = int(soup.find("span", attrs={"id":"priceblock_ourprice"}).get_text()[1:].replace(',', ""))

            if price <= self.price:
                self.send_mail()
                flag=-1
            
            return title, price, flag


        else:
            while(True):
                
                try:
                    self.url = str(self.url)
                    website = self.url.split("//")[-1].split('/')[0].split('.')[1]
                    # Some websites need to have user-agents to show results
                    HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/82.0"}
                    page = requests.get(self.url, headers=HEADERS)
                    soup = BeautifulSoup(page.content, 'html.parser')
                
                except:
                    print("Error Occured!")
                    break


                if website == 'flipkart':

                    title = soup.find("span", attrs={"class": "_35KyD6"}).get_text().strip()
                    price = int(soup.find("div", attrs={"class":"_1vC4OE _3qQ9m1"}).get_text()[1:].replace(',', ""))

            
                elif website == 'amazon':

                    title = soup.find(id="productTitle").get_text().strip()
                    price = soup.find(id="priceblock_dealprice")

                    if price != None:
                        price = int(price.get_text()[1:].replace(',', ""))
                    if price == None:
                        price = int(soup.find("span", attrs={"id":"priceblock_ourprice"}).get_text()[1:].replace(',', ""))

                
                if price <= self.price:
                    self.send_mail()
                    flag =2
                    break
                
            if flag==2:
                return
                time.sleep(60*60*60*4)


                
                

            
                


    # def delete_user_from_db(self):

    #     db.session.query(Database).filter(Database.email== self.email, Database.product_url==self.url).delete()


    def scrape(self):
        title, price, flag = self.start_thread(flag=0)
        if flag== -1:
            return title, price
        else:
            self.t = threading.Thread(target=self.start_thread)
            self.t.start()
        return title, price
    

    def send_mail(self):

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()

            server.login('goshigo23@gmail.com', 'bdryaouqjwrdoape')
        except:
            print('Error!!!!')

        subject = 'Price fell down!'
        body = f"Hey there from ScrapeShop! The price of your product fell down.\nCheck your product link: {self.url}"

        msg = f"Subject: {subject}\n\n{body}"

        server.sendmail('goshigo23@gmail.com', self.email, msg)
        print('Email has been sent')
        server.quit()


        
#if __name__=="__main__":
