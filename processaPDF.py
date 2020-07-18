# Para processar arquivos PDF
from PyPDF2 import PdfFileReader
import scraping as sc
import requests
import io
import pandas as pd
def processaPDF():
    pdfurls = sc.scrapingCovid()

    # Listas para os resultados da extração dos dados
    total_casos_confirmados = []
    total_novos_casos_confirmados = []
    total_mortes_confirmadas = []
    total_novas_mortes_confirmadas = []
    pais = 'Portugal'
    # Loop pela lista de arquivos em pdf
    for pdfurl in pdfurls:
        
        # Obtém o arquivo
        requisicao = requests.get(pdfurl)
        if requisicao.status_code == 200:
            # Grava o conteúdo em formato que permite a leitura
            arquivo = io.BytesIO(requisicao.content)
            
            # Leitura do conteúdo
            arquivo_final = PdfFileReader(arquivo)
            
            # Loop por todas as páginas do arquivo
            for page in range(arquivo_final.getNumPages()):
                try:
                    
                    # Extrai o texto
                    pagina_conteudo = arquivo_final.getPage(page).extractText().split('\n')
                    
                    # Índice de busca
                    pagina_indice = (pagina_conteudo.index(pais))

                    # Grava o resultado nas listas
                    total_casos_confirmados.append(pagina_conteudo[pagina_indice + 2])
                    total_novos_casos_confirmados.append(pagina_conteudo[pagina_indice + 4])
                    total_mortes_confirmadas.append(pagina_conteudo[pagina_indice + 6])
                    total_novas_mortes_confirmadas.append(pagina_conteudo[pagina_indice + 8])
                
                except:
                    pass

    # Vamos criar um dataframe com as listas 
    df_covid = pd.DataFrame(data = [total_casos_confirmados,
                                    total_novos_casos_confirmados,
                                    total_mortes_confirmadas,
                                    total_novas_mortes_confirmadas]).transpose()

    # Visualiza os dados
    print(df_covid.head())

    # Ajustamos o nome das colunas
    df_covid.columns = ['Total_Casos_Confirmados', 
                        'Total_Novos_Casos_Confirmados', 
                        'Total_Mortes_Confirmadas', 
                        'Total_Novas_Mortes_Confirmadas']

    # Visualiza os dados
    print(df_covid.head(10))


    # A primeira linha parace ter dados incompletos (provavelmente o relatório mais recente ainda não foi atualizado)
    # Vamos remover a primeira linha do dataset
    df_covid.drop(df_covid.head(1).index, inplace = True)
    df_covid.to_csv('covid19.csv', index=False, sep=';')

