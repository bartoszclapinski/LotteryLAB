from datetime import date, timedelta
from src.data_acquisition.file_parser import ParsedDraw
from src.data_acquisition.data_validator import validate_draw


def test_validate_ok():
    d = ParsedDraw(draw_number=10, draw_date=date.today() - timedelta(days=1), numbers=[1,2,3,4,5,6])
    res = validate_draw(d)
    assert res.ok


def test_validate_fails_range():
    d = ParsedDraw(draw_number=1, draw_date=date.today(), numbers=[0,2,3,4,5,6])
    res = validate_draw(d)
    assert not res.ok


def test_validate_fails_unique():
    d = ParsedDraw(draw_number=1, draw_date=date.today(), numbers=[1,1,2,3,4,5])
    res = validate_draw(d)
    assert not res.ok


def test_validate_future_date():
    d = ParsedDraw(draw_number=1, draw_date=date.today() + timedelta(days=1), numbers=[1,2,3,4,5,6])
    res = validate_draw(d)
    assert not res.ok
