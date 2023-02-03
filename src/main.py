import os
import requests
from bs4 import BeautifulSoup

PAGE_URL = "https://icanhas.cheezburger.com/"
MEMES_FOLDER = "memes"


def get_next_page_for_memes(page_url, page_count):
    return page_url + "page/" + str(page_count)


def _get_memes_from_page(count):
    urls = get_url_memes_list(PAGE_URL)
    page_count = 2
    while len(urls) <= count:
        next_game_url = get_next_page_for_memes(PAGE_URL, page_count)
        urls += get_url_memes_list(next_game_url)
        page_count += 1

    _saving_memes_in_folder(urls, count)


def get_url_memes_list(page_url):
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    image_tags = soup.find_all('img')
    urls = list(filter(lambda k: 'data-src' in str(k) and '/full/' in str(k), image_tags))
    urls = [img['data-src'] for img in urls]
    return urls


def _saving_memes_in_folder(urls, count):
    for i, url in enumerate(urls[:count]):
        response = requests.get(url)
        with open(f"{MEMES_FOLDER}/images{i + 1}.jpg", "wb+") as f:
            f.write(response.content)
            count += 1
    print("Download complete")


if __name__ == '__main__':
    os.mkdir(MEMES_FOLDER)
    meme_amount = input("How many memes would you like to download?\n")
    print("Searching URLs")
    _get_memes_from_page(int(meme_amount))
