from http import HTTPStatus

import pytest  # type: ignore

from fast_zero.schemas import UserPublic


@pytest.mark.skip(reason='Already tested')
def test_read_root(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}


@pytest.mark.skip(reason='Already tested')
def test_read_home(client):
    response = client.get('/home')
    assert response.status_code == HTTPStatus.OK
    assert response.headers['content-type'] == 'text/html; charset=utf-8'
    assert (
        response.text
        == """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>
        <h1>Hello, World!</h1>
        <p>Este é um parágrafo.</p>
    </body>
    </html>
    """
    )


@pytest.mark.skip(reason='Already tested')
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


@pytest.mark.skip(reason='Already tested')
def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


@pytest.mark.skip(reason='Already tested')
def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


@pytest.mark.skip(reason='Already tested')
def test_read_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


@pytest.mark.skip(reason='Already tested')
def test_read_user_not_found(client, user):
    response = client.get('/users/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'User not found',
    }


@pytest.mark.skip(reason='Already tested')
def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'poo',
            'email': 'poo@email.com',
            'password': 'secret_of_poo',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'poo',
        'email': 'poo@email.com',
    }


@pytest.mark.skip(reason='Already tested')
def test_update_user_not_found(client, user):
    response = client.put(
        '/users/2',
        json={
            'username': 'string',
            'email': 'user@example.com',
            'password': 'string',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'User not found',
    }


@pytest.mark.skip(reason='Already tested')
def test_delete_user(client, user):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'User deleted successfully',
    }


@pytest.mark.skip(reason='Already tested')
def test_delete_user_not_found(client, user):
    response = client.delete('/users/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'User not found',
    }
