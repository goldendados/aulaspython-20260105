import psycopg2
import os
from psycopg2 import pool

# String de conexão do banco de dados
DATABASE_URL = 'postgresql://neondb_owner:npg_Zu4H7SibcdCU@ep-orange-cake-ac1unhy1-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

# Pool de conexões (opcional, mas recomendado para produção)
connection_pool = None

def get_connection():
    """Obtém uma conexão com o banco de dados"""
    return psycopg2.connect(DATABASE_URL)

def init_db():
    """Inicializa o banco de dados criando a tabela se não existir"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Cria a tabela de tarefas se não existir
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tarefas (
                    id SERIAL PRIMARY KEY,
                    texto VARCHAR(500) NOT NULL,
                    concluida BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print("Tabela de tarefas criada/verificada com sucesso!")
    except Exception as e:
        print(f"Erro ao inicializar banco de dados: {e}")
        conn.rollback()
    finally:
        conn.close()

def get_all_tarefas():
    """Retorna todas as tarefas do banco de dados"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, texto, concluida FROM tarefas ORDER BY id DESC")
            tarefas = []
            for row in cur.fetchall():
                tarefas.append({
                    'id': row[0],
                    'texto': row[1],
                    'concluida': row[2]
                })
            return tarefas
    except Exception as e:
        print(f"Erro ao buscar tarefas: {e}")
        return []
    finally:
        conn.close()

def add_tarefa(texto):
    """Adiciona uma nova tarefa ao banco de dados"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO tarefas (texto, concluida) VALUES (%s, %s) RETURNING id",
                (texto, False)
            )
            tarefa_id = cur.fetchone()[0]
            conn.commit()
            return tarefa_id
    except Exception as e:
        print(f"Erro ao adicionar tarefa: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def toggle_tarefa(tarefa_id):
    """Alterna o status de conclusão de uma tarefa"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Primeiro, busca o status atual
            cur.execute("SELECT concluida FROM tarefas WHERE id = %s", (tarefa_id,))
            result = cur.fetchone()
            if result:
                novo_status = not result[0]
                cur.execute(
                    "UPDATE tarefas SET concluida = %s WHERE id = %s",
                    (novo_status, tarefa_id)
                )
                conn.commit()
                return True
            return False
    except Exception as e:
        print(f"Erro ao atualizar tarefa: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def delete_tarefa(tarefa_id):
    """Exclui uma tarefa do banco de dados"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tarefas WHERE id = %s", (tarefa_id,))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        print(f"Erro ao excluir tarefa: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

