## Definição do Problema

Desde Janeiro/2020 a OMS (Organização Mundial da Saúde) vem emitindo boletins diários sobre as contaminações e mortes causadas pelo COVID-19. Esses boletins são divulgados em relatórios no formato pdf com tabelas mostrando os números por país e o total por continente.

Neste Lab faremos Web Scraping para extrair as URLs de cada relatório em pdf e então faremos PDF Scraping para extrair os dados de cada relatório.

Com os dados em mãos, vamos fazer uma rápida exploração e construir alguns gráficos mostrando a linha de tendência através de equação polinomial.

Depois disso, usaremos os dados para ajustar um modelo matemático de previsão da curva de contaminação, trabalhando com mínimos quadrados não lineares.

Nosso objetivo aqui NÃO é fazer um estudo sobre COVID-19, mas sim fornecer um exemplo de como extrair dados de arquivos pdf e ajustar um modelo matemático.

Modelos tradicionais de Machine Learning não fazem um bom trabalho com dados do COVID-19 e não deveriam ser usados. 

O modelo usado aqui é estudado em detalhes no curso <a href="https://www.datascienceacademy.com.br/course?courseid=analise-estatistica-para-data-science-ii">Análise Estatística Para Data Science II</a> e os conceitos de equações não lineares são estudados em <a href="https://www.datascienceacademy.com.br/course?courseid=matematica-para-machine-learning">Matemática Para Machine Learning</a>.

Leia todos os comentários, execute as células e gere o modelo para diferentes países. No momento da geração deste Lab os dados do Brasil apresentavam problemas, o que iria requerer limpeza adicional (e que não foi feito). Deixamos isso com você, se desejar. Mas os dados do Brasil não estão consistentes e não recomendamos o uso.


## Fonte de Dados

Nossa fonte de dados será o site oficial da OMS: https://www.who.int

## Bibliotecas
*Scraping*
- pip install io
- pip install bs4
- pip install requests
- pip install matplotlib
- pip install numpy
- pip install pandas
- pip install matplotlib
- pip install bs4
- pip install datetime

*Processar arquivos PDF*
- pip install PyPDF2

*Modelo matemático*
- pip install scipy
- pip install sklearn