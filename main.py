# stdlib
import json
import logging

# thirdparty
import uvicorn
from fastapi import APIRouter, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from starlette.responses import JSONResponse, RedirectResponse

# project
import settings
from routers.players import players_router
from settings import PrometheusMiddleware, metrics, setting_otlp
from utils.helpers import (
    CustomHTTPException,
    custom_exception_handler,
    general_exception_handler,
    validate_mini_app_data,
    validation_exception_handler,
)

root_router = APIRouter(prefix="/api/v1")


app = FastAPI(title="Mini-App-API", version="0.0.1")


@app.middleware("http")
async def data_validation_middleware(request: Request, call_next):
    if request.method in ["POST", "PUT"]:
        body = await request.json()
        initData = body.get("initData")

        if not initData:
            return JSONResponse(status_code=401, content="UNAUTHORIZED")

        is_valid, data = validate_mini_app_data(initData)

        if not is_valid:
            return JSONResponse(status_code=401, content="UNAUTHORIZED")

        user = json.loads(data.get("user"))

        user_id = user.get("id")
        username = user.get("username", "")
        first_name = user.get("first_name", "")

        if not user_id:
            return JSONResponse(status_code=401, content="UNAUTHORIZED")

        body["player_id"] = user_id
        body["username"] = username
        body["first_name"] = first_name

        request._body = json.dumps(body).encode("utf-8")

    response = await call_next(request)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

root_router.include_router(players_router)

app.include_router(root_router)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1


class Non200Filter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return not record.getMessage().endswith("200")


logging.getLogger("uvicorn.access").addFilter(EndpointFilter())
logging.getLogger("uvicorn.access").addFilter(Non200Filter())

app.add_middleware(PrometheusMiddleware, app_name="mini-app-api")
app.add_route("/metrics", metrics)

setting_otlp(app, "mini-app-api", settings.OTLP_GRPC_ENDPOINT)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(CustomHTTPException, custom_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


def openapi_specs():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Mini App",
        version="1.0.0",
        description="Mini App API Open-API Specification",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = openapi_specs

if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = (
        "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] "
        "[trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
    )
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=log_config)
