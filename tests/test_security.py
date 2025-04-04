from http import HTTPStatus

from jwt import decode

from ..fast_zero.security import create_access_token, settings


def test_create_access_token():
    data = {'secret': 'Meu segredo'}
    token = create_access_token(data)

    decoded_data = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert data['secret'] == decoded_data['secret']
    assert 'exp' in decoded_data


def test_jwt_invalid_token(client):
    response = client.delete('/users/1', headers={'Authorization': 'Bearer invalid_token'})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_user_not_found(client):
    token = create_access_token({'sub': 'not_found'})
    response = client.delete('/users/1', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_user_found(client):
    token = create_access_token({})
    response = client.delete('/users/1', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
