from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_session
from ..models import Todo, User
from ..schemas import Message, TodoList, TodoPublic, TodoSchema, TodoUpdate
from ..security import get_current_user

router = APIRouter()

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/todos', tags=['todos'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=TodoPublic)
def create_todo(
    todo: TodoSchema,
    user: T_CurrentUser,
    session: T_Session,
):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get('/', status_code=HTTPStatus.OK, response_model=TodoList)
def get_todos(  # noqa
    session: T_Session,
    user: T_CurrentUser,
    title: str | None = None,
    description: str | None = None,
    state: str | None = None,
    offset: int | None = None,
    limit: int | None = None,
):
    query = select(Todo).where(Todo.user_id == user.id)

    if title:
        query = query.filter(Todo.title.contains(title))

    if description:
        query = query.filter(Todo.description.contains(description))

    if state:
        query = query.filter(Todo.state == state)

    todos = session.scalars(query.offset(offset).limit(limit)).all()

    return {
        'todos': todos,
    }


@router.patch('/{todo_id}', status_code=HTTPStatus.OK, response_model=TodoPublic)
def patch_todo(
    todo_id: int,
    session: T_Session,
    user: T_CurrentUser,
    todo: TodoUpdate,
):
    db_todo = session.scalar(select(Todo).where(Todo.id == todo_id, Todo.user_id == user.id))

    if not db_todo:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Task not found')

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.delete(
    '/{todo_id}',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def delete_todo(
    todo_id: int,
    session: T_Session,
    user: T_CurrentUser,
):
    db_todo = session.scalar(select(Todo).where(Todo.id == todo_id, Todo.user_id == user.id))

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Task not found',
        )

    session.delete(db_todo)
    session.commit()

    return {'message': 'Task has been  deleted successfully'}
