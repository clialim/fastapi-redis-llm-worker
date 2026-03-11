import redis
import json
from llama_cpp import Llama

redis_client = redis.from_url("redis://redis:6379", decode_responses=True)

llm = Llama(
    model_path="./models/Llama-3.2-1B-Instruct-Q4_K_M.gguf",
    chat_format="llama-3",
)

SYSTEM_PROMPT = (
    "You are a concise assistant. "
    "Always reply in the same language as the user's input. "
    "Do not change the language. "
    "Do not mix languages."
)


def create_response(question: str):
    return llm.create_chat_completion(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        max_tokens=256,
        temperature=0.7,
        stream=True,
    )


def run():
    while True:
        _, job_data = redis_client.brpop("inference_queue")
        job: dict = json.loads(job_data)

        print(f"Processing job: {job['id']}")

        stream = create_response(question=job["question"])

        channel = f"result:{job['id']}"

        for chunk in stream:
            delta = chunk["choices"][0].get("delta", {})
            token = delta.get("content")

            if token:
                redis_client.publish(channel, token)

        redis_client.publish(channel, "[DONE]")


if __name__ == "__main__":
    run()
