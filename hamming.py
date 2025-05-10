def hamming_encode(data):
    d = list(map(int, data))
    p1 = d[0] ^ d[1] ^ d[3]
    p2 = d[0] ^ d[2] ^ d[3]
    p3 = d[1] ^ d[2] ^ d[3]
    return f"{p1}{p2}{d[0]}{p3}{d[1]}{d[2]}{d[3]}"

def hamming_decode(encoded):
    e = list(map(int, encoded))
    s1 = e[0] ^ e[2] ^ e[4] ^ e[6]
    s2 = e[1] ^ e[2] ^ e[5] ^ e[6]
    s3 = e[3] ^ e[4] ^ e[5] ^ e[6]
    error_pos = s1 * 1 + s2 * 2 + s3 * 4
    if error_pos != 0:
        e[error_pos - 1] ^= 1
    decoded = f"{e[2]}{e[4]}{e[5]}{e[6]}"
    return decoded, error_pos
