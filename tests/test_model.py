import os
import pytest
from app import model


TODOS = [('wake up', True), ('sleep', False)]
UPDATE_TODOS = [('wake up', False), ('sleep', True)]


@pytest.fixture(scope='module')
def my_model():
    new_model = model.Model('teste.json')
    yield new_model
    os.remove('teste.json')


def test_model_must_start_empty(my_model):
    assert len(my_model) == 0


@pytest.mark.parametrize('todo, status', TODOS)
def test_create_todo(my_model, todo: str, status: bool):
    my_model.create_todo(todo, status)


def test_create_todo_raise_cannot_by_empty(my_model):
    with pytest.raises(model.EmptyTodo):
        my_model.create_todo('', True)


def test_create_todo_raise_already_exist(my_model):
    with pytest.raises(model.TodoAlreadyExist):
        todo = TODOS[0][0]
        status = True
        my_model.create_todo(todo, status)


def test_model_must_have_same_len_that_TODOS(my_model):
    assert len(my_model) == len(TODOS)


def test_select_where_without_args_must_return_same_that_TODOS(my_model):
    assert len(my_model.select_where()) == len(TODOS)


def test_select_where_filter_by_wake_up_must_return_one(my_model):
    assert len(my_model.select_where(todo='wake up')) == 1


@pytest.mark.parametrize('todo, new_status', UPDATE_TODOS)
def test_update_todo_status(my_model, todo, new_status) -> None:
    my_model.update_todo_status(todo, new_status)


def test_select_todo_must_be_equals_UPDATE_TODOS(my_model):
    local = []
    for todo in UPDATE_TODOS:
        local.append({'todo': todo[0], 'status': todo[1]})
    assert my_model.select_todo() == local


@pytest.mark.parametrize('todo', [todo[0] for todo in UPDATE_TODOS])
def test_delete_todo(my_model, todo):
    my_model.delete_todo(todo)
    assert len(my_model.select_where(todo=todo)) == 0
