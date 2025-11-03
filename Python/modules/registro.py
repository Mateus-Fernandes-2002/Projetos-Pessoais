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
entry_confirmPassword = ""
entry_username = ""
entry_id = ""







def Abrir_registro():

    sqlConect = sqlite3.connect(user_files) #Conectar ao banco de dados ( Vai criar se nao existir)
    sqlUser_files = sqlConect.cursor()



    def EspiarSenhaRg():
        if var_checkboxr.get() == 1:
            entry_password.configure(show="")
            entry_confirmPassword.configure(show="")
        else:
            entry_password.configure(show="*")
            entry_confirmPassword.configure(show="*")

    
    import modules.login as login
    
    winRg = tk.Tk()
    winRg.title(" Registro ")
    winRg.geometry("460x350") 

    icone = tk.PhotoImage(file="icon/ico.png") # Icone do programa na barra de tarefas
    winRg.iconphoto(True, icone)

    label_id = tk.Label(winRg, text="ID (deve conter 4 dig):")
    label_id.grid(column=0, row=0, padx=10, pady=10)

    label_username = tk.Label(winRg,text='Usuário:')
    label_username.grid(column=0, row=1, padx=10, pady=10)

    label_password = tk.Label(winRg, text='Senha:')
    label_password.grid(column=0, row=2 , padx= 10, pady=10)

    label_confirmPassword = tk.Label(winRg, text='Repita a senha:')
    label_confirmPassword.grid(column=0, row=3, padx=10, pady=10)


    var_checkboxr = tk.IntVar( value=0 )


    checkboxr = tk.Checkbutton(winRg, text="Espiar senha", variable=var_checkboxr, command=EspiarSenhaRg)
    checkboxr.grid(column=0, row=4, pady=10)

    entry_id = tk.Entry(winRg)
    entry_id.grid(column=1, row=0, padx=10, pady=10)
    
    entry_username = tk.Entry(winRg)
    entry_username.grid(column=1, row=1, padx=10, pady=10)

    entry_password = tk.Entry(winRg,show='*')
    entry_password.grid(column=1, row=2, padx=10, pady=10)

    entry_confirmPassword =tk.Entry(winRg,show='*')
    entry_confirmPassword.grid(column=1, row=3, padx=10, pady=10)

    # Função alternar entre janelas.

    def AltWinRxL(winRg,Abrir_login):
        winRg.destroy()
        Abrir_login()


    def Registrado():
        from modules.login import Abrir_login
        messagebox.showinfo("Registrado!","retornando para tela de login")
        winRg.destroy()
        Abrir_login()

        #Função de registro

    def Registro_usuario():  
        id_registro = entry_id.get().strip()
        username_registro = entry_username.get().strip()
        password_registro = entry_password.get().strip()
        confirmPassword_registro = entry_confirmPassword.get().strip()

        if len(id_registro) == 4:

            try: 
                id_user = int(id_registro)

                if id_registro and username_registro and password_registro:
                    if password_registro and confirmPassword_registro:
                        try:
                            sqlUser_files.execute('INSERT INTO users (id, username, password) VALUES (?,?,?)', (id_user, username_registro, password_registro))
                            sqlConect.commit()
                            messagebox.showinfo('Registro','Registrado com sucesso!')
                            Registrado()

                        except sqlite3.IntegrityError:
                            messagebox.showerror('Erro', 'Ops... já existe um usuário com esse nome.')
                    else:
                        messagebox.showerror("Erro","As senhas informadas não conferem.")
                else:
                    messagebox.showerror("Erro","Preencha todos os campos.")
            except:
                messagebox.showerror("Erro", "O ID deve ser somente números")
        else:
            messagebox.showerror("Erro", "A ID deve conter 4 digitos")



    button_register = tk.Button(winRg, text="Registrar-se", command= Registro_usuario)
    button_register.grid(column=1, row=4, padx=10, pady=10)

    return_wr = tk.Button(winRg, text="Voltar",command= lambda: AltWinRxL(winRg,login.Abrir_login))
    return_wr.grid(column=2, row=4, padx=10, pady=10) # Botao para retornar ao inicio

    


    winRg.mainloop()



