import pytest  # type: ignore
from sqlalchemy import select

from fast_zero.models import User


@pytest.mark.skip(reason='Already tested')
def test_create_user(session):
    new_user = User(username='snoopy', password='123456', email='snoopy@email')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'snoopy'))

    assert user.username == 'snoopy'
