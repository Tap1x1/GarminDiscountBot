import requests
from bs4 import BeautifulSoup
import lxml
import json


def get_data():

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }
    s = requests.Session()
    url = "https://www.garmin.ru/watches/catalog/"

    response = s.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    result_data = []
    watch_items = soup.find("ul", class_="list-elements-box").find_all("li", class_="element")

    for bi in watch_items:
        watch_data = bi.find_all("div", class_="body")
        try:
            watch_model = watch_data[0].find("div", class_="name").text.strip()
        except:
                watch_model = "Название модели отсутствует!"

        try:
            watch_link = watch_data[0].find("a", class_="detail").get("href")
        except:
            watch_link = "No link!"

        try:
            watch_price = watch_data[0].find("div", class_="price").text.strip()
        except:
            watch_price = "Цена отсутствует(перейдите по ссылке для информации)"

        try:
            watch_skidka = bi.find("div", class_="skidkagift").text.strip()
        except:
            watch_skidka = "Товар без скидки!"

        result_data.append(
            {
                "link": (f"https://www.garmin.ru/{watch_link}"),
                "title": watch_model,
                "price": watch_price,
                "discount": watch_skidka
            }
        )
    with open("result_data.json", "w", encoding="utf-8") as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)


def main():
    get_data()


if __name__ == '__main__':
    main()






