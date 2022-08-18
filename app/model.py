import json
import os
import typing


class Model:
    def __init__(self, database_name: str) -> None:
        self.database_name = database_name
        self.data = []

        if os.path.exists(self.database_name):
            with open(self.database_name, 'r') as file:
                registers = json.loads(file.read())
                for register in registers:
                    self.data.append(register)

    def __len__(self) -> int:
        return len(self.data)

    def _save(self) -> None:
        with open(self.database_name, 'w') as file:
            file.write(json.dumps(self.data))

    def _order(self, registers: typing.List) -> typing.List:
        return registers

    def select_todo(self) -> typing.List[typing.Dict]:
        return self._order(self.data)

    def select_where(self, todo: str = '') -> typing.List[typing.Dict]:
        registers = []
        for register in self.data:
            if register.get('todo').startswith(todo):
                registers.append(register)

        return self._order(registers)

    def create_todo(self, todo: str, status: bool) -> None:
        if todo.strip() == '':
            raise EmptyTodo('Todo cannot be empty.')

        if self.select_where(todo=todo):
            raise TodoAlreadyExist(f'Todo {todo} already exists.')

        self.data.append({'todo': todo, 'status': status})
        self._save()

    def update_todo_status(self, todo: str, new_status: bool) -> None:
        for index, register in enumerate(self.data):
            if register.get('todo').startswith(todo):
                self.data[index] = {'todo': todo, 'status': new_status}
                self._save()
                break

    def delete_todo(self, todo: str) -> None:
        for index, register in enumerate(self.data):
            if register.get('todo').startswith(todo):
                del self.data[index]
                self._save()
                break


class TodoAlreadyExist(Exception):
    pass


class EmptyTodo(Exception):
    pass
