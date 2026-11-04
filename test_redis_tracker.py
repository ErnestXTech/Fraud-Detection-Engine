
# from redis_tracker import record_transaction

# account = "ACC_TEST_001"

# for number in range(5):
#     count = record_transaction(account, f"TXN_TEST_{number + 1}")
#     print(f"Transaction {number + 1}: recent count = {count}")

import time
from redis_tracker import record_transaction

account = "ACC_WINDOW_TEST"

print("First transaction:")
print(record_transaction(account, "WINDOW_TXN_1"))

print("Second transaction:")
print(record_transaction(account, "WINDOW_TXN_2"))

print("Waiting 125 seconds...")
time.sleep(125)

print("Third transaction after waiting:")
print(record_transaction(account, "WINDOW_TXN_3"))
