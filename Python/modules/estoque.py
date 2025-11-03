import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox, filedialog
from tkinter import PhotoImage
from tkinter import Frame, Scrollbar, Listbox, VERTICAL, END
import sqlite3 
import os
    
    
if not os.path.exists("DB"):
    os.makedirs("DB")

# Variáveis
    
product_name = ""
product_qtd = 0
tipMov = ""

largura_tela = ""
altura_tela = "" 

# Função que cria tabelas necessárias e registros, caso nao tenha
def CriarTabela(): 
    sqlConect_stq = sqlite3.connect('DB/estoque.db') # conexão com DB
    sqlStq = sqlConect_stq.cursor()

    sqlStq.execute('''
                CREATE TABLE IF NOT EXISTS categorias (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome TEXT NOT NULL UNIQUE

                   );

                ''')

    sqlStq.execute('''
                CREATE TABLE IF NOT EXISTS produtos (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome TEXT NOT NULL UNIQUE,
                   categoria TEXT NOT NULL,
                   quantidade INTEGER,
                   valor_venda REAL,
                   valor_compra REAL,
                   data_adicao DATE DEFAULT (date('now')),
                   FOREIGN KEY (categoria) REFERENCES categorias(id) ON DELETE CASCADE

    );

    ''')
    
    sqlStq.execute(''' 
                CREATE TABLE IF NOT EXISTS movimentacoes (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   produto_id INTEGER,
                   nome TEXT,
                   categoria TEXT,
                   qtdnova INTEGER,
                   tipmov TEXT,
                   qtdantes INTEGER,
                   qtdatual INTEGER,
                   data DATE DEFAULT (date('now')),
                   FOREIGN KEY (nome) REFERENCES produtos(nome) ON DELETE SET NULL
                );

        ''') 
    

    
    sqlConect_stq.commit()

    #Registrar informações após inserir dados na tabela 
    sqlStq.execute('''
                CREATE TRIGGER IF NOT EXISTS trg_mov_add
                AFTER INSERT ON movimentacoes
                FOR EACH ROW
                WHEN NEW.tipmov = '+'
                BEGIN

                    -- Insere a quantidade disponível antes da movimentação
                    UPDATE movimentacoes 
                    SET qtdantes = (SELECT quantidade FROM produtos WHERE id = NEW.produto_id)
                    WHERE id = NEW.id;

                    -- Atualiza a quantidade atual de produtos  
                    UPDATE produtos
                    SET quantidade = quantidade + NEW.qtdnova
                    WHERE id = NEW.produto_id;

                    -- Define a quantidade após a movimentação
                    UPDATE movimentacoes
                    SET qtdatual = (SELECT quantidade FROM produtos WHERE id = NEW.produto_id)
                    WHERE id = NEW.id;
                   
                    -- Informa o nome do produto movimentado
                    UPDATE movimentacoes
                    SET nome = (SELECT nome FROM produtos WHERE id = NEW.produto_id)
                    WHERE id = NEW.id;
                   
                   
                   -- Informa a categoria do produto movimentado
                   UPDATE movimentacoes
                   SET categoria = (SELECT categoria FROM produtos WHERE id = NEW.produto_id)
                   WHERE id = NEW.id;
                   
                END;
            ''')
            
    sqlConect_stq.commit()

    #Registrar informações após inserir dados na tabela 
    sqlStq.execute('''
                CREATE TRIGGER IF NOT EXISTS trg_mov_rem
                AFTER INSERT ON movimentacoes
                FOR EACH ROW
                WHEN NEW.tipmov = '-'
                BEGIN
                   
                    -- Atualiza a quantidade disponível anterior a movimentação
                    UPDATE movimentacoes
                    SET qtdantes = (SELECT quantidade FROM produtos WHERE id = NEW.produto_id)
                    WHERE id = NEW.id;
                               
                    -- Atualiza a quantidade disponivel no estoque
                    UPDATE produtos 
                    SET quantidade =  quantidade - NEW.qtdnova 
                    WHERE id = NEW.produto_id;

                    -- Define a quantidade após a movimentação
                    UPDATE movimentacoes
                    SET qtdatual = (SELECT quantidade FROM produtos WHERE id = NEW.produto_id)
                    WHERE id = NEW.id;    
                   
                    -- Informa o nome do produto movimentado
                    UPDATE movimentacoes
                    SET nome = (SELECT nome FROM produtos WHERE id = NEW.produto_id)
                    WHERE id = NEW.id;
                   
                   -- Informa a categoria do produto movimentado
                   UPDATE movimentacoes
                   SET categoria = (SELECT categoria FROM produtos WHERE id = NEW.produto_id)
                   WHERE id = NEW.id;
                   
                END;
            ''')
            
    sqlConect_stq.commit()


