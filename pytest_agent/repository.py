from datetime import datetime
from typing import Dict

from pytest_agent.database import DBTest
from pytest_agent.drivers import session
from pytest_agent.dtos import TestStatus, TestStatusReadDTO


class TestsRepository:
    @staticmethod
    def update_test_status(fullname: str, status: TestStatus, output: str = None):
        test_instance = session.query(DBTest).filter_by(fullname=fullname).first()
        if test_instance:
            test_instance.status = status.value
            test_instance.output = output
        else:
            test_instance = DBTest(
                fullname=fullname,
                status=status.value,
                refresh_date=datetime.utcnow().timestamp(),
                output=output,
            )
            session.add(test_instance)
        session.commit()

    @staticmethod
    def get_statuses() -> Dict[str, TestStatusReadDTO]:
        tests = session.query(DBTest).all()
        return {test.fullname: TestStatusReadDTO.from_orm(test) for test in tests}

    @staticmethod
    def get_output(fullname: str):
        test_instance = session.query(DBTest).filter_by(fullname=fullname).first()
        if not test_instance:
            return None
        return test_instance.output
