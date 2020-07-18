# Imports
import bs4
import requests
from bs4 import BeautifulSoup

# URL Base
url_base = 'https://www.who.int'
def scrapingCovid():
    # URL com os dados do COVID-19 (coloque essa URL no seu navegador e compreenda os dados disponíveis)
    url = 'https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports/'

    # Obtém os dados da URL
    response = requests.get(url)

    # Leitura do conteúdo
    soup = BeautifulSoup(response.content, 'lxml')

    # Lista temporária
    tempList = []

    # Loop pelos elementos da página para buscar as tags "a" que indicam URLs
    # Estamos buscando os links dos relatórios chamados 'situation-reports'
    for element in soup.find_all('a', href = True):
        if 'situation-reports' in str(element):
            tempList.append(str(element))


    # Visualiza alguns registros da lista
    # print(tempList[1:5])

    # Lista para as URLs dos arquivos em pdf
    pdfurls = []

    # Variável que indica se é o último relatório
    lastreport = None

    # Loop para limpar cada registro da lista temporária, extraindo somente a URL dos arquivos em pdf
    for url in tempList:
        
        # Replace da tag de link html
        x = url.replace('<a href="', '')
        
        # Busca pelo sinal de interrogação para usar como índice de final do endereço de cada arquivo pdf
        index = x.find('?')
        
        # Extrai tudo de 0 até o índice
        extraction = x[0:index]
        
        # Nas posições de 68:70 do endereço do arquivo pdf estão os dígitos do número do relatório
        reportnumber = extraction[68:70]
        
        # Verifica se o relatório é o último
        # Se não for, adicionamos a url_base ao nome do arquivo e gravamos na lista de URLs
        if reportnumber != lastreport:
            pdfurls.append(url_base + extraction)
            
        # Atualiza a variável com o número do último relatório (posições de 68:70)
        lastreport = extraction[68:70]

    # Total de arquivos pdf
    print(len(pdfurls))

    # Visualiza amostra da lista de URLs dos arquivos pdf
    return pdfurls

