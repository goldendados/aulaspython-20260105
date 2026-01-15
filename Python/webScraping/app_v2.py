import requests
from bs4 import BeautifulSoup
import pandas as pd
import funcoes

urls = funcoes.retornaUrls(10)
lista = []

for url in urls:
    conteudo = requests.get(url)
    soup = BeautifulSoup(conteudo.text, "html.parser")
    citacoes = soup.find_all("div", class_="quote")
    lista.extend(funcoes.organizaListaCit(citacoes, url))

df = pd.DataFrame(lista)
df.to_excel("citacoes.xlsx", index=False)