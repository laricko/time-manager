from werkzeug.exceptions import Forbidden


def test_auth_forbidden(client):
    r = client.get("api/task/")
    assert r.status_code == Forbidden.code


def test_auth_allowed(client, test_user_creds):
    r = client.get("api/task/", headers=test_user_creds)
    assert r.status_code == 200
