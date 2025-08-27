import time
import logging

from fastapi import FastAPI, Request

from core.api.v1.notifications import router as notifications_router


app = FastAPI(title="notification_service")

app.include_router(notifications_router)


logging.basicConfig(
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s - %(levelname)s - %(message)s"    
)

logger = logging.getLogger("app.middleware")


@app.middleware("http")
async def process_time_logger(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info("%s %s - %.2f мс", request.method, request.url.path, process_time)
    return response