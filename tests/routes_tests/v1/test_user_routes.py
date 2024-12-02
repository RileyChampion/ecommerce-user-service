import pytest

API_VERSION = "/api/v1/"


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

    headers = {"Authorization": f"Bearer {retrieve_test_oauth_token}"}
    response = client.get(API_VERSION + "user/users", params={
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

    headers = {"Authorization": f"Bearer {retrieve_test_oauth_token}"}
    response = client.get(API_VERSION + "user/100", headers=headers)

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