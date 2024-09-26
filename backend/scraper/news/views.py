import logging
import time

from celery.result import AsyncResult
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .tasks import crawl_news_task
from .utils import extract_post_request, create_logger

logger = create_logger(__name__)

@require_POST
@csrf_exempt
def crawl_news(request):
    json_data = extract_post_request(request)
    url = json_data.get("url")

    task = crawl_news_task.delay(url)
    return JsonResponse({"task_id": task.id}, status=200)


@csrf_exempt
def get_crawl_result(request, task_id):
    start_time = time.time()
    while True:
        task_result = AsyncResult(task_id)
        task_status = task_result.status
        logger.info(f"Task result: {task_result.result}")

        if task_status == 'PENDING':
            if time.time() - start_time > 60:  # 60 seconds timeout
                return {
                    "task_id": task_id,
                    "task_status": task_result.status,
                    "task_result": task_result.result,
                    "error_message": "Service timeout, retry please"
                }
            else:
                time.sleep(0.5)  # sleep for 0.5 seconds before retrying
        else:
            result = {
                "task_id": task_id,
                "task_status": task_result.status,
                "task_result": task_result.result
            }
            return JsonResponse(result, status=200)
