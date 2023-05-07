from selenium import webdriver
from bs4 import BeautifulSoup
import csv

path = "C:/chromedriver.exe"
browser = webdriver.Chrome(executable_path=path)

def write_csv(ads):
    with open('D:\\result.csv','a',encoding='utf-8') as f:
        fields = ['title', 'price', 'url', 'review', 'rating']
        writer = csv.DictWriter(f, fieldnames=fields)
        for ad in ads:
            writer.writerow(ad)
        

def get_html(url):
     browser.get(url)
     return browser.page_source

def scrape_data(card):
        try:
            h2 = card.h2
        except:
            title = ''
            url = ''
        else:
            title = h2.text.strip()
            url = h2.a.get('href')
        
        try:
            price = card.find('span', class_='a-price-whole').text.strip('.').strip()
        except:
            price = ''
        else:
            price = ''.join(price.split(','))
        
        try:
            review =card.find('span' ,class_="a-size-base s-underline-text").text.strip()
        except:
            review = ''
        else:
            review = ''.join(review.split(','))

        try:
            rating = card.find('span', class_='a-icon-alt').text.strip()
        except:
            rating = ''
        else:
            rating = ''.join(rating.split())
        
        data = {'title':title, 'url': url, 'price': price, 'review': review, 'rating': rating}
        return data



def main():
    ads_data = []
    for i in range(1,21):
          url  = f'https://www.amazon.in/s?k=bags&page={i}&crid=2M096C61O4MLT&qid=1675792071&sprefix=ba%2Caps%2C283&ref=sr_pg_1'
          html = get_html(url)
          soup = BeautifulSoup(html, 'lxml')
          cards = soup.find_all('div', {'data-asin':True, 'data-component-type':'s-search-result'})
          for card in cards:
            data = scrape_data(card)
            ads_data.append(data)

    write_csv(ads_data)

if __name__=='__main__':
    main()

