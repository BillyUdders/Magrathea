from fastapi import APIRouter, Request, Response

# from fastapi.templating import TemplateResponse
from pydantic import BaseModel

from magrathea.templates import templates

# from magrathea.database import get_db
# from magrathea.maps.map import Map
# from magrathea.maps.rendering_engine import render_map_to_buffer

map_router = APIRouter()


class MapRequest(BaseModel):
    size: int
    seed_height: int
    seed_heat: int
    seed_wet: int


class MapResponse(BaseModel):
    id: str
    url: str


@map_router.get("/map")
async def form(request: Request) -> Response:
    return templates.TemplateResponse("map_form.html", {"request": request})


@map_router.post("/map_create")
async def create(request: Request, map_request: MapRequest) -> Response:
    # map = WorldMap(
    #     size=map_request.size,
    #     seed_height=map_request.seed_height,
    #     seed_heat=map_request.seed_heat,
    #     seed_wet=map_request.seed_wet,
    # )

    return templates.TemplateResponse("map_response.html", {"request": request})


@map_router.post("/map_view")
async def view_map() -> None:
    pass


# @map_router.get("/map", response_class=StreamingResponse)
# def quick_generate_map(
#     size: int = 128,
#     octaves: int = 4,
#     seed: int | None = None,
#     island_density: float = 0.0,
# ) -> StreamingResponse:
#     """Generates and returns a map PNG directly (ephemeral, no DB storage)."""
#     logger.info(
#         f"GET /map: size={size}, octaves={octaves}, seed={seed}, "
#         f"density={island_density}"
#     )
#     try:
#         buf = render_map_to_buffer(
#             size, octaves, seed=seed, island_density=island_density
#         )
#         return StreamingResponse(buf, media_type="image/png")
#     except Exception as e:
#         logger.error(f"Failed to generate map: {e}")
#         raise HTTPException(status_code=500, detail=str(e)) from e


# @map_router.post("/maps", response_model=MapResponse)
# def create_map(request: MapRequest, db: Session = Depends(get_db)) -> MapResponse:
#     """Generates a map and stores it in the database."""
#     logger.info(
#         f"POST /maps: size={request.size}, octaves={request.octaves}, "
#         f"seed={request.seed}, density={request.island_density}"
#     )
#     try:
#         # Check for pre-generated map if seed is not specified
#         if request.seed is None:
#             pre_gen_map = (
#                 db.query(Map)
#                 .filter(
#                     Map.is_pregenerated == True,
#                     Map.size == request.size,
#                     Map.octaves == request.octaves,
#                     Map.island_density == request.island_density,
#                 )
#                 .first()
#             )

#             if pre_gen_map:
#                 logger.info(f"Using pre-generated map: {pre_gen_map.id}")
#                 pre_gen_map.is_pregenerated = False
#                 db.commit()
#                 return MapResponse(id=pre_gen_map.id, url=f"/maps/{pre_gen_map.id}")

#         # Generate the map buffer
#         buf = render_map_to_buffer(
#             request.size,
#             request.octaves,
#             seed=request.seed,
#             island_density=request.island_density,
#         )

#         # Create a unique ID
#         map_id = str(uuid.uuid4())

#         # Create DB record
#         new_map = Map(
#             id=map_id,
#             size=request.size,
#             octaves=request.octaves,
#             seed=request.seed,
#             island_density=request.island_density,
#             data=buf.getvalue(),
#         )

#         db.add(new_map)
#         db.commit()
#         db.refresh(new_map)

#         logger.info(f"Map created successfully. ID: {map_id}")
#         return MapResponse(id=map_id, url=f"/maps/{map_id}")
#     except Exception as e:
#         logger.error(f"Failed to create map: {e}")
#         raise HTTPException(status_code=500, detail=str(e)) from e


# @map_router.get("/maps/{map_id}")
# def get_map(map_id: str, db: Session = Depends(get_db)) -> StreamingResponse:
#     """Retrieves a generated map by ID."""
#     logger.debug(f"Retrieving map with ID: {map_id}")

#     map_record = db.query(Map).filter(Map.id == map_id).first()

#     if not map_record:
#         logger.warning(f"Map ID not found: {map_id}")
#         raise HTTPException(status_code=404, detail="Map not found")

#     # Create buffer from binary data
#     assert map_record.data is not None
#     buf = io.BytesIO(map_record.data)

#     # Return as streaming response
#     return StreamingResponse(buf, media_type="image/png")
