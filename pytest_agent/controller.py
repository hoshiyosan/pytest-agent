import select
import subprocess
from typing import List

from pytest_agent.drivers import executor
from pytest_agent.dtos import TestStatus
from pytest_agent.repository import TestsRepository
from pytest_agent.styling import cli_style_to_html


def execute_command(command: str, capture_stderr=False) -> int:
    # wrap command execution with "script" command to mock a real terminal and retrieve styling
    process = subprocess.Popen(
        ["script", "-e", "-q", "-c", command],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE if capture_stderr else None,
    )

    # simultaneously read stdin and stdout to get both in same output variable
    output = b""

    while True:
        reads = [process.stdout.fileno()]
        if capture_stderr:
            reads.append(process.stderr.fileno())

        ret = select.select(reads, [], [])

        for fd in ret[0]:
            if fd == process.stdout.fileno():
                output += process.stdout.readline()
            if capture_stderr and fd == process.stderr.fileno():
                output += process.stderr.readline()

        if process.poll() != None:
            break

    print(output)

    return cli_style_to_html(output.decode("utf-8")), process.returncode


class TestsController:
    @staticmethod
    def run_test(test_fullname: str):
        output, returncode = execute_command(
            f"python -m pytest -v {test_fullname}", capture_stderr=True
        )
        new_status = TestStatus.SUCCEED if returncode == 0 else TestStatus.FAILED
        TestsRepository.update_test_status(
            fullname=test_fullname, status=new_status, output=output
        )

    @classmethod
    def schedule_tests(cls, test_fullnames: List[str]):
        for test_fullname in test_fullnames:
            TestsRepository.update_test_status(
                fullname=test_fullname, status=TestStatus.PENDING
            )

        for test_fullname in test_fullnames:
            executor.submit(cls.run_test, test_fullname)
