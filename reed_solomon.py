import reedsolo

rs = reedsolo.RSCodec(10)

def rs_encode(data: str):
    encoded = rs.encode(data.encode())
    return encoded

def rs_decode(encoded: bytes):
    try:
        decoded = rs.decode(encoded)[0]
        return decoded.decode(), None
    except reedsolo.ReedSolomonError as e:
        return None, str(e)