# Função para atualizar as categorias da combobox
    
def update_categorias(combobox):
    sqlConect_stq = sqlite3.connect('DB/estoque.db') # conexão com DB
    sqlStq = sqlConect_stq.cursor()
    sqlStq.execute("SELECT nome FROM categorias")
    categorias = [row[0] for row in sqlStq.fetchall()]
    combobox['values'] = categorias


# Janelas

# Cadastro de categoria  
def cadastro_categoria(combobox):

    def salvar_categoria():
        nova_categoria = entry_novaCategoria.get().strip()
        if nova_categoria:
            sqlConect_stq = sqlite3.connect('DB/estoque.db') # conexão com DB
            sqlStq = sqlConect_stq.cursor()
            try:
                sqlStq.execute("INSERT INTO categorias (nome) VALUES (?)", (nova_categoria,))
                sqlConect_stq.commit()
                messagebox.showinfo("Sucesso","Nova categoria cadastrada com sucesso.")
                update_categorias(combobox)
                winCtg.destroy()

            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "A categoria já existe!")
            
        else:
            messagebox.showerror("Erro", "O campo não pode ficar vazio.")

    winCtg = tk.Toplevel()
    winCtg.title("Nova categoria")
    winCtg.geometry("450x150")

    nomeCtg_label = tk.Label(winCtg, text="Nome da nova categoria:")
    nomeCtg_label.grid(row=0, column=0, padx=10, pady=10)

    entry_novaCategoria = tk.Entry(winCtg)
    entry_novaCategoria.grid(row=0, column=1, padx=10, pady=10)

    save_button = tk.Button(winCtg, text="Salvar", command=salvar_categoria)
    save_button.grid(row=1, column=0, padx=10, pady=10)

    def CadcatxList():
        winCtg.destroy()
        Listar_produtos()

    button_return = tk.Button(winCtg, text="Voltar", command= CadcatxList)
    button_return.grid(row=2, column=0, padx=10, pady=10)




# Janela de cadastro de produto
    

