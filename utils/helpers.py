# stdlib
import hashlib
import hmac
import traceback
from datetime import date, datetime
from urllib.parse import unquote

# thirdparty
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError

# project
import settings
from settings import logger
from utils.errors import ErrorResponseEnum


def response_wrapper_result(result, status_code=status.HTTP_200_OK):
    response = {"result": jsonable_encoder(result)}
    return JSONResponse(content=response, status_code=status_code)


def response_wrapper_results(results, status_code=status.HTTP_200_OK, pagination=None):
    response = {"results": jsonable_encoder(results)}
    if pagination:
        response["pagination"] = pagination
    return JSONResponse(content=response, status_code=status_code)


def validate_mini_app_data(data: str):  # noqa
    vals = {k: unquote(v) for k, v in [s.split("=", 1) for s in data.split("&")]}
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(vals.items()) if k != "hash")

    secret_key = hmac.new("WebAppData".encode(), settings.BOT_TOKEN.encode(), hashlib.sha256).digest()
    h = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256)
    return h.hexdigest() == vals["hash"], vals


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


class CustomHTTPException(Exception):
    def __init__(self, error_response: ErrorResponseEnum):
        self.error_response = error_response


class PaginationModel(BaseModel):
    page: int
    pages: int
    on_page: int
    results: int


def generate_error_response_content(
    error_response: ErrorResponseEnum, exc: ValidationError = None, traceback: str = None
):
    response = dict(code=error_response.name, message=error_response.detail)

    if exc:
        response.update(dict(details=exc.errors()))

    if traceback and settings.TRACEBACK_OUTPUT_ENABLED:
        response.update(dict(traceback=traceback))

    return jsonable_encoder(response)


def get_custom_error_response(error_response: ErrorResponseEnum):
    return JSONResponse(
        status_code=error_response.http_code.value,
        content=generate_error_response_content(error_response=error_response),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=ErrorResponseEnum.INVALID_QUERY_PARAMETERS.http_code.value,
        content=generate_error_response_content(error_response=ErrorResponseEnum.INVALID_QUERY_PARAMETERS, exc=exc),
    )


async def custom_exception_handler(request: Request, exc: CustomHTTPException):
    return JSONResponse(
        status_code=exc.error_response.http_code.value,
        content=generate_error_response_content(error_response=exc.error_response),
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"Error: {exc}\n{traceback.format_exc()}")

    return JSONResponse(
        status_code=ErrorResponseEnum.SOMETHING_WENT_WRONG.http_code.value,
        content=generate_error_response_content(
            error_response=ErrorResponseEnum.SOMETHING_WENT_WRONG, traceback=traceback.format_exc()
        ),
    )
