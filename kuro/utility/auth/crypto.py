"""Crypto-related functions."""

import base64
import hashlib
import typing
import uuid


def encode_md5_parameter(m: dict[str, typing.Any], app_key: str) -> str:
    """Encode MD5 parameter."""
    builder: typing.Sequence[typing.Any] = []

    for key in sorted(m.keys()):
        if key not in {"sign", "market"} and m[key] is not None:
            builder.append(f"{key}={m[key]}&")

    builder.append(app_key)
    return md5_code("".join(builder))


def md5_code(code: str) -> str:
    """MD5 code."""
    b = encode_hex_md5(code).lower().encode()
    if len(b) >= 23:
        b = bytearray(b)
        b[1], b[13] = b[13], b[1]
        b[5], b[17] = b[17], b[5]
        b[7], b[23] = b[23], b[7]

    return b.decode()


def encode_password(password: str) -> str:
    """Encode password."""
    if not password:
        return ""
    pass_encoded = base64.b64encode(password.encode()).decode()
    p = list(pass_encoded)
    shuffle(p, 0)
    shuffle(p, 1)
    return "".join(p)


def shuffle(data: list[str], start_index: int) -> typing.Sequence[str]:
    """Shuffle data."""
    for i in range(start_index, len(data), 4):
        if i + 2 < len(data):
            data[i], data[i + 2] = data[i + 2], data[i]
        if i + 6 >= len(data):
            break
    return data


def encode_hex_md5(s: str) -> str:
    """Encode hex MD5."""
    try:
        return hashlib.md5(s.encode()).hexdigest()
    except Exception:
        return s


def generate_uuid() -> str:
    """Generate a UUID."""
    return str(uuid.uuid4())


def generate_uuid_uppercase() -> str:
    """Generate a UUID."""
    return str(uuid.uuid4()).upper()
