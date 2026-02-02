BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE62_SALT = 100000


def base62_encode(num: int) -> str:
    if num < 0:
        raise ValueError("num must be non-negative")
    if num == 0:
        return BASE62_ALPHABET[0]

    base = len(BASE62_ALPHABET)
    chars = []
    while num > 0:
        num, rem = divmod(num, base)
        chars.append(BASE62_ALPHABET[rem])
    return "".join(reversed(chars))
