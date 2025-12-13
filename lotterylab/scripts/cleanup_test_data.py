#!/usr/bin/env python3
"""
Cleanup script to remove test data from the database.
Test records have draw_number > 900000 (e.g., 999997, 999998).
"""

from src.database.session import SessionLocal
from src.database.models import Draw
from sqlalchemy import delete, select, func


def cleanup_test_data():
    """Remove test records with draw_number > 900000."""
    with SessionLocal() as session:
        # First, show what will be deleted
        test_records = session.execute(
            select(Draw).where(Draw.draw_number > 900000)
        ).scalars().all()
        
        if not test_records:
            print("[OK] No test records found. Database is clean.")
            return
        
        print(f"[FOUND] {len(test_records)} test records to delete:")
        for record in test_records:
            print(f"   #{record.draw_number} | {record.draw_date} | {record.game_type} | {record.numbers}")
        
        # Delete them
        result = session.execute(delete(Draw).where(Draw.draw_number > 900000))
        deleted_count = result.rowcount
        session.commit()
        
        print(f"\n[DELETED] {deleted_count} test records")
        
        # Verify final state
        max_id = session.execute(select(func.max(Draw.draw_number))).scalar()
        total = session.execute(select(func.count(Draw.id))).scalar()
        print(f"[STATS] Database now has {total} records, max draw_number = {max_id}")


if __name__ == "__main__":
    cleanup_test_data()

