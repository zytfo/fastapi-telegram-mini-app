# stdlib
from typing import Generic, List, Optional, TypeVar

# thirdparty
from pydantic import BaseModel

# project
from utils.helpers import PaginationModel

M = TypeVar("M", bound=BaseModel)


class ResultResponse(BaseModel, Generic[M]):
    result: M


class ResultsResponse(BaseModel, Generic[M]):
    results: List[M]
    pagination: Optional[PaginationModel] = None


class CommonResponseSchema(BaseModel):
    success: str


class CeleryTaskSchema(BaseModel):
    task_id: str
