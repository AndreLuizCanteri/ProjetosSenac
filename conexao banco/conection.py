import pyodbc
class ConnectionFactory:
    @staticmethod
    def get_connection():
        connection_string = (
            "Driver={SQL Server};" 
            "Server=localhost;" 
            "Database=loginBanco;"
            "Trusted_Connection=yes;"
            "Encrypt=no;"
        )
        try:
            conn = pyodbc.connect(connection_string)
            return conn
        except Exception as e:
            raise RuntimeError(f"Erro na conexão: {e}")