def Cadastro_produto(): 

    sqlConect_stq = sqlite3.connect('DB/estoque.db') # conexão com DB
    sqlStq = sqlConect_stq.cursor()

    CriarTabela()

    global product_name
    global product_qtd
    

    valorCompra = 0,00
    valorVenda = 0,00

    winStqCad = tk.Tk()
    winStqCad.title("Cadastro de Produtos")
    winStqCad.geometry("700x450")

    # Função alternar entre janelas
    def CadprodxListstq():
        winStqCad.destroy()
        Listar_produtos()


    label_windowStq = tk.Label(winStqCad, text='Os campos do formulário que conter * no começo, é de preenchimento obrigatório')
    label_windowStq.grid(row=0, column=1, padx=10, pady=10)

    label_produtoNome = tk.Label(winStqCad, text='* Nome do produto')
    label_produtoNome.grid(row=1, column=0, padx=10, pady=10)
    
    product_name = tk.Entry(winStqCad)
    product_name.grid(row=1, column=1, padx=10, pady=10)

    label_produtoQtd = tk.Label(winStqCad, text='* Quantidade')
    label_produtoQtd.grid(row=2, column=0, padx=10, pady=10)

    product_qtd = tk.Entry(winStqCad)
    product_qtd.grid(row=2, column=1, padx=10, pady=10)

    label_valorCompra = tk.Label(winStqCad, text='Valor de Compra')
    label_valorCompra.grid(row=3, column=0, padx=10, pady=10)

    valorCompra = tk.Entry(winStqCad)
    valorCompra.grid(row=3, column=1, padx=10, pady=10)

    label_valorVenda = tk.Label(winStqCad, text='Valor de venda')
    label_valorVenda.grid(row=4, column=0, padx=10, pady=10)

    valorVenda = tk.Entry(winStqCad)
    valorVenda.grid(row=4, column=1, padx=10, pady=10)

    # Combobox para selecionar categoria existente
    label_categoria = tk.Label(winStqCad, text="Categoria:")
    label_categoria.grid(row=5, column=0, padx=10, pady=10)

    categoria_combobox = ttk.Combobox(winStqCad, state="readonly")
    categoria_combobox.grid(row=5, column=1, padx=5, pady=5)

    update_categorias(categoria_combobox) # verifica as categorias existente

    button_cadCtg = tk.Button(winStqCad, text="Cadastrar Categoria", command=lambda: cadastro_categoria(categoria_combobox))
    button_cadCtg.grid(row=6, column=0, padx=10, pady=10)



    def ApagarCat():

        categoria = categoria_combobox.get().strip()


        if categoria:
            
            messagebox.askyesno("Atenção", "Essa ação não poderá ser desfeita, produtos vinculados a esta categoria serão apagados. Recomendamos que certifique-se que foi feita a alteração antes de prosseguir.")

            sqlStq.execute("DELETE FROM categorias WHERE nome = ?", (categoria,))
            sqlConect_stq.commit()
            CadprodxListstq()

        else:
            messagebox.showerror("Erro", "Para deletar uma categoria é necessario selecionar uma.")


    button_delCat = tk.Button(winStqCad, text="Deletar categoria", command= ApagarCat)
    button_delCat.grid(row=6, column=1, padx=10, pady=10)




    '''  Função de cadastro de produtos   '''
    def AddProduct(): 
        sqlConect_stq = sqlite3.connect('DB/estoque.db') # conexão com DB
        sqlStq = sqlConect_stq.cursor()
        nome = product_name.get().strip()
        quantidade = product_qtd.get().strip()
        categoria = categoria_combobox.get().strip()
        vcompra = valorCompra.get().strip()
        vvenda = valorVenda.get().strip()
        valor_Compra = vcompra.replace(',' , '.')
        valor_Venda = vvenda.replace(',' , '.')
        valor_compra = float(valor_Compra)
        valor_venda = float(valor_Venda)

        if nome and quantidade:

            if categoria:

                # Busca o ID da categoria

                sqlStq.execute("SELECT id FROM categorias WHERE nome = ?",(categoria,))
                categoria_id = sqlStq.fetchone()
            
                if float(valor_Compra) and float(valor_Venda): # verifica se o valor inserido é numérico
                    
                    valor_compra1 = "{:.2f}".format(valor_compra)
                    valor_venda1 = "{:.2f}".format(valor_venda)

                    if int(quantidade):

                        sqlConect_stq = sqlite3.connect('DB/estoque.db')
                        sqlStq = sqlConect_stq.cursor()

                        sqlStq.execute("INSERT INTO produtos( nome, categoria, quantidade, valor_compra, valor_venda) VALUES ( ?, ?, ?, ?, ?)", ((nome), (categoria), int(quantidade), (valor_compra1), (valor_venda1)))


                        sqlConect_stq.commit()
                        sqlConect_stq.close()
                        messagebox.showinfo("Sucesso!", "Produto cadastrado com sucesso!")
                        categoria_combobox.set("")
                        CadprodxListstq()

                    else:
                        messagebox.showerror("Erro", "No campo quantidade deve ser inserido somente números")
                else:
                    messagebox.showerror("Erro", "nos campos valor de compra/venda devem ser caracteres númericos")
            else:
                messagebox.showerror("Falha", "É obrigatório informar a categoria")
        else:
            messagebox.showerror("Falha","Verifique os campos e tente novamente.") 



    button_cadastroProd = tk.Button(winStqCad, text="Cadastrar produto", command=AddProduct)
    button_cadastroProd.grid(row=7, column=0, padx=10, pady=10)
    
    button_return = tk.Button(winStqCad, text="Voltar", command=CadprodxListstq)
    button_return.grid(row=7, column=1, padx=10, pady=10)

    

    winStqCad.mainloop()





