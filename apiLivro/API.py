import requests
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem


class ResultadosWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        pass

    def _buscaDescricao(self, work_id):
        #Busca a descrição completa da obra
        if not work_id:
            return "Chave de obra (Key) não disponível para busca de descrição."
            
        url = f"https://openlibrary.org/works/{work_id}.json"

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            dados = response.json()
            
            description_data = dados.get("description")
            
            if isinstance(description_data, str):
                return description_data.replace('\n', ' ').strip()
            elif isinstance(description_data, dict) and 'value' in description_data:
                return description_data['value'].replace('\n', ' ').strip()
            else:
                return "Descrição não encontrada para esta obra."

        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar a descrição (falha de conexão ou API): {e}")
            return "Erro ao buscar a descrição."
            

    def exibir_resultados(self, livros):
        #Imprime a lista de livros e suas descrições no terminal.
        print("\n" + "=" * 80)
        print("RESULTADOS DA BUSCA - EXIBIÇÃO NO TERMINAL")
        print("=" * 80)
        
        if not livros:
            print("Nenhum livro encontrado.")
            print("=" * 80)
            return

        print(f"Total de {len(livros)} livros encontrados.")
        print("-" * 80)

        print(f"{'#':<3}{'Título':<40}{'Autor':<25}{'Ano':<6}{'ISBN':<15}")
        print("-" * 80)

        for i, livro in enumerate(livros):
            titulo = livro.get("Titulo", "N/A")
            autor = livro.get("Autor", "N/A")
            ano = str(livro.get("Ano", "N/A"))
            isbn = livro.get("ISBN", "N/A")
            work_id = livro.get("Key", "")
            
            print(f"{i+1:<3}{titulo[:37] + '...' if len(titulo) > 40 else titulo:<40}{autor[:22] + '...' if len(autor) > 25 else autor:<25}{ano:<6}{isbn:<15}")
            
            descricao = self._buscaDescricao(work_id)
            if "Descrição não encontrada" not in descricao and "Erro ao buscar a descrição" not in descricao and descricao.strip():
                print(f"  > Descrição: {descricao[:150]}...") 
            else:
                print(f"  > Descrição: {descricao}")
            print("-" * 80)
        
        print("\nBusca concluída.")


class BuscaLivrosWindow(QtWidgets.QMainWindow):
    #Gerencia a janela principal de busca (para input) e coordena a execução da busca.
    def __init__(self, busca_ui_file):
        super().__init__()
        uic.loadUi(busca_ui_file, self)

        self.tela_resultados = ResultadosWindow()

        self.findChild(QtWidgets.QPushButton, 'btn_BuscarLivro').clicked.connect(self.executar_busca)

    def executar_busca(self):
        """Coleta os campos de busca, valida e chama a API. A saída é direcionada ao terminal."""
        Autor = self.findChild(QtWidgets.QLineEdit, 'line_autor').text().strip()
        if self.findChild(QtWidgets.QLineEdit, 'line_Titulo'):
            self.findChild(QtWidgets.QLineEdit, 'line_Titulo').setText("")
        
        Genero = self.findChild(QtWidgets.QLineEdit, 'line_Genero').text().strip()

        if Genero == "" and Autor == "":
            print("\n" + "-" * 50)
            print("ERRO: Preencha ao menos um dos campos (Gênero ou Autor) para buscar.")
            print("-" * 50)
            return

        print(f"\nIniciando busca por: Gênero='{Genero}', Autor='{Autor}'...")
        lista_livros = self._buscaLivro(Genero, Autor)

        if lista_livros:
            self.tela_resultados.exibir_resultados(lista_livros)
        else:
            print("\n[Busca] Nenhum resultado encontrado ou erro na API.")

    def _buscaLivro(self, Genero, Autor):
        #Implementação da chamada à API Open Library
        url = "https://openlibrary.org/search.json"
        
        params = {
            "author": Autor,
            "subject": Genero,
            "limit": 10
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            dados = response.json()

            livros_encontrados = []

            if dados.get("numFound", 0) > 0:
                for doc in dados.get("docs", [])[:10]:
                    key_full = doc.get("key", "")
                    
                    livro = {
                        "Titulo": doc.get("title", "N/A"),
                        "Autor": doc.get("author_name", ["N/A"])[0], 
                        "Ano": doc.get("first_publish_year", "N/A"), 
                        "ISBN": doc.get("isbn", ["N/A"])[0],
                        "Key": key_full.split('/')[-1] if key_full else ""
                    }
                    livros_encontrados.append(livro)
                
                return livros_encontrados 

            return []

        except requests.exceptions.Timeout:
            print("\n[Erro de Conexão] A busca excedeu o tempo limite de 10 segundos. Tente novamente.")
            return []
        
        except requests.exceptions.RequestException as erro:
            print(f"\n[Erro de API] Erro ao acessar a API: {erro}")
            return [] 


def main():
    # NOTA: É NECESSÁRIO ter o arquivo de interface gráfica (UI) "Tela_BuscaLivro.ui"
    # criado com o Qt Designer para que o código de busca funcione.
    BUSCA_UI = "Tela_BuscaLivro.ui"
    
    app = QtWidgets.QApplication(sys.argv)
    
    try:
        janela_busca = BuscaLivrosWindow(BUSCA_UI)
        janela_busca.show()
    except Exception as e:
        print(f"Erro ao carregar a interface: Certifique-se de que o arquivo '{BUSCA_UI}' existe e está correto.")
        print(f"Detalhes do erro: {e}")
        return

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()