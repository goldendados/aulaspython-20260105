from flask import Flask, render_template, request, redirect, url_for
from database import init_db, get_all_tarefas, add_tarefa, toggle_tarefa, delete_tarefa

app = Flask(__name__)

# Inicializa o banco de dados quando a aplicação inicia
init_db()

@app.route('/')
def index():
    """Página inicial que lista todas as tarefas"""
    tarefas = get_all_tarefas()
    return render_template('index.html', tarefas=tarefas)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    """Adiciona uma nova tarefa"""
    try:
        texto = request.form.get('texto', '').strip()
        
        if texto:
            add_tarefa(texto)
    except Exception as e:
        print(f"Erro ao adicionar tarefa: {e}")
    
    return redirect(url_for('index'))

@app.route('/concluir/<int:tarefa_id>', methods=['POST'])
def concluir(tarefa_id):
    """Marca uma tarefa como concluída ou não concluída"""
    try:
        toggle_tarefa(tarefa_id)
    except Exception as e:
        print(f"Erro ao atualizar tarefa: {e}")
    
    return redirect(url_for('index'))

@app.route('/excluir/<int:tarefa_id>', methods=['POST'])
def excluir(tarefa_id):
    """Exclui uma tarefa"""
    try:
        delete_tarefa(tarefa_id)
    except Exception as e:
        print(f"Erro ao excluir tarefa: {e}")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
