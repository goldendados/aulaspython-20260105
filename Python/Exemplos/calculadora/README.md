# Calculadora Moderna com Flask

Uma calculadora web moderna e elegante desenvolvida com Flask (Python), aplicando conceitos avançados de UX/UI.

## 🎨 Características

- **Interface Moderna**: Design limpo e elegante com tema claro/escuro
- **Responsiva**: Funciona perfeitamente em desktop e mobile
- **Animações Suaves**: Transições e efeitos visuais agradáveis
- **Feedback Visual**: Indicadores visuais para todas as interações
- **Suporte a Teclado**: Use seu teclado para realizar cálculos
- **Operações Avançadas**: Suporte para raiz quadrada, constantes (π, e) e parênteses

## 🚀 Como Usar

### Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Execução

2. Execute a aplicação:
```bash
python app.py
```

3. Acesse no navegador:
```
http://localhost:5000
```

## ⌨️ Atalhos de Teclado

- **Números**: 0-9
- **Operadores**: +, -, *, /
- **Enter**: Calcular (=)
- **Escape**: Limpar tudo (C)
- **Backspace**: Apagar último caractere
- **Delete**: Limpar entrada atual (CE)

## 🎯 Funcionalidades

### Operações Básicas
- Adição (+)
- Subtração (-)
- Multiplicação (×)
- Divisão (÷)

### Operações Avançadas
- Raiz quadrada (√)
- Parênteses para agrupamento
- Constantes matemáticas (π, e)
- Mudança de sinal (±)

### Interface
- Tema claro/escuro (toggle no canto superior direito)
- Display duplo (expressão e resultado)
- Animações e feedback visual
- Design responsivo

## 🛠️ Tecnologias

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Fontes**: Google Fonts (Inter)
- **Estilização**: CSS Custom Properties (variáveis CSS)

## 📁 Estrutura do Projeto

```
.
├── app.py                 # Aplicação Flask principal
├── requirements.txt       # Dependências Python
├── templates/
│   └── calculator.html    # Template HTML
└── static/
    ├── style.css         # Estilos CSS
    └── script.js         # Lógica JavaScript
```

## 🎨 Conceitos de UX/UI Aplicados

1. **Hierarquia Visual**: Tamanhos de fonte e cores diferenciadas
2. **Feedback Imediato**: Animações e estados hover/active
3. **Consistência**: Padrões visuais uniformes
4. **Acessibilidade**: Suporte a teclado e contraste adequado
5. **Responsividade**: Adaptação a diferentes tamanhos de tela
6. **Microinterações**: Efeitos sutis que melhoram a experiência
7. **Tema Adaptável**: Suporte a modo claro/escuro

## 🔒 Segurança

A aplicação implementa validação de segurança para prevenir execução de código malicioso:
- Validação de caracteres permitidos
- Namespace restrito para avaliação de expressões
- Sanitização de entrada

## 📝 Licença

Este projeto é de código aberto e está disponível para uso livre.

