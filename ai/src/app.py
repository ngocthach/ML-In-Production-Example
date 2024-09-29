import logging
import time

from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse

from utils import crawl_website, extract_title
from model import predict


app = FastAPI(
    title="Sentiment Classify API",
    description="This API allows sentiment.",
    version="1.0.0",
    contact={
        "name": "Thach Le",
        "email": "thach.le.tech@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

logger = logging.getLogger("sentiment")
logging.basicConfig(level=logging.INFO)




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
