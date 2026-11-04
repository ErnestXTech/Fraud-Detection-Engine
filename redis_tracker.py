
import time
import redis

client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


def record_transaction(account: str, transaction_id: str) -> int:
    current_time = time.time()

    key = f"transactions:{account}"

    # Remove transactions older than 120 seconds
    client.zremrangebyscore(
        key, 0, current_time - 120
    )

    # Record this transaction using its unique ID
    client.zadd(
        key, {transaction_id: current_time}
    )

    # Automatically expire unused account keys
    client.expire(key, 180)

    # Count transactions in the last 120 seconds
    return client.zcount(
        key, current_time - 120, current_time
    )
