from http import HTTPStatus

from freezegun import freeze_time


# @pytest.mark.skip(reason='Already tested')
def test_login_for_access_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


# @pytest.mark.skip(reason='Already tested')
def test_login_for_access_token_non_existent_user(client, user):
    response = client.post(
        '/auth/token',
        data={'username': 'user.email', 'password': user.clean_password},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


# @pytest.mark.skip(reason='Already tested')
def test_login_for_access_token_incorrect_password(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'user.clean_password'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


# @pytest.mark.skip(reason='Already tested')
def test_access_token_expired_after_time(client, user):
    with freeze_time('2024-10-20 12:00:00'):
        response = client.post(
            'auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2024-10-20 12:31:00'):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'wrong',
                'email': 'wrong@email.com',
                'password': 'wrong',
            },
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


# @pytest.mark.skip(reason='Already tested')
def test_access_token_inexistent_user(client, user):
    response = client.post(
        'auth/token',
        data={'username': 'no_user@domain.com', 'password': 'testtest'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


# @pytest.mark.skip(reason='Already tested')
def test_access_token_wrong_password(client, user):
    response = client.post(
        'auth/token',
        data={'username': user.email, 'password': 'wrong_password'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


# @pytest.mark.skip(reason='Already tested')
def test_refresh_access_token(client, user, token):
    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'


# @pytest.mark.skip(reason='Already tested')
def test_access_token_expired_not_refresh(client, user):
    with freeze_time('2024-10-20 12:00:00'):
        response = client.post(
            'auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2024-10-20 12:31:00'):
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
