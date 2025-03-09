import random
import time
from functools import lru_cache

N = 100_000
array = [random.randint(1, 1000) for _ in range(N)]

def range_sum_no_cache(array, L, R):
    return sum(array[L:R + 1])

def update_no_cache(array, index, value):
    array[index] = value

K = 1000
@lru_cache(maxsize=K)
def range_sum_with_cache(L, R):
    return sum(array[L:R + 1])

def update_with_cache(array, index, value):
    array[index] = value
    range_sum_with_cache.cache_clear()

Q = 50_000
queries = []
for _ in range(Q):
    if random.random() < 0.7: 
        L = random.randint(0, N - 1)
        R = random.randint(L, N - 1)
        queries.append(("Range", L, R))
    else:  
        index = random.randint(0, N - 1)
        value = random.randint(1, 1000)
        queries.append(("Update", index, value))

start_time = time.time()
for query in queries:
    if query[0] == "Range":
        range_sum_no_cache(array, query[1], query[2])
    else:
        update_no_cache(array, query[1], query[2])
no_cache_time = time.time() - start_time

start_time = time.time()
for query in queries:
    if query[0] == "Range":
        range_sum_with_cache(query[1], query[2])
    else:
        update_with_cache(array, query[1], query[2])
cached_time = time.time() - start_time

print(f"Час виконання без кешування: {no_cache_time:.2f} секунд")
print(f"Час виконання з LRU-кешем: {cached_time:.2f} секунд")
