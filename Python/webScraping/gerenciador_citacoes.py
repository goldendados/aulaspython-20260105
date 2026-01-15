import shelve
import os
from typing import List, Dict, Optional

# Cores para o terminal (ANSI escape codes)
class Cores:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    VERDE = '\033[92m'
    AZUL = '\033[94m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    CIANO = '\033[96m'
    MAGENTA = '\033[95m'

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_menu():
    """Exibe o menu principal"""
    print(f"\n{Cores.CIANO}{'='*60}{Cores.RESET}")
    print(f"{Cores.BOLD}{Cores.AZUL}{' '*15}GERENCIADOR DE CITAÇÕES{Cores.RESET}")
    print(f"{Cores.CIANO}{'='*60}{Cores.RESET}\n")
    print(f"{Cores.VERDE}[1]{Cores.RESET} Listar todas as citações")
    print(f"{Cores.VERDE}[2]{Cores.RESET} Buscar citação por índice")
    print(f"{Cores.VERDE}[3]{Cores.RESET} Inserir nova citação")
    print(f"{Cores.VERDE}[4]{Cores.RESET} Alterar citação existente")
    print(f"{Cores.VERDE}[5]{Cores.RESET} Deletar citação")
    print(f"{Cores.VERDE}[6]{Cores.RESET} Estatísticas")
    print(f"{Cores.VERMELHO}[0]{Cores.RESET} Sair")
    print(f"\n{Cores.CIANO}{'='*60}{Cores.RESET}\n")

def carregar_citacoes(caminho_shelve: str) -> List[Dict]:
    """Carrega as citações do arquivo shelve"""
    try:
        with shelve.open(caminho_shelve, 'r') as db:
            return db.get('citacoes', [])
    except Exception as e:
        print(f"{Cores.VERMELHO}Erro ao carregar dados: {e}{Cores.RESET}")
        return []

def salvar_citacoes(caminho_shelve: str, citacoes: List[Dict]):
    """Salva as citações no arquivo shelve"""
    try:
        with shelve.open(caminho_shelve, 'w') as db:
            db['citacoes'] = citacoes
            db['total_citacoes'] = len(citacoes)
        return True
    except Exception as e:
        print(f"{Cores.VERMELHO}Erro ao salvar dados: {e}{Cores.RESET}")
        return False

def listar_citacoes(citacoes: List[Dict]):
    """Lista todas as citações"""
    if not citacoes:
        print(f"{Cores.AMARELO}Nenhuma citação encontrada.{Cores.RESET}")
        return
    
    print(f"\n{Cores.BOLD}{Cores.AZUL}{'='*60}{Cores.RESET}")
    print(f"{Cores.BOLD}{Cores.AZUL}Total de citações: {len(citacoes)}{Cores.RESET}")
    print(f"{Cores.BOLD}{Cores.AZUL}{'='*60}{Cores.RESET}\n")
    
    for idx, citacao in enumerate(citacoes, 1):
        print(f"{Cores.CIANO}[{idx}]{Cores.RESET}")
        print(f"  {Cores.BOLD}Autor:{Cores.RESET} {citacao.get('Autor', 'N/A')}")
        print(f"  {Cores.BOLD}Frase:{Cores.RESET} {citacao.get('Frase', 'N/A')}")
        print(f"  {Cores.BOLD}Origem:{Cores.RESET} {citacao.get('Origem', 'N/A')}")
        print(f"{Cores.CIANO}{'-'*60}{Cores.RESET}\n")

def buscar_citacao(citacoes: List[Dict]):
    """Busca uma citação por índice"""
    if not citacoes:
        print(f"{Cores.AMARELO}Nenhuma citação encontrada.{Cores.RESET}")
        return
    
    try:
        idx = int(input(f"{Cores.CIANO}Digite o índice da citação (1-{len(citacoes)}): {Cores.RESET}"))
        if 1 <= idx <= len(citacoes):
            citacao = citacoes[idx - 1]
            print(f"\n{Cores.BOLD}{Cores.AZUL}{'='*60}{Cores.RESET}")
            print(f"{Cores.BOLD}Índice: {idx}{Cores.RESET}")
            print(f"{Cores.BOLD}Autor:{Cores.RESET} {citacao.get('Autor', 'N/A')}")
            print(f"{Cores.BOLD}Frase:{Cores.RESET} {citacao.get('Frase', 'N/A')}")
            print(f"{Cores.BOLD}Origem:{Cores.RESET} {citacao.get('Origem', 'N/A')}")
            print(f"{Cores.BOLD}{Cores.AZUL}{'='*60}{Cores.RESET}\n")
        else:
            print(f"{Cores.VERMELHO}Índice inválido!{Cores.RESET}")
    except ValueError:
        print(f"{Cores.VERMELHO}Por favor, digite um número válido.{Cores.RESET}")

def inserir_citacao(citacoes: List[Dict]) -> bool:
    """Insere uma nova citação"""
    print(f"\n{Cores.CIANO}{'='*60}{Cores.RESET}")
    print(f"{Cores.BOLD}{Cores.AZUL}INSERIR NOVA CITAÇÃO{Cores.RESET}")
    print(f"{Cores.CIANO}{'='*60}{Cores.RESET}\n")
    
    autor = input(f"{Cores.VERDE}Digite o autor: {Cores.RESET}").strip()
    frase = input(f"{Cores.VERDE}Digite a frase: {Cores.RESET}").strip()
    origem = input(f"{Cores.VERDE}Digite a origem (URL): {Cores.RESET}").strip()
    
    if not autor or not frase:
        print(f"{Cores.VERMELHO}Autor e frase são obrigatórios!{Cores.RESET}")
        return False
    
    nova_citacao = {
        'Autor': autor,
        'Frase': frase,
        'Origem': origem if origem else 'Manual'
    }
    
    citacoes.append(nova_citacao)
    print(f"{Cores.VERDE}Citação inserida com sucesso!{Cores.RESET}")
    return True

def alterar_citacao(citacoes: List[Dict]) -> bool:
    """Altera uma citação existente"""
    if not citacoes:
        print(f"{Cores.AMARELO}Nenhuma citação encontrada.{Cores.RESET}")
        return False
    
    try:
        idx = int(input(f"{Cores.CIANO}Digite o índice da citação a alterar (1-{len(citacoes)}): {Cores.RESET}"))
        if 1 <= idx <= len(citacoes):
            citacao = citacoes[idx - 1]
            
            print(f"\n{Cores.BOLD}{Cores.AZUL}{'='*60}{Cores.RESET}")
            print(f"{Cores.BOLD}CITAÇÃO ATUAL:{Cores.RESET}")
            print(f"  Autor: {citacao.get('Autor', 'N/A')}")
            print(f"  Frase: {citacao.get('Frase', 'N/A')}")
            print(f"  Origem: {citacao.get('Origem', 'N/A')}")
            print(f"{Cores.BOLD}{Cores.AZUL}{'='*60}{Cores.RESET}\n")
            
            print(f"{Cores.AMARELO}Deixe em branco para manter o valor atual.{Cores.RESET}\n")
            
            novo_autor = input(f"{Cores.VERDE}Novo autor [{citacao.get('Autor', '')}]: {Cores.RESET}").strip()
            nova_frase = input(f"{Cores.VERDE}Nova frase [{citacao.get('Frase', '')}]: {Cores.RESET}").strip()
            nova_origem = input(f"{Cores.VERDE}Nova origem [{citacao.get('Origem', '')}]: {Cores.RESET}").strip()
            
            if novo_autor:
                citacao['Autor'] = novo_autor
            if nova_frase:
                citacao['Frase'] = nova_frase
            if nova_origem:
                citacao['Origem'] = nova_origem
            
            print(f"{Cores.VERDE}Citação alterada com sucesso!{Cores.RESET}")
            return True
        else:
            print(f"{Cores.VERMELHO}Índice inválido!{Cores.RESET}")
            return False
    except ValueError:
        print(f"{Cores.VERMELHO}Por favor, digite um número válido.{Cores.RESET}")
        return False

def deletar_citacao(citacoes: List[Dict]) -> bool:
    """Deleta uma citação"""
    if not citacoes:
        print(f"{Cores.AMARELO}Nenhuma citação encontrada.{Cores.RESET}")
        return False
    
    try:
        idx = int(input(f"{Cores.CIANO}Digite o índice da citação a deletar (1-{len(citacoes)}): {Cores.RESET}"))
        if 1 <= idx <= len(citacoes):
            citacao = citacoes[idx - 1]
            
            print(f"\n{Cores.VERMELHO}CITAÇÃO A SER DELETADA:{Cores.RESET}")
            print(f"  Autor: {citacao.get('Autor', 'N/A')}")
            print(f"  Frase: {citacao.get('Frase', 'N/A')}")
            print(f"  Origem: {citacao.get('Origem', 'N/A')}\n")
            
            confirmacao = input(f"{Cores.VERMELHO}Tem certeza? (s/n): {Cores.RESET}").strip().lower()
            
            if confirmacao == 's':
                citacoes.pop(idx - 1)
                print(f"{Cores.VERDE}Citação deletada com sucesso!{Cores.RESET}")
                return True
            else:
                print(f"{Cores.AMARELO}Operação cancelada.{Cores.RESET}")
                return False
        else:
            print(f"{Cores.VERMELHO}Índice inválido!{Cores.RESET}")
            return False
    except ValueError:
        print(f"{Cores.VERMELHO}Por favor, digite um número válido.{Cores.RESET}")
        return False

def exibir_estatisticas(citacoes: List[Dict]):
    """Exibe estatísticas das citações"""
    if not citacoes:
        print(f"{Cores.AMARELO}Nenhuma citação encontrada.{Cores.RESET}")
        return
    
    total = len(citacoes)
    autores = {}
    
    for citacao in citacoes:
        autor = citacao.get('Autor', 'Desconhecido')
        autores[autor] = autores.get(autor, 0) + 1
    
    print(f"\n{Cores.BOLD}{Cores.AZUL}{'='*60}{Cores.RESET}")
    print(f"{Cores.BOLD}{Cores.AZUL}ESTATÍSTICAS{Cores.RESET}")
    print(f"{Cores.BOLD}{Cores.AZUL}{'='*60}{Cores.RESET}\n")
    print(f"{Cores.CIANO}Total de citações: {Cores.BOLD}{total}{Cores.RESET}")
    print(f"{Cores.CIANO}Total de autores únicos: {Cores.BOLD}{len(autores)}{Cores.RESET}\n")
    
    print(f"{Cores.BOLD}Top 5 autores:{Cores.RESET}")
    autores_ordenados = sorted(autores.items(), key=lambda x: x[1], reverse=True)[:5]
    for i, (autor, quantidade) in enumerate(autores_ordenados, 1):
        print(f"  {Cores.VERDE}{i}.{Cores.RESET} {autor}: {quantidade} citação(ões)")
    print(f"\n{Cores.BOLD}{Cores.AZUL}{'='*60}{Cores.RESET}\n")

def main():
    """Função principal"""
    pasta_dados = "dados_shelve"
    caminho_shelve = os.path.join(pasta_dados, "citacoes.db")
    
    # O shelve cria múltiplos arquivos (.dat, .dir, .bak), verificamos o .dat que é o principal
    caminho_dat = caminho_shelve + ".dat"
    if not os.path.exists(caminho_dat):
        print(f"{Cores.VERMELHO}Arquivo shelve não encontrado em {caminho_dat}{Cores.RESET}")
        print(f"{Cores.AMARELO}Execute primeiro o app_v2_shelve.py para criar os dados.{Cores.RESET}")
        return
    
    while True:
        limpar_tela()
        exibir_menu()
        
        citacoes = carregar_citacoes(caminho_shelve)
        opcao = input(f"{Cores.CIANO}Escolha uma opção: {Cores.RESET}").strip()
        
        if opcao == '0':
            print(f"\n{Cores.VERDE}Encerrando... Até logo!{Cores.RESET}\n")
            break
        elif opcao == '1':
            listar_citacoes(citacoes)
            input(f"\n{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")
        elif opcao == '2':
            buscar_citacao(citacoes)
            input(f"\n{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")
        elif opcao == '3':
            if inserir_citacao(citacoes):
                salvar_citacoes(caminho_shelve, citacoes)
            input(f"\n{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")
        elif opcao == '4':
            if alterar_citacao(citacoes):
                salvar_citacoes(caminho_shelve, citacoes)
            input(f"\n{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")
        elif opcao == '5':
            if deletar_citacao(citacoes):
                salvar_citacoes(caminho_shelve, citacoes)
            input(f"\n{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")
        elif opcao == '6':
            exibir_estatisticas(citacoes)
            input(f"\n{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")
        else:
            print(f"{Cores.VERMELHO}Opção inválida! Tente novamente.{Cores.RESET}")
            input(f"\n{Cores.CIANO}Pressione ENTER para continuar...{Cores.RESET}")

if __name__ == "__main__":
    main()

