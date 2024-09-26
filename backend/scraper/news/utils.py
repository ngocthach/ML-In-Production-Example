import json
import logging
import requests
from bs4 import BeautifulSoup


def extract_post_request(request):
    try:
        return json.loads(request.body.decode('utf-8'))
    except ValueError as err:
        logging.error(err)
        return {}


def crawl_website(url):
    response = requests.get(url)
    response.raise_for_status()  # Raises an error for bad responses (4xx or 5xx)
    return response.content


def extract_title(html):
    soup = BeautifulSoup(html, "html.parser")

    try:
        title = soup.find('h1', class_='title-detail').text.strip()
    except AttributeError:
        title = 'N/A'

    return title


def create_logger(name, level=logging.DEBUG):
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s")
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(logging.StreamHandler())
    return logger


if __name__ == '__main__':
    result = crawl_website("https://vnexpress.net/chuyen-gia-sinh-vien-it-nen-lam-viec-truoc-hoc-thac-si-4790805.html")
    print(extract_title(result))