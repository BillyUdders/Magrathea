import io
import uuid

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from loguru import logger
from pydantic import BaseModel
from sqlalchemy.orm import Session

from magrathea.database import get_db
from magrathea.maps.map import Map
from magrathea.maps.rendering_engine import render_map_to_buffer

map_router = APIRouter()


class MapRequest(BaseModel):
    size: int = 128
    octaves: int = 4
    seed: int | None = None


class MapResponse(BaseModel):
    id: str
    url: str


@map_router.post("/maps", response_model=MapResponse)
def create_map(request: MapRequest, db: Session = Depends(get_db)) -> MapResponse:  # noqa: B008
    """Generates a map and stores it in the database."""
    logger.info(
        f"POST /maps: size={request.size}, octaves={request.octaves}, "
        f"seed={request.seed}"
    )
    try:
        # Generate the map buffer
        buf = render_map_to_buffer(request.size, request.octaves, seed=request.seed)

        # Create a unique ID
        map_id = str(uuid.uuid4())

        # Create DB record
        new_map = Map(
            id=map_id,
            size=request.size,
            octaves=request.octaves,
            seed=request.seed,
            data=buf.getvalue(),
        )

        db.add(new_map)
        db.commit()
        db.refresh(new_map)

        logger.info(f"Map created successfully. ID: {map_id}")
        return MapResponse(id=map_id, url=f"/maps/{map_id}")
    except Exception as e:
        logger.error(f"Failed to create map: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@map_router.get("/maps/{map_id}")
def get_map(map_id: str, db: Session = Depends(get_db)) -> StreamingResponse:  # noqa: B008
    """Retrieves a generated map by ID."""
    logger.debug(f"Retrieving map with ID: {map_id}")

    map_record = db.query(Map).filter(Map.id == map_id).first()

    if not map_record:
        logger.warning(f"Map ID not found: {map_id}")
        raise HTTPException(status_code=404, detail="Map not found")

    # Create buffer from binary data
    assert map_record.data is not None
    buf = io.BytesIO(map_record.data)

    # Return as streaming response
    return StreamingResponse(buf, media_type="image/png")
