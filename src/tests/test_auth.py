def test_auth_forbidden(client):
    r = client.get("api/task/")
    assert r.status_code == 403