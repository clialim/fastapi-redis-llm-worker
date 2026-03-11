import json
import uuid
from contextlib import asynccontextmanager
from redis import asyncio as aredis
from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse

# Redis 클라이언트를 전역으로 선언하되 연결 관리는 lifespan에서 수행
redis_client = aredis.from_url("redis://redis:6379", decode_responses=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 앱 시작 시 실행
    yield
    # 앱 종료 시 실행 (연결 정리)
    await redis_client.close()


app = FastAPI(lifespan=lifespan)


@app.post("/chats")
async def chat_handler(
    question: str = Body(..., embed=True),
):
    job_id = str(uuid.uuid4())
    channel = f"result:{job_id}"

    pubsub = redis_client.pubsub()
    await pubsub.subscribe(channel)

    job = {"id": job_id, "question": question}
    await redis_client.lpush("inference_queue", json.dumps(job))

    async def event_generator():
        try:
            async for message in pubsub.listen():
                if message["type"] == "message":
                    data = message["data"]

                    if data == "[DONE]":
                        break

                    yield f"data: {data}\n\n"
        finally:
            await pubsub.unsubscribe(channel)
            await pubsub.close()

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )
