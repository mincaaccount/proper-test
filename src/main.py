import os
import re
import requests
from bs4 import BeautifulSoup

PAGE_URL = "https://icanhas.cheezburger.com/"
MEMES_FOLDER = "memes"


def _get_memes_from_page():
    page = requests.get(PAGE_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    image_tags = soup.find_all('img')
    urls = list(filter(lambda k: 'data-src' in str(k) and '/full/' in str(k), image_tags))
    urls = [img['data-src'] for img in urls]

    count = 0
    for i, url in enumerate(urls):
        response = requests.get(url)
        with open(f"{MEMES_FOLDER}/images{i+1}.jpg", "wb+") as f:
            f.write(response.content)
            count += 1
    print("Download complete")


if __name__ == '__main__':
    os.mkdir(MEMES_FOLDER)
    print("Searching URLs")
    _get_memes_from_page()
