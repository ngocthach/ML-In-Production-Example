from celery import shared_task
from .utils import crawl_website, extract_title, create_logger, detect_sentiment

logger = create_logger(__name__)

@shared_task
def crawl_news_task(url):
    html = crawl_website(url)
    title = extract_title(html)
    logger.info(f"Collected {title}")

    sentiment = detect_sentiment(title)
    logger.info(f"Detect {sentiment}")

    return {"title": title, "sentiment": sentiment}
