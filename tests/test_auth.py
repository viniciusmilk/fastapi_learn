from http import HTTPStatus


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
