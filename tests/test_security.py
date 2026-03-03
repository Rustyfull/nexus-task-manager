from app.core.security import get_security_service



def test_hash_password():
    """Test password hashing."""
    password = "secure_password_123"
    hashed = get_security_service().hashpassword(password)

    assert hashed != password
    assert get_security_service().verifypassword(password,hashed)


def test_verify_password_wrong():
    """Test wrong password verification."""
    password = "correct_password"
    hashed = get_security_service().hashpassword(password)

    assert not get_security_service().verifypassword("wrong_password",hashed)


def test_create_access_token():
    """Test access token creation."""
    data = {"sub":"123", "email":"test@example.com"}
    token = get_security_service().create_access_token(data)

    assert token is not None
    assert isinstance(token,str)

    # Decode and verify
    payload = get_security_service().decode_token(token)
    assert payload is not None
    assert payload["sub"] == "123"
    assert payload["type"] == "access"



def test_create_refresh_token():
    """Test refresh token creation."""
    data = {"sub":"123", "email":"test@example.com"}
    token = get_security_service().create_refresh_token(data)


    assert token is not None

    # Decode and verify
    payload = get_security_service().decode_token(token)
    assert payload is not None
    assert payload["type"] == "refresh"


def test_decode_invalid_token():
    """Test decoding invalid token."""
    from datetime import timedelta, timezone, datetime

    # Create a token that expires immediately
    data = {
        "sub":"123"
    }
    to_encode = data.copy()
    to_encode.update({
        "exp":datetime.now(timezone.utc)- timedelta(hours=1),
        "type":"access"
    })

    from jose import jwt
    from app.core.config import get_settings


    expired_token = jwt.encode(
        to_encode,
        get_settings().secret_key,
        algorithm=get_settings().algorithm
    )

    payload = get_security_service().decode_token(expired_token)
    assert payload is None
