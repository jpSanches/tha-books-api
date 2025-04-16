from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.services.sse_manager import sse_manager
from app.core.deps import get_current_user

router = APIRouter(prefix="/v1/stream", tags=["SSE"])


@router.get("/books")
async def stream_books(
    _: str = Depends(get_current_user),
):
    async def event_generator():
        async for message in sse_manager.connect():
            yield message

    return StreamingResponse(event_generator(), media_type="text/event-stream")
