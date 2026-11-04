import redis

# Connect to the local Memurai server
client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

# Test the connection
print(client.ping())
