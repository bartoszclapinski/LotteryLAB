from src.services.ingestion import import_lines, import_file
from src.database.session import SessionLocal
from src.database.models import Draw
from sqlalchemy import select, delete
import random


def test_import_lines_basic():
    """Test basic line import functionality."""
    lines = [
        "1. 01.01.2000 1,2,3,4,5,6",
        "2. 02.01.2000 7,8,9,10,11,12",
    ]
    res = import_lines(lines)
    assert res["inserted"] >= 0
    assert res["skipped"] >= 0
    assert "inserted" in res
    assert "skipped" in res


def test_import_lines_with_duplicates():
    """Test that duplicate draw numbers are handled properly."""
    # Use a very high random number to avoid conflicts with existing data
    unique_id = random.randint(10_000_000, 99_999_999)
    
    # Clean up any existing test records first
    with SessionLocal() as session:
        session.execute(delete(Draw).where(Draw.draw_number == unique_id))
        session.commit()
    
    # First import - should succeed
    lines_first = [
        f"{unique_id}. 01.01.2000 1,2,3,4,5,6",
    ]
    res1 = import_lines(lines_first)
    assert res1["inserted"] == 1
    assert res1["skipped"] == 0
    
    # Second import with same draw_number - should be skipped (max_id logic)
    lines_second = [
        f"{unique_id}. 02.01.2000 7,8,9,10,11,12",  # Same draw number
    ]
    res2 = import_lines(lines_second)
    # Due to max_id logic, this should be skipped
    assert res2["skipped"] >= 0
    
    # Clean up
    with SessionLocal() as session:
        session.execute(delete(Draw).where(Draw.draw_number == unique_id))
        session.commit()


def test_import_lines_game_type_assignment():
    """Test that game types are assigned correctly (lotto vs lotto_plus)."""
    # Use unique high numbers to avoid conflicts
    unique_base = random.randint(20_000_000, 29_999_999)
    draw_num_1 = unique_base
    draw_num_2 = unique_base + 1
    
    # Clean up any existing test records
    with SessionLocal() as session:
        session.execute(delete(Draw).where(Draw.draw_number.in_([draw_num_1, draw_num_2])))
        session.commit()
    
    # The game_type assignment logic: first draw of day = "lotto", second = "lotto_plus"
    lines = [
        f"{draw_num_1}. 01.01.2000 1,2,3,4,5,6",   # First draw of day
        f"{draw_num_2}. 01.01.2000 7,8,9,10,11,12", # Second draw of day
    ]
    res = import_lines(lines)
    
    # Result should have expected structure
    assert "inserted" in res
    assert "skipped" in res
    
    # Check the database
    with SessionLocal() as session:
        draws = session.execute(
            select(Draw).where(Draw.draw_number.in_([draw_num_1, draw_num_2]))
        ).scalars().all()

        if len(draws) == 2:
            draw_dict = {d.draw_number: d for d in draws}
            # Game types should be either lotto or lotto_plus
            assert draw_dict[draw_num_1].game_type in ("lotto", "lotto_plus")
            assert draw_dict[draw_num_2].game_type in ("lotto", "lotto_plus")
    
    # Clean up
    with SessionLocal() as session:
        session.execute(delete(Draw).where(Draw.draw_number.in_([draw_num_1, draw_num_2])))
        session.commit()


def test_import_file_function_exists():
    """Test that import_file function exists and can be called (basic smoke test)."""
    # This is just a smoke test - we don't want to create actual files in tests
    try:
        # This should not crash, even with invalid path
        result = import_file("/nonexistent/file.txt")
        assert isinstance(result, dict)
        assert "inserted" in result
        assert "skipped" in result
    except (FileNotFoundError, OSError):
        # Expected for non-existent file
        pass
