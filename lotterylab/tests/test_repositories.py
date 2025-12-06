from datetime import date, timedelta
from src.database.session import SessionLocal
from src.repositories.draws import DrawRepository


def test_repo_list_and_count():
    with SessionLocal() as s:
        repo = DrawRepository(s)
        total = repo.count()
        items = repo.list(limit=5)
    assert total >= 0
    assert len(items) <= 5


def test_repo_latest():
    with SessionLocal() as s:
        repo = DrawRepository(s)
        rows = repo.latest(10)
    assert len(rows) <= 10
    # ensure descending by draw_number if at least 2
    if len(rows) >= 2:
        assert rows[0]["draw_number"] >= rows[1]["draw_number"]


def test_repo_filter_by_game_type():
    """Test filtering draws by game type."""
    with SessionLocal() as s:
        repo = DrawRepository(s)
        lotto_items = repo.list(game_type="lotto", limit=5)
        lotto_plus_items = repo.list(game_type="lotto_plus", limit=5)

    # All lotto items should be lotto type
    for item in lotto_items:
        assert item["game_type"] == "lotto"

    # All lotto_plus items should be lotto_plus type
    for item in lotto_plus_items:
        assert item["game_type"] == "lotto_plus"


def test_repo_date_filtering():
    """Test filtering draws by date range."""
    with SessionLocal() as s:
        repo = DrawRepository(s)
        today = date.today()
        month_ago = today - timedelta(days=30)

        # Get draws from last 30 days
        recent_items = repo.list(date_from=month_ago, date_to=today, limit=10)

        # All returned draws should be within the date range
        for item in recent_items:
            # draw_date is returned as ISO string, convert back to date
            item_date = date.fromisoformat(item["draw_date"])
            assert month_ago <= item_date <= today


def test_repo_pagination():
    """Test pagination works correctly."""
    with SessionLocal() as s:
        repo = DrawRepository(s)
        total_count = repo.count()

        # Get first page
        page1 = repo.list(limit=5, offset=0)
        # Get second page
        page2 = repo.list(limit=5, offset=5)

        assert len(page1) <= 5
        assert len(page2) <= 5

        # Pages should be different (unless we don't have enough data)
        if total_count > 5:
            assert page1 != page2


def test_repo_count_matches_list():
    """Test that count() with filters matches list() with same filters."""
    with SessionLocal() as s:
        repo = DrawRepository(s)
        
        # Test with a specific game_type filter to get manageable count
        lotto_count = repo.count(game_type="lotto")
        lotto_items = repo.list(game_type="lotto", limit=lotto_count + 100)
        
        # Count should match filtered list length (up to the limit we set)
        assert lotto_count == len(lotto_items) or len(lotto_items) == lotto_count
