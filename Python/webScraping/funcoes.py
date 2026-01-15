def retornaUrls(numpaginas):
    urls = []
    for numero in range(1, numpaginas+1):
        url = f"https://quotes.toscrape.com/page/{numero}/"
        urls.append(url)
    return urls

def organizaListaCit(tags, url):
    lista = []
    for tag in tags:
        autor = tag.find("small", class_="author").get_text()
        frase = tag.find("span", class_="text").get_text()
        lista.append({'Autor': autor, 'Frase': frase, 'Origem': url})
    return lista