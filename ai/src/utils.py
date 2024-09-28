import logging

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


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
