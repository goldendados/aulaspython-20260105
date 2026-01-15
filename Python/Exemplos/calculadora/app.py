from flask import Flask, render_template, request, jsonify
import math
import re

app = Flask(__name__)

def safe_eval(expression):
    """Avalia expressão matemática de forma segura"""
    # Substituir constantes
    expression = expression.replace('π', str(math.pi))
    expression = expression.replace('e', str(math.e))
    
    # Substituir sqrt
    expression = re.sub(r'Math\.sqrt\(', 'math.sqrt(', expression)
    expression = re.sub(r'sqrt\(', 'math.sqrt(', expression)
    
    # Remover espaços
    expression = expression.replace(' ', '')
    
    # Verificação de segurança: não permitir sequências perigosas
    dangerous_patterns = ['__', 'import', 'exec', 'eval', 'open', 'file', 'input', 'raw_input', 
                         'compile', 'reload', 'getattr', 'setattr', 'delattr', 'hasattr']
    expression_lower = expression.lower()
    for pattern in dangerous_patterns:
        if pattern in expression_lower:
            raise ValueError("Expressão contém caracteres inválidos")
    
    # Verificar se contém apenas caracteres seguros após substituições
    # Permitir: números, operadores matemáticos, math., parênteses, ponto
    safe_chars = set('0123456789+-*/.()mathsqrte')
    if not all(c in safe_chars for c in expression):
        raise ValueError("Expressão contém caracteres inválidos")
    
    # Criar namespace seguro apenas com math
    safe_dict = {
        "__builtins__": {},
        "math": math,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,
        "exp": math.exp,
        "pow": math.pow,
    }
    
    try:
        result = eval(expression, safe_dict)
        return float(result)
    except:
        raise ValueError("Erro ao calcular expressão")

@app.route('/')
def index():
    """Rota principal que renderiza a calculadora"""
    return render_template('calculator.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """Rota para processar cálculos no servidor"""
    try:
        data = request.get_json()
        expression = data.get('expression', '')
        
        if not expression or expression.strip() == '':
            return jsonify({'error': 'Expressão vazia'}), 400
        
        # Processar e calcular
        result = safe_eval(expression)
        
        return jsonify({'result': result})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Erro ao processar cálculo'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

