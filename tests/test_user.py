import jwt
import pytest

from app import schemas
from app.config import settings


def test_create_user(client):
    response = client.post(
        "/users/", json={"email": "demo@gmail.com", "password": "password"}
    )
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "demo@gmail.com"
    assert response.status_code == 201


def test_login_user(test_user, client):
    response = client.post(
        "/login/",
        data={
            "username": test_user["email"],
            "password": test_user["password"],
        },
    )
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(
        login_response.access_token,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )
    user_id: int = payload.get("user_id")
    assert user_id == test_user["id"]
    assert login_response.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "password", 403),
        ("demo@gmail.com", "wrongpassword", 403),
        ("demo@gmail.com", None, 422),  # pydantic validation error
        (None, "password", 422),  # pydantic validation error
    ],
)
def test_incorrect_login(test_user, client, email, password, status_code):
    response = client.post(
        "/login",
        data={"username": email, "password": password},
    )
    assert response.status_code == status_code
