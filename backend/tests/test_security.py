import pytest

jwt = pytest.importorskip("jwt", reason="PyJWT dependency is not installed")
from app.core.config import get_settings
from app.core.security import create_access_token, decode_access_token


@pytest.fixture(autouse=True)
def configure_key(monkeypatch):
    monkeypatch.setenv("JWT_SECRET_KEY", "a-test-only-key-that-is-over-thirty-two-characters")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_token_round_trip():
    assert decode_access_token(create_access_token("test-user"))["sub"] == "test-user"


def test_wrong_audience_expiration_and_signature_are_rejected():
    key = get_settings().jwt_secret_key.get_secret_value()
    payload = decode_access_token(create_access_token("test-user"))
    for changes in ({"aud": "wrong-app"}, {"exp": 0}):
        token = jwt.encode({**payload, **changes}, key, algorithm="HS256")
        with pytest.raises(jwt.InvalidTokenError):
            decode_access_token(token)
    forged = jwt.encode(payload, "a-different-key-that-is-over-thirty-two-characters", algorithm="HS256")
    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token(forged)
