import tkinter as tk
import requests as rq
import pandas as pd
import os
from tkinter import messagebox

#pyinstaller --onefile main.py

def iniciar_processo():
    data_inicio = entry_data_inicio.get()
    data_fim = entry_data_fim.get()

    path_name = "ContratoScrap.xlsx"
    BASE = "https://compras.dados.gov.br/comprasContratos/v1/contratos.json"
    response = rq.get(f"{BASE}?data_assinatura_max={data_fim}&data_assinatura_min={data_inicio}").json()["_embedded"]

    contratos_clean = [x for x in response["contratos"]]

    if os.path.exists(path_name):

        dados_antigos = pd.read_excel(path_name)["id"]

        contratos_novos = [x for x in contratos_clean if x["id"] not in dados_antigos]
        df = pd.DataFrame(contratos_novos)
        df.sort_values(by="id")
        df.to_excel(path_name, index=False)

    else:
        df = pd.DataFrame(contratos_clean)
        df.sort_values(by="id")
        df.to_excel(path_name, index=False)

    # Exemplo simples: Mostrar um diálogo com as datas selecionadas
    messagebox.showinfo("Sucesso!", "Os dados foram salvos no arquivo: ContratoScrap.xlsx")


# Criar a janela principal
root = tk.Tk()
root.title("Seleção de Datas")

# Adicionar um rótulo com o texto
label_texto = tk.Label(root, text="Coloque a data de inicio e de fim nesse modelo: ano-mês-dia")
label_texto.pack()

# Adicionar campos de entrada para data inicial e final
label_data_inicio = tk.Label(root, text="Data de Início:")
label_data_inicio.pack()
entry_data_inicio = tk.Entry(root)
entry_data_inicio.pack()

label_data_fim = tk.Label(root, text="Data de Fim:")
label_data_fim.pack()
entry_data_fim = tk.Entry(root)
entry_data_fim.pack()

# Adicionar um botão para iniciar o processo
botao_iniciar = tk.Button(root, text="Iniciar", command=iniciar_processo)
botao_iniciar.pack()

# Iniciar a interface gráfica
root.mainloop()
