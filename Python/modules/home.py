import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
import sqlite3 
import os


def Home():
    from modules.estoque import Listar_produtos

    winHome = tk.Tk()
    winHome.title(f'Home')
    winHome.geometry('300x200') # Dimensões da pagina home

    icone = tk.PhotoImage(file="icon/ico.png") # Icone do programa na barra de tarefas
    winHome.iconphoto(True, icone )

    # Icones

    logo = tk.PhotoImage(file='icon/logo.png')

    iconEstoque = tk.PhotoImage(file="icon/Estoque.png")

    
    # Função alternar entre Janelas para Estoque:

    def HomexStq(winHome, Listar_produtos):
        winHome.destroy()
        Listar_produtos()


    # Botoes

    botao_Estoque = tk.Button(winHome, image=iconEstoque,text='Estoque', compound='top', command= lambda: HomexStq(winHome, Listar_produtos), width=150, height=70)
    botao_Estoque.grid(row= 1, column= 0, padx= 10, pady=10)

    logo_sistema = tk.Label(winHome, image=logo) # Logo
    logo_sistema.grid(row=2 ,column=2)
    
    
    winHome.mainloop()