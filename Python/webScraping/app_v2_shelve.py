import requests
from bs4 import BeautifulSoup
import shelve
import os
import funcoes

# Criar pasta para dados shelve se não existir
pasta_dados = "dados_shelve"
if not os.path.exists(pasta_dados):
    os.makedirs(pasta_dados)

urls = funcoes.retornaUrls(10)
lista = []

for url in urls:
    conteudo = requests.get(url)
    soup = BeautifulSoup(conteudo.text, "html.parser")
    citacoes = soup.find_all("div", class_="quote")
    lista.extend(funcoes.organizaListaCit(citacoes, url))

# Salvar dados em arquivo shelve
caminho_shelve = os.path.join(pasta_dados, "citacoes.db")
with shelve.open(caminho_shelve, 'c') as db:
    db['citacoes'] = lista
    db['total_citacoes'] = len(lista)

print(f"Dados salvos em {caminho_shelve}")
print(f"Total de citações salvas: {len(lista)}")

