from django.conf import settings
from hashids import Hashids

hashids = Hashids(salt=settings.SECRET_KEY, min_length=8)


def encode_id(id):
    return hashids.encode(id)


def decode_id(encoded_id):
    decoded = hashids.decode(encoded_id)
    if decoded:
        return decoded[0]
    return None
