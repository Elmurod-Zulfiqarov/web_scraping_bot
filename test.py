import requests
from bs4 import BeautifulSoup

search = 'telefon'
url = f"https://asaxiy.uz/product?key={search}"

page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

products = list(soup.find("div", class_="custom-gutter").find_all("div", recursive=False))[:10]
for item in products:
    # text = ""

    # img = item.find("img", class_="img-fluid lazyload").get("data-src")
    # if img[-5:]=='.webp':
    #     img = img[:-5]
    # print(img)

    title = str(item.find("h5", class_="product__item__info-title").text)
    print(title)
    # text += title + "\n\n" 

    old_price = item.find("div", class_="product__item-old--price")
    if old_price:
        old_price_text = old_price.text
        text += f"<strike>{old_price_text}</strike> \n\n"
        print(old_price_text)

    price = str(item.find("div", class_="produrct__item-prices--wrapper").text)
    print(price)
    # text += price + "\n\n" 

    # link = "https://asaxiy.uz" + str(item.find("a", class_="title__link").get("href"))
    # print(link)
    # text += link

