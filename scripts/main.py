import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import dotenv
import os

# Load .env variables
dotenv.load_dotenv()
USER_AGENT = os.environ.get('USER_AGENT')
CHROME_DRIVER_PATH = os.environ.get('CHROME_DRIVER_PATH')

headers = {'User-Agent': USER_AGENT}

options = Options()
options.headless = True

driver = webdriver.Chrome(
    executable_path=CHROME_DRIVER_PATH, options=options)


barcode = input("Please Enter the Barcode: ")


def getTrendyolRating(item):

    stars = item.select('.star-w .full')

    total = 0

    if stars:
        for i in stars:
            total += (float(i['style'].split(";")
                      [0].replace("width:", "").replace("%", "")))

    rating = (total / 100)

    return rating


def getTrendyolPrice(barcode):

    response = requests.get(
        'https://www.trendyol.com/sr?q={0}&qt={0}&st={0}&os=1&sst=PRICE_BY_ASC'.format(barcode), headers=headers)
    html = response.text
    soup = BeautifulSoup(html, "lxml")

    products = soup.find_all(class_='card-border')

    for item in products:

        rating = getTrendyolRating(item)

        return (item.find(class_='prc-box-dscntd').text), rating

    return "Not Found...", rating


def getCiceksepetiPrice(barcode):

    response = requests.get(
        'https://www.ciceksepeti.com/arama?orderby=3&query={}'.format(barcode), headers=headers)
    html = response.text

    if "search-not-found__img" in html:
        return "Not Found..."

    soup = BeautifulSoup(html, "lxml")

    products = soup.find_all(class_='products__item')

    for item in products:
        return (item.find(class_='price--now').text.replace("  ", ""))

    return "Not Found..."


def getHepsiburadaRating(item):
    stars = item.select('ul[data-baseweb="star-rating"] > li > div')

    total = 0

    if stars:
        for i in stars:
            total += (float(i['width'].replace("%", "")))

    rating = (total / 100)

    return rating


def getHepsiburadaPrice(barcode):
    response = requests.get(
        'https://www.hepsiburada.com/ara?q={}&siralama=artanfiyat'.format(barcode), headers=headers)
    html = response.text
    soup = BeautifulSoup(html, "lxml")

    products = soup.select('li[class*="productListContent"]')

    for item in products:
        rating = getHepsiburadaRating(item)
        return (item.select('div[data-test-id="price-current-price"]')[0].text), rating

    return "Not Found...", rating


def getAmazonRating(item):

    stars = item.select('span[aria-label*="5 yıldız üzerinden"]')

    total = 0

    if stars:
        total = float(item.select('span[aria-label*="5 yıldız üzerinden"]')[
                      0]['aria-label'].replace("5 yıldız üzerinden ", "").replace(",", "."))

    return total


def getAmazonPrice(barcode):
    # Since 403 error
    # response = requests.get('https://www.amazon.com.tr/s?k={0}&s=price-asc-rank&__mk_tr_TR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=11ETR7ATNW841&qid=1683313772&sprefix={0}%2Caps%2C183&ref=sr_st_price-asc-rank&ds=v1%3AePxaQMjuV%2BQNbgIsG%2BxTvvZ9fsPkXTwTesAFlG6S1vc'.format(barcode),headers=headers)
    # html = response.text
    # Headless seleium is used.

    driver.get('https://www.amazon.com.tr/s?k={0}&s=price-asc-rank&__mk_tr_TR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=11ETR7ATNW841&qid=1683313772&sprefix={0}%2Caps%2C183&ref=sr_st_price-asc-rank&ds=v1%3AePxaQMjuV%2BQNbgIsG%2BxTvvZ9fsPkXTwTesAFlG6S1vc'.format(barcode))

    html = driver.page_source

    if "builder-no-results" in html:
        return "Not Found..."

    soup = BeautifulSoup(html, "lxml")

    products = soup.select('div[data-component-type="s-search-result"]')

    for item in products:
        rating = getAmazonRating(item)
        return (item.select('span.a-price .a-offscreen')[0].text), rating

    return "Not Found...", rating


print("""
Trendyol    ---> {0}
Hepsiburada ---> {1}
Amazon      ---> {2}
Çiçeksepeti ---> {3}
      """.format(getTrendyolPrice(barcode), getHepsiburadaPrice(barcode), getAmazonPrice(barcode), getCiceksepetiPrice(barcode)))
