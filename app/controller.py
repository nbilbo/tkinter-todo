from sqlite3 import register_adapter
from app import view
from app import model
from app import constants


class Controller:
    def __init__(self) -> None:
        self.model = model.Model(constants.DATABASE_NAME)
        self.view = view.View()
        self.update_table()
        self.view.focus_todo_input()

        self.view.add_button.config(command=self.add_todo)
        self.view.complete_button.config(command=self.complete_todo)
        self.view.delete_button.config(command=self.delete_todo)

    def start(self) -> None:
        self.view.mainloop()

    def update_table(self) -> None:
        registers = []
        for register in self.model.select_todo():
            todo = register.get('todo')
            status = register.get('status')
            status_unicode = '\u2714' if status else '\u274C'
            registers.append((todo, status_unicode))
        self.view.set_rows(registers)

    def add_todo(self) -> None:
        try:
            self.view.set_feedback('')
            todo = self.view.todo().lower()
            self.model.create_todo(todo, False)
            self.update_table()
            self.view.set_todo('')
        except model.EmptyTodo:
            self.view.set_feedback('Required field.')
        except model.TodoAlreadyExist:
            self.view.set_feedback('Already exists.')

    def complete_todo(self) -> None:
        selection = self.view.selection()
        if selection:
            todo = selection[0].lower()
            register = self.model.select_where(todo=todo)[0]
            current_status = register.get('status')
            new_status = not current_status
            self.model.update_todo_status(todo, new_status)
            self.update_table()
            self.view.focus_todo_input()

    def delete_todo(self) -> None:
        selection = self.view.selection()
        if selection:
            todo = selection[0].lower()
            self.model.delete_todo(todo)
            self.update_table()
            self.view.focus_todo_input()
