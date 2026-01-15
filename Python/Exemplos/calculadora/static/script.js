class Calculator {
    constructor() {
        this.expression = '0';
        this.result = '0';
        this.shouldReset = false;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadTheme();
        this.updateDisplay();
    }

    setupEventListeners() {
        // Botões numéricos e operadores
        document.querySelectorAll('.btn[data-value]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.handleInput(e.target.dataset.value);
            });
        });

        // Botões de ação
        document.querySelectorAll('.btn[data-action]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.handleAction(e.target.dataset.action);
            });
        });

        // Teclado
        document.addEventListener('keydown', (e) => {
            this.handleKeyboard(e);
        });

        // Toggle de tema
        document.getElementById('themeToggle').addEventListener('click', () => {
            this.toggleTheme();
        });
    }

    handleInput(value) {
        if (this.shouldReset) {
            this.expression = '0';
            this.shouldReset = false;
        }

        // Converter símbolos para operadores matemáticos
        const operators = {
            '×': '*',
            '÷': '/',
            '−': '-',
            '+': '+'
        };

        if (value in operators) {
            value = operators[value];
        }

        // Tratamento especial para raiz quadrada
        if (value === '√') {
            if (this.expression === '0') {
                this.expression = 'sqrt(';
            } else {
                this.expression += 'sqrt(';
            }
            this.updateDisplay();
            return;
        }
        
        // Tratamento especial para mudança de sinal
        if (value === '±') {
            if (this.expression === '0') {
                this.expression = '-';
            } else if (this.expression.startsWith('-')) {
                this.expression = this.expression.substring(1);
            } else {
                this.expression = '-' + this.expression;
            }
            this.updateDisplay();
            this.calculateResult();
            return;
        }

        // Tratamento especial para π e e
        if (value === 'π' || value === 'e') {
            if (this.expression === '0') {
                this.expression = value;
            } else {
                this.expression += value;
            }
            this.updateDisplay();
            return;
        }

        // Tratamento para números
        if (this.expression === '0' && value !== '.') {
            this.expression = value;
        } else {
            this.expression += value;
        }

        this.updateDisplay();
        this.calculateResult();
    }

    handleAction(action) {
        switch (action) {
            case 'clear':
                this.expression = '0';
                this.result = '0';
                this.updateDisplay();
                break;
            case 'clear-entry':
                this.expression = '0';
                this.updateDisplay();
                break;
            case 'backspace':
                if (this.expression.length > 1) {
                    this.expression = this.expression.slice(0, -1);
                } else {
                    this.expression = '0';
                }
                this.updateDisplay();
                this.calculateResult();
                break;
            case 'equals':
                this.evaluate();
                break;
        }
    }

    handleKeyboard(e) {
        e.preventDefault();
        
        const keyMap = {
            '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
            '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
            '+': '+', '-': '-', '*': '*', '/': '/',
            '.': '.', '(': '(', ')': ')',
            'Enter': 'equals',
            'Escape': 'clear',
            'Backspace': 'backspace',
            'Delete': 'clear-entry'
        };

        if (keyMap[e.key]) {
            if (keyMap[e.key] === 'equals') {
                this.handleAction('equals');
            } else if (keyMap[e.key] === 'clear' || keyMap[e.key] === 'clear-entry' || keyMap[e.key] === 'backspace') {
                this.handleAction(keyMap[e.key]);
            } else {
                this.handleInput(keyMap[e.key]);
            }
        }
    }

    calculateResult() {
        try {
            let expr = this.expression;
            
            // Substituir símbolos matemáticos
            expr = expr.replace(/×/g, '*').replace(/÷/g, '/').replace(/−/g, '-');
            
            // Substituir constantes
            expr = expr.replace(/π/g, Math.PI.toString()).replace(/e/g, Math.E.toString());
            
            // Substituir sqrt
            expr = expr.replace(/sqrt\(/g, 'Math.sqrt(');
            
            // Adicionar Math. para funções matemáticas se necessário
            if (expr.includes('sqrt(') && !expr.includes('Math.sqrt(')) {
                expr = expr.replace(/sqrt\(/g, 'Math.sqrt(');
            }
            
            // Validar expressão
            if (this.isValidExpression(expr)) {
                const result = Function('"use strict"; return (' + expr + ')')();
                this.result = this.formatResult(result);
            } else {
                this.result = '0';
            }
        } catch (error) {
            this.result = '0';
        }
        
        this.updateDisplay();
    }

    isValidExpression(expr) {
        // Verificação básica de segurança
        const dangerous = ['eval', 'Function', 'constructor', 'prototype'];
        return !dangerous.some(d => expr.includes(d));
    }

    async evaluate() {
        try {
            let expr = this.expression;
            
            // Substituir símbolos matemáticos
            expr = expr.replace(/×/g, '*').replace(/÷/g, '/').replace(/−/g, '-');
            
            // Substituir sqrt
            expr = expr.replace(/sqrt\(/g, 'math.sqrt(');
            
            // Enviar para o servidor
            const response = await fetch('/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ expression: expr })
            });

            const data = await response.json();
            
            if (data.error) {
                this.result = 'Erro';
                this.expression = '0';
            } else {
                this.result = this.formatResult(data.result);
                this.expression = this.result;
                this.shouldReset = true;
            }
        } catch (error) {
            this.result = 'Erro';
            this.expression = '0';
        }
        
        this.updateDisplay();
    }

    formatResult(num) {
        if (typeof num !== 'number' || !isFinite(num)) {
            return 'Erro';
        }
        
        // Formatar números muito grandes ou muito pequenos
        if (Math.abs(num) > 1e10 || (Math.abs(num) < 1e-4 && num !== 0)) {
            return num.toExponential(6);
        }
        
        // Limitar casas decimais
        const rounded = Math.round(num * 1e10) / 1e10;
        return rounded.toString();
    }

    updateDisplay() {
        const expressionEl = document.getElementById('expression');
        const resultEl = document.getElementById('result');
        
        expressionEl.textContent = this.expression;
        resultEl.textContent = this.result;
        
        // Adicionar efeito de digitação
        resultEl.classList.add('typing');
        setTimeout(() => {
            resultEl.classList.remove('typing');
        }, 300);
    }

    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        // Atualizar ícone
        const icon = document.querySelector('.theme-icon');
        icon.textContent = newTheme === 'light' ? '🌙' : '☀️';
    }

    loadTheme() {
        const savedTheme = localStorage.getItem('theme') || 'dark';
        document.documentElement.setAttribute('data-theme', savedTheme);
        
        const icon = document.querySelector('.theme-icon');
        icon.textContent = savedTheme === 'light' ? '🌙' : '☀️';
    }
}

// Inicializar calculadora quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    new Calculator();
});

