import tkinter as tk
import tkinter.ttk as ttk


def light_theme(root: tk.Tk) -> None:
    color_0 = '#F2ECE4'
    color_0 = '#ffffff'
    color_1 = '#98D936'
    color_2 = '#4ABF2A'
    color_3 = '#01261C'

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('.', background=color_0)
    style.configure('.', font='Consolas 20 normal')

    style.configure('TEntry', bordercolor=color_2)
    style.configure('TEntry', lightcolor=color_2)
    style.configure('TEntry', darkcolor=color_2)
    style.map('TEntry', bordercolor=[('focus', color_3)])
    style.map('TEntry', lightcolor=[('focus', color_3)])
    style.map('TEntry', darkcolor=[('focus', color_3)])

    style.configure('TButton', background=color_1)
    style.map(
        'TButton', background=[('pressed', color_3), ('active', color_2)]
    )
    style.map(
        'TButton', foreground=[('pressed', color_0), ('active', color_0)]
    )

    style.configure('Treeview', rowheight=40)
    style.configure('Treeview.Heading', font='Consolas 16 normal')
