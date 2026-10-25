import uuid

from django.conf import settings
from django.core import signing


COOKIE_NAME = "kararsizim_guest"
COOKIE_SALT = "kararsizim.polls.guest"
COOKIE_MAX_AGE = 60 * 60 * 24 * 365


def read_guest_id(request):
    signed_value = request.COOKIES.get(COOKIE_NAME)
    if not signed_value:
        return None
    try:
        raw_value = signing.loads(signed_value, salt=COOKIE_SALT, max_age=COOKIE_MAX_AGE)
        return uuid.UUID(raw_value)
    except (signing.BadSignature, ValueError, TypeError):
        return None


def new_guest_identity():
    guest_id = uuid.uuid4()
    signed_value = signing.dumps(str(guest_id), salt=COOKIE_SALT, compress=True)
    return guest_id, signed_value


def set_guest_cookie(response, signed_value):
    response.set_cookie(
        COOKIE_NAME,
        signed_value,
        max_age=COOKIE_MAX_AGE,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="Lax",
    )
