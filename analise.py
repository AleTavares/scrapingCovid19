import processaPDF as prss
import os.path as op
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.optimize import fsolve
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error

if not op.exists('covid19.csv'):
    prss.processaPDF()

df_covid = pd.read_csv('covid19.csv', sep=";")

print(df_covid)

pais = 'Portugal'

# Dados para o plot
df_plot_data = df_covid.loc[0:len(df_covid.index)]

# Remove espaços do dataset
df_plot_data = df_plot_data.replace(r'^\s*$', 0, regex = True)

# Transforma campos em inteiro
df_plot_data = df_plot_data.astype(int)

# Ordena os dados e reindexa o dataframe
df_plot_data = df_plot_data.sort_index(ascending = False).reset_index()

# DataSet Final
df_plot_data = df_plot_data.iloc[:,1:]

# Primeiro Gráfico

# Define a área de plotagem
fig, ax = plt.subplots(figsize = (15, 7.5))

# Título e labels
plt.title('\nContaminações do COVID-19 no País: < ' + pais + ' > - Fonte de Dados: OMS\n', size = 16)
plt.xlabel('\nDias Desde a Primeira Contaminação\n', size = 14)
plt.ylabel('\nNúmero Total de Contaminações\n', size = 14)

# Dados para o plot
x = df_plot_data.index
y = df_plot_data['Total_Casos_Confirmados']

# Scatter plot
plt.scatter(x, y, color = 'blue')

# Linha de tendência com np.polyfit() e np.poly1d()
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
plt.plot(x, p(x), "r--")
plt.show()


# Segundo Gráfico

# Define a área de plotagem
fig, ax = plt.subplots(figsize = (15, 7.5))

# Título e labels
plt.title('\nMortes de COVID-19 no País: < ' + pais + ' > - Fonte de Dados: OMS\n', size = 16)
plt.xlabel('\nDias Desde a Primeira Contaminação\n', size = 14)
plt.ylabel('\nNúmero Total de Mortes\n', size = 14)

# Dados para o plot
x = df_plot_data.index
y = df_plot_data['Total_Mortes_Confirmadas']

# Scatter plot
plt.scatter(x, y, color = 'blue')

# Trendline com np.polyfit
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
plt.plot(x, p(x), "r--")
plt.show()


# Modelagem Preditiva
#  Separamos os dados em x e y

# Para x usaremos o dia 61 como ponto de partida até o comprimento do dataset, que representa o dia mais atual em que
# os dados foram coletados.
x = list(range(61, 61 + len(df_plot_data)))

# Para y criaremos uma lista de total de casos confirmados
y = list(df_plot_data['Total_Casos_Confirmados'])

# Criamos o modelo logístico
# x = dados de entrada
# a = velocidade de crescimento
# b = pico de x
# L = valor máximo de y
def modelo_logistico(x, a, b, L):
    return L / (1 + np.exp(-(x - b) / a))

# Ajuste da curva do modelo logístico
modelo_covid = curve_fit(modelo_logistico, x, y, p0 = [2, 100, 20000])

# Extrai do modelo os valores de interesse: velocidade, pico de x e valor máximo de y
velocidade, pico_x, max_y = modelo_covid[0]

# Agora podemos calcular os erros
velocidade_erro, pico_x_erro, max_y_erro = [np.sqrt(modelo_covid[1][i][i]) for i in [0, 1, 2]]

# Agora resolver a equação não linear com a função fsolve()
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.fsolve.html
resultado = int(fsolve(lambda x: modelo_logistico(x, velocidade, pico_x, max_y) - max_y * 0.9999, pico_x))

# Geramos os valores finais para o gráfico com as previsões
x, _, velocidade, pico_x, max_y, _, _, resultado, _ = x, y, velocidade, pico_x, max_y, pico_x_erro, max_y_erro, resultado, df_plot_data.shape[0]

# Range de x
x_range = list(range(min(x), resultado))

# Plot das Previsões

# Define a área de plotagem
fig, ax = plt.subplots(figsize = (16, 8))

# Título e labels
plt.title('\nCurva Logística Para o Número de Contaminações de COVID-19 no País: < ' + pais + ' >\n', size = 16)
plt.xlabel('\nDias Desde a Primeira Contaminação\n', size = 14)
plt.ylabel('\nNúmero Contaminações\n', size = 14)

plt.plot(x_range, [modelo_logistico(i, velocidade, pico_x, max_y) for i in x_range], color = 'green')
plt.scatter(x, y, color = 'red')
plt.legend(['Previsto', 'Atual'])
plt.show()