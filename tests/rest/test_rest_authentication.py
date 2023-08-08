from tests.fixtures import test_app, dummy_db, test_client


def test_authentication_process(test_client):
    user_data =  {"username": "test_username", "password": "test_password"}

    register_response = test_client.post("/api/register", data=user_data)
    assert register_response.json["msg"] == "ok"

    login_response = test_client.post("/api/login", data=user_data)
    assert "access_token" in login_response.json

    cookie_present = False
    for cookie in login_response.headers.getlist('Set-Cookie'):
        if "access_token" in cookie:
            cookie_present = True
            break
    
    assert cookie_present is True

    wrong_passwrod_response = test_client.post("/api/login", data={"username": user_data["username"], "password": "12345"})
    assert wrong_passwrod_response.json["msg"] == "Wrong password"
    assert wrong_passwrod_response.status_code == 400


def test_authentication_errors(test_client):
    unique_username_response = test_client.post("/api/register", data={"username": "Max", "password": "123"})
    assert unique_username_response.json["msg"] == "User with username Max already exists!"
    assert unique_username_response.status_code == 400

    missing_username_response = test_client.post("/api/register", data={"password": "123"})
    assert missing_username_response.json["message"]["username"] == "Username is required"
    assert missing_username_response.status_code == 400

    missing_password_response = test_client.post("/api/register", data={"username": "123"})
    assert missing_password_response.json["message"]["password"] == "Password is required"
    assert missing_password_response.status_code == 400

    nonexisting_response = test_client.post("/api/login", data={"username": "123", "password": "123"})
    assert nonexisting_response.json["msg"] == "User does not exist"
    assert nonexisting_response.status_code == 404

    register_username_too_long_response = test_client.post("/api/register", data={"username": "test"*32, "password": "testpassword"})
    assert register_username_too_long_response.status_code == 400
    assert register_username_too_long_response.json["msg"].startswith("Username or password too long")

    register_password_too_long_response = test_client.post("/api/register", data={"username": "test", "password": "testpassword"*32})
    assert register_password_too_long_response.status_code == 400
    assert register_password_too_long_response.json["msg"].startswith("Username or password too long")

    login_username_too_long_response = test_client.post("/api/login", data={"username": "test"*32, "password": "testpassword"})
    assert login_username_too_long_response.status_code == 400
    assert login_username_too_long_response.json["msg"].startswith("Username or password too long")
