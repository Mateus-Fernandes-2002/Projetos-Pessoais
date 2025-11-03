import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
import sqlite3 
import os
if not os.path.exists('DB'):  #verifica a existencia da pasta DB
    os.makedirs('DB')

user_files = 'DB/users.db' #Caminho para o arquivo banco de dados



# Variaveis 

entry_password = ""

entry_username = "" # ID de usuario

var_checkbox1= None # Variavél para armazenar o estado da caixinha


# Janela Login:
        
def Abrir_login():


    sqlConect = sqlite3.connect(user_files) #Conectar ao banco de dados ( Vai criar se nao existir)
    sqlUser_files = sqlConect.cursor()

    # cria tabela de usuários se nao existir
    sqlUser_files.execute('''
                           
        CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT  NOT NULL,
            acesso INTEGER        
        )
    ''')

    sqlConect.commit()

    def EspiarSenhaLg():
        if var_checkbox1.get() == 1:
            entry_password.configure(show="")
        else:
            entry_password.configure(show="*")

    from modules.registro import Abrir_registro
    import modules.home as home
    from modules.home import Home

    winLg = tk.Tk() #Janela Cadastro
    winLg.title(f"Login")
    winLg.geometry("460x200")

    icone = tk.PhotoImage(file="icon/ico.png") # Icone do programa na barra de tarefas
    winLg.iconphoto(True, icone)


    label_id = tk.Label(winLg, text="ID") #Label[ID] 
    label_id.grid(row=0,column=0,padx=10,pady=10)

    global entry_id
    global entry_password
    global var_checkbox1
    var_checkbox1 = tk.IntVar(value=0) # Variavél para armazenar o estado da caixinha
    
    # Caixinha espiar
    checkbox1 = tk.Checkbutton(winLg, text="Espiar senha",variable=var_checkbox1, command=EspiarSenhaLg)
    checkbox1.grid(row=2,column=0,pady=10)

    label_password = tk.Label(winLg,text="Senha") #label[Senha]
    label_password.grid(row=1, column=0,padx=10,pady=10)

    entry_id = tk.Entry(winLg) #Entrada de resposta [Usuário]
    entry_id.grid(row=0, column=1, padx=10, pady=10)


    entry_password = tk.Entry(winLg,show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=10)

    entry_confirmPassword = ""

    # Função alternar entre janelas.

    def AltWinLxR(winLg, Abrir_registro):
        winLg.destroy()
        Abrir_registro()


    def AltWinLxHome():
        sqlConect.close()
        winLg.destroy()
        Home()
        

        # Função login

    def Login_usuario():
        id_login = entry_id.get().strip()
        password_login = entry_password.get().strip()
        
        try: 
            id_user = int(id_login)

            if id_user and password_login:
                sqlUser_files.execute('SELECT * FROM users WHERE id=? and password=?',(id_user, password_login))
                if sqlUser_files.fetchone():
                    messagebox.showinfo("Login","Login bem-sucedido.")
                    AltWinLxHome()
                else:
                    messagebox.showerror("Erro","ID ou senha estão incorretos ")
            else:
                messagebox.showerror("Erro","Preencha todos os campos.")
        except:
            messagebox.showerror("Erro", "ID deve-se digitar somente números")
    


    botao_wl_login = tk.Button(winLg, text="Login", command=Login_usuario) 
    botao_wl_login.grid(row=2, column=1, padx=10, pady=10) # Botao login

    botao_wl_registro = tk.Button(winLg, text="Registro", command= lambda: AltWinLxR(winLg, Abrir_registro) )
    botao_wl_registro.grid(row=2, column=2, padx=10, pady=10) # Botao registro

    

    winLg.mainloop()



