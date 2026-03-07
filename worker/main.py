import redis

redis_client = redis.from_url("redis://redis:6379", decode_responses=True)
def run():
    # while true
    pass

if __name__ == "__main__":
    run()