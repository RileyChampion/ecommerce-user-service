import pytest

API_VERSION = "/api/v1"


def test_get_users(client, create_user, batch_create_users, retrieve_test_oauth_token):
    create_user(
        username="ashleytaylor",
        first_name="Alexa",
        last_name="Carr",
        email="jamiebeck@example.com",
        telephone="001-496-715-4158",
        profile_pic="default.png",
    )
    batch_create_users(size=10)

    nonadmin_client = next(client())

    headers = {"Authorization": f"Bearer {retrieve_test_oauth_token}"}
    response = nonadmin_client.get(API_VERSION + "/user/users", params={
        "limit": 11,
        "offset": 0,
        "order_by": "created_at",
        "is_active": "false"
    }, headers=headers)

    assert response.status_code == 200
    assert response.json()[0] == {
        "username": "ashleytaylor",
        "first_name": "Alexa",
        "last_name": "Carr",
        "email": "jamiebeck@example.com",
        "telephone": "001-496-715-4158",
        "profile_pic": "default.png",
        "id": 31
    }
    assert len(response.json()) == 11


def test_get_user_id(client, create_user, retrieve_test_oauth_token):
    create_user(
        id=100,
        username="test_user_name",
        first_name="Alexa",
        last_name="Carr",
        email="jamiebeck@example.com",
        telephone="001-496-715-4158",
        profile_pic="default.png",
    )

    nonadmin_client = next(client())

    headers = {"Authorization": f"Bearer {retrieve_test_oauth_token}"}
    response = nonadmin_client.get(API_VERSION + "/user/100", headers=headers)

    assert response.json() == {
        'id': 100,
        'username': 'test_user_name',
        'first_name': 'Alexa',
        'last_name': 'Carr',
        'email': 'jamiebeck@example.com',
        'telephone': '001-496-715-4158',
        'profile_pic': 'default.png',
        'addresses': [],
        'preferences': [],
        'roles': []
    }


def test_create_new_user(client, retrieve_test_oauth_token):
    payload = {
        'username': 'test_user_name_useruser1234',
        'first_name': 'Alexa',
        'last_name': 'Carr',
        'email': 'jamiebeck@example.com',
        'telephone': '001-496-715-4158',
        'password': 'passwordpasswordpassword'
    }

    nonadmin_client = next(client())

    headers = {"Authorization": f"Bearer {retrieve_test_oauth_token}"}
    response = nonadmin_client.post(
        API_VERSION + "/user/create",
        json=payload,
        headers=headers
    )
    print(response.json())

    assert response.status_code == 201
    json_resp = response.json()

    assert json_resp["username"] == "test_user_name_useruser1234"
    assert json_resp["first_name"] == "Alexa"
    assert json_resp["last_name"] == "Carr"
    assert json_resp["email"] == "jamiebeck@example.com"
    assert json_resp["telephone"] == "001-496-715-4158"
    assert json_resp["profile_pic"] == "default.png"


def test_create_new_user_username_taken(client, create_user, retrieve_test_oauth_token):
    create_user(
        username='test_user_name_useruser1234'
    )

    payload = {
        'username': 'test_user_name_useruser1234',
        'first_name': 'Alexa',
        'last_name': 'Carr',
        'email': 'jamiebeck@example.com',
        'telephone': '001-496-715-4158',
        'password': 'passwordpasswordpassword'
    }

    nonadmin_client = next(client())

    headers = {"Authorization": f"Bearer {retrieve_test_oauth_token}"}
    response = nonadmin_client.post(
        API_VERSION + "/user/create",
        json=payload,
        headers=headers
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Username already taken."
    }
    

def test_delete_user_from_service_unauthorized(client, create_user, retrieve_test_oauth_token):
    create_user(
        id=101
    )

    admin_client = next(client())
    
    headers = {"Authorization": f"Bearer {retrieve_test_oauth_token}"}
    response = admin_client.delete(API_VERSION + "/user/delete/101", headers=headers)

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Unauthorized request."
    }


def test_delete_user_from_service_authorized(client, create_user, retrieve_test_oauth_token):
    create_user(
        id=101
    )

    admin_client = next(client(True))
    
    headers = {"Authorization": f"Bearer {retrieve_test_oauth_token}"}
    response = admin_client.delete(API_VERSION + "/user/delete/101", headers=headers)

    assert response.status_code == 200
    assert response.json() == {
        "messages": "Deleted user."
    }


def test_delete_user_from_service_not_found(client, create_user, retrieve_test_oauth_token):
    admin_client = next(client(True))

    headers = {"Authorization": f"Bearer {retrieve_test_oauth_token}"}
    response = admin_client.delete(API_VERSION + "/user/delete/101", headers=headers)

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Unable to delete entered user."
    }


def test_update_user_unauthorized(client, create_user, retrieve_test_oauth_token):
    create_user(
        id=101
    )

    nonadmin_client = next(client())
    
    payload = {
        "username": "new_user_name",
        "first_name": "test_first_name",
        "last_name": "test_last",
        "email": "newEmail@email.com",
        "telephone": "3738848483",
        "profile_pic": "default.png",
        "is_active": True
    }
    
    headers = {"Authorization": f"Bearer {retrieve_test_oauth_token}"}
    response = nonadmin_client.patch(
        API_VERSION + "/user/update/101",
        json=payload,
        headers=headers
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Unauthorized request."
    }


def test_update_user_authorized(client, create_user, retrieve_test_oauth_token):
    create_user(
        id=101
    )

    admin_client = next(client(True))

    payload = {
        "username": "new_user_name",
        "first_name": "test_first_name",
        "last_name": "test_last",
        "email": "newEmail@email.com",
        "telephone": "3738848483",
        "profile_pic": "default.png",
        "is_active": True
    }
    
    headers = {"Authorization": f"Bearer {retrieve_test_oauth_token}"}
    response = admin_client.patch(
        API_VERSION + "/user/update/101",
        json=payload,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json() == {
        "messages": "Updated user."
    }


def test_update_user_not_found(client, retrieve_test_oauth_token):
    admin_client = next(client(True))

    payload = {
        "username": "new_user_name",
        "first_name": "test_first_name",
        "last_name": "test_last",
        "email": "newEmail@email.com",
        "telephone": "3738848483",
        "profile_pic": "default.png",
        "is_active": True
    }
    
    headers = {"Authorization": f"Bearer {retrieve_test_oauth_token}"}
    response = admin_client.patch(
        API_VERSION + "/user/update/101",
        json=payload,
        headers=headers
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Unable to update entered user."
    }


def test_login():
    # TODO: 
    pass


def test_logout():
    # TODO:
    pass
