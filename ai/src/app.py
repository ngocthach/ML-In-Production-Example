import logging
import time

from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse

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


@app.get("/v1/test")
async def root():
    return {"message": "Hello World"}


@app.post("/v1/detect")
async def detect(input_data: dict):
    t0 = time.time()
    text = input_data.get("text")
    if text:
        try:
            result = predict(text)[0]
            result['runtime'] = int((time.time() - t0) * 1000)
            return result
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": f"Error predict {text}: {str(e)}"})
    else:
        return JSONResponse(status_code=400, content={"message": "Input is empty"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