def Movimentar_produto(): # Janela de movimentar produto
     
    # Variaveis da funcao
    
    operacao = ''
    entry_produtoId = ""
    entry_qtdTransf = ""
    global tipoMov 

    CriarTabela()

    def registrar_mov(): # Função movimentar estoque
        produto_id = entry_produtoId.get().strip()
        qtdnova = entry_qtdTransf.get().strip()
        global operacao

        if produto_id and qtdnova:
            sqlConect_stq = sqlite3.connect('DB/estoque.db') # conexão com DB
            sqlStq = sqlConect_stq.cursor()

            sqlStq.execute("SELECT quantidade FROM produtos WHERE id = ?",(produto_id,))
            qtd_disponivel = sqlStq.fetchone()

            if qtd_disponivel:  # Verificar se o resultado da consulta não é None
                qtd_estoque = qtd_disponivel[0]
                qtd = int(qtd_estoque)

                try: # Verificar se o valor inserido é um valor inteiro
                    novaqtd = int(qtdnova)
            
                    if operacao == "-": # Verifica se há quantidade suficiente
                        if qtd >= novaqtd: 
                            sqlStq.execute("INSERT INTO movimentacoes (produto_id, qtdnova, tipmov) VALUES (?, ?, ?)", (int(produto_id), int(qtdnova), '-'))
            
                            sqlConect_stq.commit()
                            messagebox.showinfo("Sucesso!","Movimentação registrada.")
                            
                            winStqMov.destroy()
                            Listar_produtos()

                        else:
                            messagebox.showerror("Erro", "Estoque insuficiente, verifique a quantidade disponível em seu estoque")

                    elif operacao == "+":
                        sqlStq.execute("INSERT INTO movimentacoes (produto_id, qtdnova, tipmov) VALUES (?, ?, ?)", (int(produto_id), int(qtdnova), '+'))
            
                        sqlConect_stq.commit()
            

                        messagebox.showinfo("Sucesso!","Movimentação registrada.")

                        winStqMov.destroy()
                        Listar_produtos()
                        
                    else:
                        messagebox.showerror("Falha", "Operação não identificada")

                except: # Bug, esse aviso aparece toda vez que movimenta um produto
                    messagebox.showerror("Atenção","Nos campos devem ser digitados somente números")

            else:
                messagebox.showerror("Produto não encontrado", "O produto especificado não foi encontrado no estoque.")   

        else:
            messagebox.showerror("Falha", "Verifique se os campos foram preenchidos corretamente e tente novamente.")
        


    winStqMov = tk.Tk()
    winStqMov.title("Movimentação de produto")
    winStqMov.geometry('520x350')

    label_produtoId = tk.Label(winStqMov, text='ID do Produto:')
    label_produtoId.grid( row=0, column=0, padx=10, pady=10)

    entry_produtoId = tk.Entry(winStqMov)
    entry_produtoId.grid( row=0, column=1, padx=10, pady=10)

    label_produtoqtd = tk.Label(winStqMov, text='Quantidade:')
    label_produtoqtd.grid(row=1, column=0, padx=10, pady=10)

    entry_qtdTransf = tk.Entry(winStqMov)
    entry_qtdTransf.grid(row=1, column=1, padx=10, pady=10)

    # Função para definir a operação.
    operacao = ""
    
    def movButtonAdd():
        global operacao 
        operacao = "+"
        registrar_mov()

    def movButtonRem():
        global operacao 
        operacao = "-"
        registrar_mov()



    button_addProd = tk.Button(winStqMov, text='+', command= movButtonAdd)
    button_addProd.grid(row=2, column=0, padx=10, pady=10)

    button_remProd = tk.Button(winStqMov, text='-', command= movButtonRem)
    button_remProd.grid(row=2, column=1, padx=10, pady=10)


    # Função alternar entre janelas para Estoque:
    def MovprodxStq(winStqMov,Listar_produtos):
        winStqMov.destroy()
        Listar_produtos()


    button_return = tk.Button(winStqMov, text='Voltar', command= lambda: MovprodxStq(winStqMov,Listar_produtos))
    button_return.grid(row=2, column=2, padx=10, pady=10)



    winStqMov.mainloop()


