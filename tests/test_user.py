from app import schemas
from tests.database import client, session  # noqa: F401


def test_create_user(client):  # noqa: F811
    response = client.post(
        "/users/", json={"email": "demo@gmail.com", "password": "password"}
    )
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "demo@gmail.com"
    assert response.status_code == 201
