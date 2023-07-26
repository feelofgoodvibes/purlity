from tests.fixtures import test_app, dummy_db, test_client


def test_authentication_process(test_client):
    user_data =  {"username": "test_username", "password": "test_password"}

    register_response = test_client.post("/api/register", data=user_data)
    login_response = test_client.post("/api/login", data=user_data)
    wrong_passwrod_response = test_client.post("/api/login", data={"username": user_data["username"], "password": "12345"})

    assert register_response.json["message"] == "ok"
    assert "access_token" in login_response.json
    assert wrong_passwrod_response.json["message"] == "Wrong password"


def test_authentication_errors(test_client):
    unique_username_response = test_client.post("/api/register", data={"username": "Max", "password": "123"})
    missing_username_response = test_client.post("/api/register", data={"password": "123"})
    missing_password_response = test_client.post("/api/register", data={"username": "123"})
    nonexisting_response = test_client.post("/api/login", data={"username": "123", "password": "123"})

    assert unique_username_response.json["message"] == "User with username Max already exists!"
    assert missing_username_response.json["message"]["username"] == "Username is required"
    assert missing_password_response.json["message"]["password"] == "Password is required"
    assert nonexisting_response.json["message"] == "User does not exist"
