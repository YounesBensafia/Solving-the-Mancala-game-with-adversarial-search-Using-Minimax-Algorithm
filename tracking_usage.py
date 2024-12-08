import time
import tracemalloc

def track_time(func, *args, **kwargs):
    start_time = time.time()
    func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time


def track_memory(func, *args, **kwargs):
    tracemalloc.start()
    func(*args, **kwargs)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    peak_memory_kb = peak / 1024
    return peak_memory_kb

def our_function(n):
    a = [i for i in range(n)]
    time.sleep(5)

memory_used = track_memory(our_function, 15)
