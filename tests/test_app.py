from http import HTTPStatus

from fast_zero.schemas import UserPublic


# @pytest.mark.skip(reason='Already tested')
def test_read_root(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}


# @pytest.mark.skip(reason='Already tested')
def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'username': 'snoopy',
            'email': 'snoopy@email.com',
            'password': 'secret_of_snoopy',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'snoopy',
        'email': 'snoopy@email.com',
    }


# @pytest.mark.skip(reason='Already tested')
def test_create_user_username_exists(client, user):
    response = client.post(
        '/users',
        json={
            'username': 'snoopy',
            'email': 'snoopy@email.com',
            'password': 'secret_of_snoopy',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


# @pytest.mark.skip(reason='Already tested')
def test_create_user_email_exists(client, user):
    response = client.post(
        '/users',
        json={
            'username': 'snoopy2',
            'email': 'snoopy@email.com',
            'password': 'secret_of_snoopy',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


# @pytest.mark.skip(reason='Already tested')
def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


# @pytest.mark.skip(reason='Already tested')
def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


# @pytest.mark.skip(reason='Already tested')
def test_read_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


# @pytest.mark.skip(reason='Already tested')
def test_read_user_not_found(client, user):
    response = client.get('/users/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'User not found',
    }


# @pytest.mark.skip(reason='Already tested')
def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'poo',
            'email': 'poo@email.com',
            'password': 'secret_of_poo',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': 'poo',
        'email': 'poo@email.com',
    }


# @pytest.mark.skip(reason='Already tested')
def test_update_user_not_current_user(client, user, token):
    response = client.put(
        f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'string',
            'email': 'user@example.com',
            'password': 'string',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'Not enough permissions',
    }


# @pytest.mark.skip(reason='Already tested')
def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'User deleted successfully',
    }


# @pytest.mark.skip(reason='Already tested')
def test_delete_user_not_found(client, user, token):
    response = client.delete(
        f'/users/{user.id + 1}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'Not enough permissions',
    }


# @pytest.mark.skip(reason='Already tested')
def test_login_for_access_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


# @pytest.mark.skip(reason='Already tested')
def test_login_for_access_token_non_existent_user(client, user):
    response = client.post(
        '/token',
        data={'username': 'user.email', 'password': user.clean_password},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


# @pytest.mark.skip(reason='Already tested')
def test_login_for_access_token_incorrect_password(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': 'user.clean_password'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