# Função carregar produtos do banco de dados
def UpdateStq(tree, coluna=None, ordem="ASC"):
    sqlConect_stq = sqlite3.connect('DB/estoque.db') # conexão com DB
    sqlStq = sqlConect_stq.cursor()


    if coluna:
        query = f"SELECT id, nome, categoria, quantidade, valor_venda, valor_compra, data_adicao FROM produtos ORDER BY {coluna} {ordem}"
    else:
        query = f"SELECT id, nome, categoria, quantidade, valor_venda, valor_compra, data_adicao FROM produtos"

    sqlStq.execute(query)
    produtosStq = sqlStq.fetchall()

    tree.delete(*tree.get_children())

    for row in produtosStq:
        tree.insert("", "end", values=row)

def ordenar_coluna(tree, coluna, ordem_atual):
    nova_ordem = "ASC" if ordem_atual == "DESC" else "DESC"
    
    UpdateStq(tree, coluna, nova_ordem)

    # Atualizar o comando do cabeçalho da coluna
    tree.heading(coluna, command=lambda: ordenar_coluna(tree, coluna, nova_ordem))




def Listar_produtos():  # Janela principal (Produtos listado)
    from modules.home import Home
    

    sqlConect_stq = sqlite3.connect('DB/estoque.db') # conexão com DB
    sqlStq = sqlConect_stq.cursor()

    CriarTabela()

    global altura_tela, largura_tela

    winStqProd = tk.Tk()
    winStqProd.title("Estoque")

    winStqProd.grid_rowconfigure(1, weight=1) # Permite o usuário ajustar a linha
    winStqProd.grid_columnconfigure(0, weight=1) # permite o usuário ajustar a coluna
    
    global altura_tela, largura_tela

    largura_tela= winStqProd.winfo_screenwidth()
    altura_tela = winStqProd.winfo_screenheight()

    winStqProd.geometry(f"{largura_tela}x{altura_tela}+0+0")

        # Função alternar janela para Menu
    def ListProdStqxMenu(winStqProd,Home):
        sqlConect_stq.close()
        winStqProd.destroy()
        Home()


    button_return = tk.Button(winStqProd, text='Menu',command= lambda: ListProdStqxMenu(winStqProd,Home))
    button_return.grid(row=0, column=0, padx=10, pady=10)

    # Alternar Janela para Cadastrar produto
    def ListStqxCadProd(winStqProd,Cadastro_produto):
        winStqProd.destroy()
        Cadastro_produto()

    button_newProduct = tk.Button(winStqProd, text='Produto/Categoria', command= lambda: ListStqxCadProd(winStqProd,Cadastro_produto))
    button_newProduct.grid(row=0, column=1, padx=10, pady=10)

    # Função alternar entre janelas para Movimentar:
    
    def WinstqxMovstq(winStqProd, Movimentar_produto):
        winStqProd.destroy()
        Movimentar_produto()
   
    button_movimentar = tk.Button(winStqProd, text='Movimentar', command= lambda: WinstqxMovstq(winStqProd, Movimentar_produto))
    button_movimentar.grid(row=0, column=2, padx=10, pady=10)
    
    def ListxEdit(winStqProd, editarProduto):
        winStqProd.destroy()
        editarProduto()

    button_editar = tk.Button(winStqProd, text="Editar/Excluir", command= lambda: ListxEdit(winStqProd, editarProduto))
    button_editar.grid(row=0, column=3, padx=10, pady=10)

    def ListxRelat(winStqProd, RelatMov_estoque):
        winStqProd.destroy()
        RelatMov_estoque()

    button_relat = tk.Button(winStqProd, text="Registro de Movimentação", command= lambda: ListxRelat(winStqProd, RelatMov_estoque))
    button_relat.grid(row=0, column=4, padx=10, pady=10)

    # Configurando a tabela
    colunaList = ("ID", "NOME", "CATEGORIA", "QUANTIDADE", "VALOR VENDA", "CUSTO", "DT REGISTRO")
    tree = ttk.Treeview( winStqProd, columns= colunaList, show="headings", height=25)
    tree.grid(row=1, columnspan=5, padx=10, pady=10, sticky="nsew")

    # Configurar coluna

    for col in colunaList:
        tree.heading(col, text=col.capitalize(), command=lambda _col=col: ordenar_coluna(tree, _col, "ASC"))
        tree.column(col, width=120, anchor="center")


    # Carrega os dados do banco de dados
    UpdateStq(tree)

    scroll_y = ttk.Scrollbar(winStqProd, orient="vertical", command=tree.yview)
    scroll_y.grid(side="right", fill="y")
    tree.configure(yscrollcommand=scroll_y.set)

    winStqProd.update_idletasks()
    winStqProd.mainloop()


    
