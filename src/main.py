import os
from queue import Queue
import multiprocessing
import requests
from bs4 import BeautifulSoup

PAGE_URL = "https://icanhas.cheezburger.com/"
MEMES_FOLDER = "memes"
THREADS = 0
q = Queue()


def get_next_page(page_url, page_count):
    return page_url + "page/" + str(page_count)


def _get_memes_from_page(count):
    urls = get_url_memes_list(PAGE_URL)
    page_count = 2
    while len(urls) <= count:
        next_game_url = get_next_page(PAGE_URL, page_count)
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
    jobs = []

    while True:
        THREADS = int(input("How many threads would you like to use? (1 min, 5 max)\n"))
        if 1 <= THREADS <= 5:
            break

    while True:
        meme_amount = int(input("How many memes would you like to download?\n"))
        if meme_amount > 0:
            _get_memes_from_page(meme_amount)
            break
        if meme_amount <= 0:
            print("Please submit a valid number")
