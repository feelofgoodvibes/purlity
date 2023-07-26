from tests.fixtures import dummy_db, test_app, test_client, test_jwt


def test_url_collection_get(test_client, test_jwt):
    get_no_auth = test_client.get("/api/url")
    get_auth = test_client.get("/api/url", headers={"Authorization": test_jwt})
    get_filters = test_client.get("/api/url", headers={"Authorization": test_jwt}, query_string={"limit":1})
    get_filters_2 = test_client.get("/api/url", headers={"Authorization": test_jwt}, query_string={"offset":1})

    assert "msg" in get_no_auth.json and get_no_auth.json["msg"] == "Missing Authorization Header"
    assert len(get_auth.json) == 2 and get_auth.json[0]["url"] == "http://example.com"
    assert len(get_filters.json) == 1 and get_filters.json[0]["url"] == "http://example.com"
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
    get_auth = test_client.get("/api/url/pyThN", headers={"Authorization": test_jwt})
    get_invalid = test_client.get("/api/url/xxXXxx")

    assert "visits" not in get_noauth.json
    assert "visits" in get_auth.json
    assert "error" in get_invalid.json and get_invalid.json["error"].endswith("not found!")