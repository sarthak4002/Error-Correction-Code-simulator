import numpy as np

# Generator polynomials: G1 = 111, G2 = 101
def conv_encode(bits):
    state = [0, 0]
    encoded = []
    for bit in bits:
        bit = int(bit)
        state = [bit] + state[:2]
        out1 = state[0] ^ state[1] ^ state[2]
        out2 = state[0] ^ state[2]
        encoded.extend([out1, out2])
    return ''.join(map(str, encoded))

def hamming_distance(s1, s2):
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def conv_decode(encoded_bits):
    n = 2  # 2 output bits per input
    k = 3  # Constraint length
    states = {
        '00': ['00', '10'],
        '01': ['00', '10'],
        '10': ['01', '11'],
        '11': ['01', '11']
    }

    # State transition: (current_state, input_bit) -> (next_state, output)
    transitions = {
        '00': {'0': ('00', '00'), '1': ('10', '11')},
        '01': {'0': ('00', '11'), '1': ('10', '00')},
        '10': {'0': ('01', '10'), '1': ('11', '01')},
        '11': {'0': ('01', '01'), '1': ('11', '10')}
    }

    paths = {'00': ('', 0)}  # state -> (path, score)

    for i in range(0, len(encoded_bits), 2):
        new_paths = {}
        segment = encoded_bits[i:i+2]

        for state in paths:
            for input_bit in ['0', '1']:
                next_state, out = transitions[state][input_bit]
                dist = hamming_distance(segment, out)
                score = paths[state][1] + dist
                path = paths[state][0] + input_bit

                if next_state not in new_paths or score < new_paths[next_state][1]:
                    new_paths[next_state] = (path, score)
        paths = new_paths

    best_path = min(paths.values(), key=lambda x: x[1])[0]
    return best_path
