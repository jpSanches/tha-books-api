import json
from typing import List, AsyncGenerator, Any
from asyncio import Queue


class SSEManager:
    def __init__(self):
        self.connections: List[Queue[dict[str, Any]]] = []

    async def connect(self) -> AsyncGenerator[str, None]:
        queue: Queue[dict[str, Any]] = Queue()
        self.connections.append(queue)

        try:
            while True:
                data = await queue.get()
                yield f"data: {json.dumps(data)}\n\n"

        finally:
            self.connections.remove(queue)

    async def broadcast(self, event_data: dict[str, Any]):
        for queue in self.connections:
            await queue.put(event_data)


sse_manager = SSEManager()
