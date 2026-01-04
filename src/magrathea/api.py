import uuid
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from .main import render_map_to_buffer

app = FastAPI()

# In-memory storage for map buffers
# Key: UUID (str), Value: BytesIO buffer
map_store = {}

class MapRequest(BaseModel):
    size: int = 128
    octaves: int = 4

class MapResponse(BaseModel):
    id: str
    url: str

@app.post("/maps", response_model=MapResponse)
def create_map(request: MapRequest):
    """Generates a map and stores it in memory."""
    try:
        # Generate the map buffer
        buf = render_map_to_buffer(request.size, request.octaves)
        
        # Create a unique ID
        map_id = str(uuid.uuid4())
        
        # Store in memory
        map_store[map_id] = buf
        
        return {
            "id": map_id,
            "url": f"/maps/{map_id}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/maps/{map_id}")
def get_map(map_id: str):
    """Retrieves a generated map by ID."""
    if map_id not in map_store:
        raise HTTPException(status_code=404, detail="Map not found")
    
    # Get the buffer
    buf = map_store[map_id]
    
    # Reset buffer position to ensuring we read from start
    buf.seek(0)
    
    # Return as streaming response
    return StreamingResponse(buf, media_type="image/png")
