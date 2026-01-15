# com recursividade
def contagemRegressiva(num):
    if num <= 0:
        print("Fim")
    else:
        print(num)
        contagemRegressiva(num-1)

contagemRegressiva(5)