def update_relat(): # Carregar dados de relatorio

    sqlConect_stq = sqlite3.connect('DB/estoque.db') # conexão com DB
    sqlStq = sqlConect_stq.cursor()

    
    sqlStq.execute("SELECT id, produto_id, nome, categoria, qtdantes, tipmov, qtdnova, qtdatual, data FROM movimentacoes")
    reg_Mov = sqlStq.fetchall()

    return reg_Mov

# Janela de relatorio de estoque 

def RelatMov_estoque():

    sqlConect_stq = sqlite3.connect('DB/estoque.db') # conexão com DB
    sqlStq = sqlConect_stq.cursor()  
    
    global largura_tela, altura_tela

    winRelat = tk.Tk()
    winRelat.title("Registro de movimentações")
    winRelat.geometry(f'{largura_tela}x{altura_tela}+0+0')

    winRelat.grid_rowconfigure(1, weight=1) # Linha da tabela ajustável
    winRelat.grid_columnconfigure(0, weight=1)  # Coluna da tabela ajustável
    

    def AltwinRelatxStq(winRelat,Listar_produtos):
        winRelat.destroy()
        Listar_produtos()

    button_return = tk.Button(winRelat, text="Voltar", command= lambda: AltwinRelatxStq(winRelat , Listar_produtos))
    button_return.grid(row=0, column=0, padx=10, pady=10)

    # Criação de tabelas
    colunasRelat = ("ID", "PRODUTO ID", "PRODUTO", "CATEGORIA", "QTD ANTES", "OPERAÇÃO", "NOVA QTD", "QTD ATUAL", "DATA")
    tree = ttk.Treeview(winRelat, columns= colunasRelat, show="headings", height=25)
    tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")


    # Configuração de colunas
    for col in colunasRelat:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    # Consulta os dados e preenchimento da tabela
    dadosRelatStq = update_relat()

    try:

        if dadosRelatStq:
            for relatorioEstoque in dadosRelatStq:
                tree.insert("", "end", values=relatorioEstoque) #insere os dados na tabela
        
        else:
            messagebox.showinfo("Ops", "Ainda não há registros de movimentações")
    
    except Exception as e15:
        messagebox.showerror("Erro", f" Erro codigo: {e15}")


    scroll_y = ttk.Scrollbar(winRelat, orient="vertical", command=tree.yview)
    scroll_y.grid(side="right", fill="y")
    tree.configure(yscrollcommand=scroll_y.set)

    
    winRelat.update_idletasks()
    winRelat.mainloop()


# Janela para editar e ou remover produto

