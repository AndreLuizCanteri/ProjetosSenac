from conection import ConnectionFactory
class UsuarioDAO:
    def cadastrar(self, nome, email, senha):
        sql = """
            INSERT INTO usuarios (nome, email, senha)
            VALUES (?, ?, ?)
        """
        try: 
            conn = ConnectionFactory.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (nome, email, senha))
            cursor.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao cadastrar usuario: {e}")
            return False
    
    def autenticar(self, email, senha):
        sql = """
            SELECT * FROM usuarios
            WHERE email = ? AND senha = ?
            """
        try:
            conn = ConnectionFactory.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql,(email, senha))
            resultado = cursor.fetchone()
            cursor.close()
            conn.close()
            return resultado is not None
        except Exception as e:
            print(f"Erro ao autenticar:{e}")

    def consultar_todos(self):
        sql = "SELECT id, nome, email FROM usuarios"
        try:
            conn = ConnectionFactory.get_connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            usuarios = cursor.fetchall()
            cursor.close()
            conn.close()
            return usuarios #retorna a lista de usuarios
        except Exception as e:
            print(f"Erro ao consultar usuario: {e}")
            return []
    
    def remover(self, email):
        sql_verifica = "SELECT id FROM usuarios WHERE email = ?"
        sql_delete = "DELETE FROM usuarios WHERE email = ?"
        try:
            conn = ConnectionFactory.get_connection()
            cursor = conn.cursor()
            #Verifica se existe o usuario
            cursor.execute(sql_verifica, (email))
            usuario = cursor.fetchone()
            if usuario is None:
                # Não existe = nada sera removido
                cursor.close()
                conn.close()
                return False
            
            #Remova usuario
            cursor.execute(sql_delete, (email))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao remover usuario: {e}")
            return False