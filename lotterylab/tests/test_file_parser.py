from datetime import date
from src.data_acquisition.file_parser import parse_initial_txt


def test_parse_initial_txt_basic():
    lines = [
        "1. 27.01.1957 8,12,31,39,43,45",
        "2. 03.02.1957 5,10,11,22,25,27",
    ]
    parsed = list(parse_initial_txt(lines))
    assert len(parsed) == 2
    assert parsed[0].draw_number == 1
    assert parsed[0].draw_date == date(1957, 1, 27)
    assert parsed[0].numbers == [8, 12, 31, 39, 43, 45]


def test_parse_initial_txt_ignores_invalid():
    lines = [
        "bad line",
        "3. 10.02.1957 18,19,20,26,45,49",
        "4. bad-date 1,2,3,4,5,6",
    ]
    parsed = list(parse_initial_txt(lines))
    assert len(parsed) == 1
    assert parsed[0].draw_number == 3
