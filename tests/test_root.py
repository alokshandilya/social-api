from tests.database import client, session  # noqa: F401


def test_read_root(client):  # noqa: F811
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"data": "Hello World"}
