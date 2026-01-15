import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://quotes.toscrape.com/"
conteudo = requests.get(url)

#escrever = open("quotes.txt", "w", encoding="utf-8")
#for linha in conteudo.text:
#    escrever.write(linha)
#escrever.close()
#print(conteudo.text)

soup = BeautifulSoup(conteudo.text, "html.parser")
citacoes = soup.find_all("div", class_="quote")

#print(type(citacoes))
#frase = citacoes[0].find("span", class_="text").get_text())

lista = []
for elemento in citacoes:
    frase = elemento.find("span", class_="text").get_text()
    autor = elemento.find("small", class_="author").get_text()
    lista.append({'Citacao': frase, 'Autor': autor})

df = pd.DataFrame(lista)
df.to_excel("citacoes.xlsx", index=False)