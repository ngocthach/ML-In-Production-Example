from django.urls import path

from . import views

app_name = "news"

urlpatterns = [
    path("crawl", views.crawl_news, name="crawl_news"),
    path("crawl/<str:task_id>", views.get_crawl_result, name="get_crawl_result"),
]
