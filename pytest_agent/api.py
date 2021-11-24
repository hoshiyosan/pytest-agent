"""
Defines API endpoints and policy.
"""
from typing import Dict, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import PlainTextResponse

from pytest_agent.controller import TestsController
from pytest_agent.dtos import TestStatusReadDTO
from pytest_agent.repository import TestsRepository

api = FastAPI(
    title="Pytest Agent API",
    description="Expose testing features and metrics via a REST API.",
    version="v1",
    docs_url="/",
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.post("/tests/collect", response_model=Dict[str, TestStatusReadDTO])
def collect_and_update_tests():
    """
    collect_and_update_tests
    """
    TestsController.collect_and_update_tests()
    return TestsRepository.get_statuses()


@api.get("/tests/status", response_model=Dict[str, TestStatusReadDTO])
def get_tests_statuses():
    """
    get_tests_statuses
    """
    return TestsRepository.get_statuses()


@api.post("/tests/run", response_model=Dict[str, TestStatusReadDTO])
def run_tests_statuses(test_fullnames: List[str]):
    """
    run_tests_statuses
    """
    TestsController.schedule_tests(test_fullnames)
    return TestsRepository.get_statuses()


@api.get("/tests/output/{test_fullname:path}")
def get_test_output(test_fullname: str):
    """
    get_test_output
    """
    output = TestsRepository.get_output(test_fullname)
    if output is None:
        return None
    return PlainTextResponse(output)
