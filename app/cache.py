import redis

# Connect to the Redis server running on the VM
# (Since FastAPI and Redis are on the same VM, we use 'localhost')
redis_client = redis.Redis(
    host="localhost", 
    port=6379, 
    db=0, 
    decode_responses=True # Automatically converts bytes to strings
)