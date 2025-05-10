
import random

def flip_bit_str(data: str, index: int) -> str:
    lst = list(data)
    lst[index] = '1' if lst[index] == '0' else '0'
    return ''.join(lst)

def flip_random_bits(data: str, flip_count: int = 1) -> str:
    lst = list(data)
    indices = random.sample(range(len(lst)), flip_count)
    for idx in indices:
        lst[idx] = '1' if lst[idx] == '0' else '0'
    return ''.join(lst)

def burst_flip(data: str, burst_length: int = 3) -> str:
    lst = list(data)
    if len(lst) < burst_length:
        return flip_random_bits(data, 1)
    start = random.randint(0, len(lst) - burst_length)
    for i in range(start, start + burst_length):
        lst[i] = '1' if lst[i] == '0' else '0'
    return ''.join(lst)

def gaussian_flip(data: str, intensity: float = 0.2) -> str:
    lst = list(data)
    for i in range(len(lst)):
        if random.random() < intensity:
            lst[i] = '1' if lst[i] == '0' else '0'
    return ''.join(lst)
