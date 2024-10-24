from http import HTTPStatus

import pytest

from fast_zero.models import TodoState

from .conftest import TodoFactory


@pytest.mark.skip(reason='Already tested')
def test_create_todo(client, token, mock_db_time):
    time = mock_db_time.isoformat().split('.')[0]
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Buy milk',
            'description': 'Buy milk for breakfast',
            'state': 'todo',
        },
    )

    #  Formatar a resposta da API
    actual_response = response.json()
    actual_response['created_at'] = actual_response['created_at'].split('.')[0]
    actual_response['updated_at'] = actual_response['updated_at'].split('.')[0]

    assert response.status_code == HTTPStatus.CREATED
    assert actual_response == {
        'id': 1,
        'title': 'Buy milk',
        'description': 'Buy milk for breakfast',
        'state': 'todo',
        'created_at': time,
        'updated_at': time,
    }


@pytest.mark.skip(reason='Already tested')
def test_list_todos_should_return_5_todos(session, client, user, token):
    expected_todos = 5

    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.skip(reason='Already tested')
def test_list_todos_pagination_should_return_2_todos(session, client, user, token):
    expected_todos = 2
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.skip(reason='Already tested')
def test_list_todos_filter_title_should_return_5_todos(session, client, user, token):
    expected_todos = 5
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id, title='Buy milk'))
    session.commit()

    response = client.get(
        '/todos/?title=Buy milk',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.skip(reason='Already tested')
def test_list_todos_filter_description_should_return_5_todos(session, client, user, token):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, description='Buy milk for breakfast')
    )
    session.commit()

    response = client.get(
        '/todos/?description=milk',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.skip(reason='Already tested')
def test_list_todos_filter_state_should_return_5_todos(session, client, user, token):
    expected_todos = 5
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id, state=TodoState.draft))
    session.commit()

    response = client.get(
        '/todos/?state=draft',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.skip(reason='Already tested')
def test_list_todos_filter_combined_should_return_5_todos(session, client, user, token):
    expected_todos = 8

    session.bulk_save_objects(
        TodoFactory.create_batch(
            5,
            user_id=user.id,
            title='Buy milk',
            description='Buy milk for breakfast',
            state=TodoState.done,
        )
    )

    session.bulk_save_objects(
        TodoFactory.create_batch(
            5,
            user_id=user.id,
            title='Buy milk',
            description='Buy milk for breakfast',
            state=TodoState.todo,
        )
    )

    session.bulk_save_objects(
        TodoFactory.create_batch(
            3,
            user_id=user.id,
            title='Other title',
            description='Other task for breakfast',
            state=TodoState.todo,
        )
    )

    session.commit()

    response = client.get(
        '/todos/?description=breakfast&state=todo',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


@pytest.mark.skip(reason='Already tested')
def test_list_todos_should_return_all_expected_fields(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    session.commit()
    session.refresh(todo)

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Formatar a resposta da API
    actual_response = response.json()['todos']
    for item in actual_response:
        item['created_at'] = item['created_at'].split('.')[0]
        item['updated_at'] = item['updated_at'].split('.')[0]

    assert response.status_code == HTTPStatus.OK
    assert actual_response == [
        {
            'id': todo.id,
            'title': todo.title,
            'description': todo.description,
            'state': todo.state.value,
            'created_at': todo.created_at.isoformat().split('.')[0],
            'updated_at': todo.updated_at.isoformat().split('.')[0],
        }
    ]


@pytest.mark.skip(reason='Already tested')
def test_patch_todo_task_not_found(client, token):
    response = client.patch(
        f'/todos/{10}',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


@pytest.mark.skip(reason='Already tested')
def test_patch_todo(client, token, session, user):
    todo = TodoFactory(user_id=user.id, title='Buy bread')

    session.add(todo)
    session.commit()

    response = client.patch(
        f'/todos/{todo.id}',
        json={'title': 'Buy milk'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'Buy milk'


@pytest.mark.skip(reason='Already tested')
def test_delete_todo_task_not_found(client, token):
    response = client.delete(
        f'/todos/{10}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


@pytest.mark.skip(reason='Already tested')
def test_delete_todo(client, token, session, user):
    todo = TodoFactory(user_id=user.id, title='Buy bread')

    session.add(todo)
    session.commit()

    response = client.delete(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Task ras been  deleted successfully'}
