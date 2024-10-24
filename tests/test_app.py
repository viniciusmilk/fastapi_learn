from http import HTTPStatus

import pytest


@pytest.mark.skip(reason='Already tested')
def test_read_root(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}
