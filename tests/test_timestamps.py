import time
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from magrathea.main import Base
from magrathea.maps.map import Map


def test_timestamps() -> None:
    # Use in-memory database for this test
    engine = create_engine("sqlite:///:memory:")
    session_local = sessionmaker(bind=engine)

    # Ensure tables are created
    Base.metadata.create_all(bind=engine)

    db = session_local()
    try:
        # Create a new map
        map_id = "test_timestamp_map"
        new_map = Map(id=map_id, size=100, octaves=4, data=b"fake data")
        db.add(new_map)
        db.commit()
        db.refresh(new_map)

        assert new_map.created_at is not None
        assert new_map.updated_at is not None
        assert isinstance(new_map.created_at, datetime)

        created_at_initial = new_map.created_at
        updated_at_initial = new_map.updated_at

        # Wait a bit to ensure a different timestamp
        time.sleep(1.1)

        # Update the map
        new_map.size = 200
        db.commit()
        db.refresh(new_map)

        assert new_map.size == 200
        # Check that updated_at increased
        assert new_map.updated_at > updated_at_initial
        # Check that created_at stayed the same
        assert new_map.created_at == created_at_initial
    finally:
        db.close()
