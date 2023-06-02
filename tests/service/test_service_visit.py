from datetime import datetime
import pytest

from tests.fixtures import test_app, dummy_db, visit_service
from src.service.visit import VisitService


def test_visit_get(visit_service: VisitService):
    visit = visit_service.get_visit(2)
    assert visit.date == datetime(2023, 5, 1, 22, 12, 00)

    with pytest.raises(ValueError):
        visit_service.get_visit(50)

def test_visit_get_all(visit_service: VisitService):
    assert len(visit_service.get_all_visits()) == 16

def test_visit_get_filtered(visit_service: VisitService):
    assert len(visit_service.get_all_visits(short_url='exMpL')) == 4

def test_visit_create(visit_service: VisitService):
    visit = visit_service.create_visit(short_url="gitHB")

    assert len(visit_service.get_all_visits()) == 17