def editarProduto(): 

    sqlConect_stq = sqlite3.connect('DB/estoque.db') # conexão com DB
    sqlStq = sqlConect_stq.cursor()

    winedit = tk.Tk()
    winedit.title("Editar/Apagar Produto")
    winedit.geometry("400x200")
    

    label_produtoId = tk.Label(winedit, text="ID do Produto:")
    label_produtoId.grid(row=0, column=0, padx=10, pady=10)

    entry_produtoId = tk.Entry(winedit)
    entry_produtoId.grid(row=0, column=1, padx=10, pady=10)


    def Buscarprod():
        produto_id = entry_produtoId.get().strip()

        # Buscar o produto no banco de dados

        sqlStq.execute("SELECT * FROM produtos WHERE id = ?",(produto_id,))
        produto = sqlStq.fetchone()

        # Janela editar produto

        if produto:  

            

            editProd = tk.Tk()
            editProd.title("Editar/Apagar produto")
            editProd.geometry("480x500")

            label_produto = tk.Label(editProd, text="Nome:")
            label_produto.grid(row=0, column=0, padx=10, pady=10)

            entry_prod = tk.Entry(editProd)
            entry_prod.grid(row=0, column=1, padx=10, pady=10)

            label_categoria = tk.Label(editProd, text="Categoria:")
            label_categoria.grid(row=1, column=0, padx=10, pady=10)

            combobox_categoria = ttk.Combobox(editProd, state="readonly")
            combobox_categoria.grid(row=1, column=1, padx=10, pady=10)

            # Atualizar a lista categoria

            update_categorias(combobox_categoria)

            label_valorC = tk.Label(editProd, text="Valor de compra:")
            label_valorC.grid(row=2, column=0, padx=10, pady=10)

            entry_valorC = tk.Entry(editProd)
            entry_valorC.grid(row=2, column=1, padx=10, pady=10)

            label_valorV = tk.Label(editProd, text="Valor de venda:")
            label_valorV.grid(row=3, column=0, padx=10, pady=10)

            entry_valorV = tk.Entry(editProd)
            entry_valorV.grid(row=3, column=1, padx=10, pady=10)

            entry_prod.insert(0, produto[1])
            combobox_categoria.set(produto[2])
            entry_valorC.insert(0, produto[5])
            entry_valorV.insert(0, produto[4])
            
            # Limpar campos
            def limpar_form():
                entry_produtoId.delete(0, tk.END)
                entry_prod.delete(0, tk.END)
                combobox_categoria.set("")
                entry_valorC.delete(0, tk.END)
                entry_valorV.delete(0, tk.END)


            def editprodxwinedit():
                limpar_form()
                editProd.destroy()
                Listar_produtos()

            button_return = tk.Button(editProd, text="Voltar", command= editprodxwinedit)
            button_return.grid(row=5, column=0, padx=10, pady=10)

            def SalvarAlt():
                nome = entry_prod.get().strip()
                categoria = combobox_categoria.get().strip()
                valorC = entry_valorC.get().strip()
                valorV = entry_valorV.get().strip()
                valorC1 = valorC.replace(",", ".")
                valorV1 = valorV.replace(",", ".")
                valorc = float(valorC1)
                valorv = float(valorV1)


                if float(valorC1) and float(valorV1):  
                    valorc1 = "{:.2f}".format(valorc)
                    valorv1 = "{:.2f}".format(valorv)

                    sqlStq.execute("UPDATE produtos SET nome = ?, categoria = ?, valor_venda = ?, valor_compra = ? WHERE id = ?" , (nome, categoria, valorv1, valorc1, produto_id))
                    sqlConect_stq.commit()

                    messagebox.showinfo("Sucesso!", "Produto alterado com sucesso.")

                    limpar_form()

                    editprodxwinedit()

                else:
                    messagebox.showerror("Erro", "Os valores Compra/Venda estão incorretos, verifique novamente os campos.")

            button_confirm = tk.Button(editProd, text="Confirmar", command= SalvarAlt)
            button_confirm.grid(row=4, column=0, padx=10, pady=10)

            def DelProd():
                confirmacao = messagebox.askyesno("Atenção", "Tem certeza que deseja deletar o produto ? (Esta ação não poderá ser desfeita.)")

                if confirmacao:
                    sqlStq.execute("DELETE FROM produtos WHERE id = ?", (produto_id))
                    sqlConect_stq.commit()

                    messagebox.showinfo("Sucesso!", "Produto deletado com sucesso")

                    limpar_form()

                    editprodxwinedit()


            button_del = tk.Button(editProd, text="Deletar", command= DelProd)
            button_del.grid(row=4, column=2, padx=10, pady=10)


            editProd.mainloop()

        else:
            messagebox.showerror("Erro", "Produto não encontrado, verifique o campo e tente novamente.")

    
    button_confirm = tk.Button(winedit, text="Buscar produto", command= Buscarprod)
    button_confirm.grid(row=1, column=0, padx=10, pady=10)


    def EditprodxLista(winedit,Listar_produtos):
        winedit.destroy()
        Listar_produtos()

    button_return = tk.Button(winedit, text="Voltar", command= lambda: EditprodxLista(winedit,Listar_produtos))
    button_return.grid(row=1, column=1, padx=10, pady=10)


    winedit.mainloop()

  