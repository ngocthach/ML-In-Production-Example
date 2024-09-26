import logging

from celery import shared_task
from .utils import crawl_website, extract_title

logger = logging.getLogger(__name__)

@shared_task
def crawl_news_task(url):
    html = crawl_website(url)
    title = extract_title(html)

    logger.info(f"Collected {title}")
    return {"title": title}
