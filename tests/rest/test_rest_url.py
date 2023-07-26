from tests.fixtures import dummy_db, test_app, test_client, test_jwt


def test_url_collection_get(test_client, test_jwt):
    get_unauth = test_client.get("/api/url")
    assert "msg" in get_unauth.json and get_unauth.json["msg"] == "Missing Authorization Header"

    get_auth = test_client.get("/api/url", headers={"Authorization": test_jwt})
    assert len(get_auth.json) == 2 and get_auth.json[0]["url"] == "http://example.com"

    get_filters = test_client.get("/api/url", headers={"Authorization": test_jwt}, query_string={"limit":1})
    assert len(get_filters.json) == 1 and get_filters.json[0]["url"] == "http://example.com"

    get_filters_2 = test_client.get("/api/url", headers={"Authorization": test_jwt}, query_string={"offset":1})
    assert len(get_filters_2.json) == 1 and get_filters_2.json[0]["short_url"] == "YouTb"

def test_url_creation(test_client, test_jwt):
    create_unauth = test_client.post("/api/url", data={"url": "https://hello.com"})
    assert create_unauth.json["url"] == "https://hello.com"

    check_before = test_client.get("/api/url", headers={"Authorization": test_jwt})
    create_auth = test_client.post("/api/url", data={"url": "https://hello2.com"}, headers={"Authorization": test_jwt})
    check_after = test_client.get("/api/url", headers={"Authorization": test_jwt})
    assert create_auth.json["url"] == "https://hello2.com"
    assert len(check_after.json) - len(check_before.json) == 1

def test_url_get(test_client, test_jwt):
    get_noauth = test_client.get("/api/url/pyThN")
    assert "visits" not in get_noauth.json

    get_auth = test_client.get("/api/url/pyThN", headers={"Authorization": test_jwt})
    assert "visits" in get_auth.json

    get_invalid = test_client.get("/api/url/xxXXxx")
    assert "msg" in get_invalid.json and get_invalid.json["msg"].endswith("not found!")

def test_url_delete(test_client, test_jwt):
    delete_unauth = test_client.delete("/api/url/pyThN")
    assert "msg" in delete_unauth.json and delete_unauth.json["msg"] == "Missing Authorization Header"

    delete_auth_forbidden = test_client.delete("/api/url/pyThN", headers={"Authorization": test_jwt})
    assert "msg" in delete_auth_forbidden.json and delete_auth_forbidden.json["msg"] == "Access denied"

    delete_auth = test_client.delete("/api/url/YouTb", headers={"Authorization": test_jwt})
    check_after = test_client.get("/api/url", headers={"Authorization": test_jwt})
    assert "message" in delete_auth.json and delete_auth.json["message"] == "deleted"
    assert delete_auth.json["url"]["url"] == "http://youtube.com"
    assert len(check_after.json) == 1

    delete_invalid = test_client.delete("/api/url/xxXxx", headers={"Authorization": test_jwt})
    assert "msg" in delete_invalid.json and delete_invalid.json["msg"].endswith("not found!")