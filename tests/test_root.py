def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"data": "Hello World"}