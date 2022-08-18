import tkinter as tk
import tkinter.ttk as ttk
import typing
from app import styles


class View(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.main_frame = MainFrame(self)
        self.main_frame.pack(side='top', fill='both', expand=True)

        styles.light_theme(self)
        self.title('Todo list')

    def set_columns(self, columns: typing.List[str]) -> None:
        table = self.main_frame.table
        table.set_columns(columns)

    def set_rows(
        self, rows: typing.List[typing.Tuple[typing.Any, ...]]
    ) -> None:
        table = self.main_frame.table
        table.set_rows(rows)

    def set_feedback(self, feedback: str) -> None:
        todo_input = self.main_frame.todo_input
        todo_input.set_feedback(feedback)
        self.focus_todo_input()

    def selection(self) -> typing.Optional[typing.Tuple[str, ...]]:
        return self.main_frame.table.selection()

    def todo(self) -> str:
        return self.main_frame.todo_input.text()

    def set_todo(self, todo: str) -> None:
        self.main_frame.todo_input.set_text(todo)

    def focus_todo_input(self) -> None:
        self.main_frame.todo_input.entry.focus()

    @property
    def delete_button(self) -> ttk.Button:
        return self.main_frame.delete_button

    @property
    def complete_button(self) -> ttk.Button:
        return self.main_frame.complete_button

    @property
    def add_button(self) -> ttk.Button:
        return self.main_frame.add_button


class MainFrame(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.config(padding=15)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.table = Table(self)
        self.table.set_columns(('todo', 'status'))

        self.todo_input = TextInput(self)

        self.delete_button = ttk.Button(self)
        self.delete_button.config(text='delete')

        self.add_button = ttk.Button(self)
        self.add_button.config(text='add todo')

        self.complete_button = ttk.Button(self)
        self.complete_button.config(text='complete')

        self.table.grid(row=0, column=0, columns=2, sticky='nsew', pady=10)
        self.delete_button.grid(row=1, column=0, sticky='ew', padx=5)
        self.complete_button.grid(row=1, column=1, sticky='ew', padx=5)
        self.todo_input.grid(
            row=2, column=0, columns=2, sticky='ew', padx=5, pady=10
        )
        self.add_button.grid(row=3, column=0, columns=2, sticky='ew', padx=5)


class Table(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.treeview = ttk.Treeview(self)
        self.treeview.config(show='headings')
        self.treeview.pack(side='left', fill='both', expand=True)

        self.scrollbar = ttk.Scrollbar(self)
        self.scrollbar.pack(side='right', fill='y')

        self.scrollbar.config(command=self.treeview.yview)
        self.treeview.config(yscrollcommand=self.scrollbar.set)

    def set_columns(self, columns: typing.Tuple[str, ...]) -> None:
        self.treeview.config(columns=columns)
        for column in columns:
            self.treeview.heading(column, text=column)
            self.treeview.column(column, anchor='center')

    def set_rows(
        self, rows: typing.List[typing.Tuple[typing.Any, ...]]
    ) -> None:
        self.treeview.delete(*self.treeview.get_children())
        for row in rows:
            self.treeview.insert('', 'end', values=row)

    def selection(self) -> typing.Optional[typing.Tuple[str, ...]]:
        selections = self.treeview.selection()
        if selections:
            values = self.treeview.item(selections[0])['values']
            return [str(value) for value in values]

        return None


class TextInput(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.entry_var = tk.StringVar()
        self.entry_var.trace_add('write', self._clear_feedback)
        self.entry = ttk.Entry(self)
        self.entry.config(textvariable=self.entry_var)
        self.entry.config(justify='center')
        self.entry.config(font='Arial 20 normal')
        self.entry.pack(side='top', fill='x')

        self.feedback_var = tk.StringVar()
        self.feedback = ttk.Label(self)
        self.feedback.config(textvariable=self.feedback_var)
        self.feedback.config(anchor='center')
        self.feedback.config(foreground='#ff0000')

    def _clear_feedback(self, *args) -> None:
        self.set_feedback('')

    def text(self) -> str:
        return self.entry_var.get()

    def set_text(self, text: str) -> None:
        self.entry_var.set(text)

    def set_feedback(self, feedback: str) -> None:
        self.feedback_var.set(feedback)
        self.feedback.pack_forget()
        if feedback:
            self.feedback.pack(side='top', fill='x')
