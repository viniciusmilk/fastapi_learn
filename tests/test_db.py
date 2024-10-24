import pytest
from sqlalchemy import select

from ..fast_zero.models import Todo, User


@pytest.mark.skip(reason='Already tested')
def test_create_user(session):
    new_user = User(username='snoopy', password='123456', email='snoopy@email')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'snoopy'))

    assert user.username == 'snoopy'


@pytest.mark.skip(reason='Already tested')
def test_create_todo(session, user: User):
    todo = Todo(
        title='Buy milk',
        description='Buy milk for breakfast',
        state='todo',
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == user.id))

    assert todo in user.todos
