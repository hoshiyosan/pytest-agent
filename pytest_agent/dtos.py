from enum import Enum

import pydantic


class BaseModel(pydantic.BaseModel):
    class Config:
        orm_mode = True


class TestStatus(Enum):
    RUNNING = "running"
    PENDING = "pending"
    FAILED = "failed"
    SUCCEED = "succeed"


class TestStatusReadDTO(BaseModel):
    status: TestStatus
    refresh_date: float
