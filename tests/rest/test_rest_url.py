from tests.fixtures import dummy_db, test_app, test_client, test_jwt


def test_url_get(test_client, test_jwt):
    get_no_auth = test_client.get("/api/url")
    get_auth = test_client.get("/api/url", headers={"Authorization": test_jwt})
    get_filters = test_client.get("/api/url", headers={"Authorization": test_jwt}, query_string={"limit":1})
    get_filters_2 = test_client.get("/api/url", headers={"Authorization": test_jwt}, query_string={"offset":1})

    assert "msg" in get_no_auth.json and get_no_auth.json["msg"] == "Missing Authorization Header"
    assert len(get_auth.json) == 2 and get_auth.json[0]["url"] == "http://example.com"
    assert len(get_filters.json) == 1 and get_filters.json[0]["url"] == "http://example.com"
    assert len(get_filters_2.json) == 1 and get_filters_2.json[0]["short_url"] == "YouTb"

def test_url_creation(test_client, test_jwt):
    create_unauthenticated = test_client.post("/api/url", data={"url": "https://hello.com"})
    create_authenticated = test_client.post("/api/url", data={"url": "https://hello2.com"}, headers={"Authorization": test_jwt})

    assert create_unauthenticated.json["user_id"] == None
    assert create_authenticated.json["user_id"] == 1