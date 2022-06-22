# -*- coding: utf-8 -*-
"""EDA - Jugadores Premier League"""
#Librerías
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#cargamos un archivo CSV separado por comas
df = pd.read_csv('Data/EPL_20_21.csv', low_memory=False)
df

#leer 5 primeras lineas
df.head()

#leer 4 primeras lineas aleatorias
df.sample(4)

df.shape

#Información del DataFrame
df.info()

#Resumen de Datos estadisticos ---- Solo columnas numéricas
df.describe().T

#Número total de valores nulos
df.isna().sum()

df.columns

# Creacion de 2 columnas
df['mins_per_match'] = (df['Mins'] / df['Matches']).astype(int)    # minutos por partido

df['goals_per_match'] = (df['Goals'] / df['Matches']).astype(float)   # goles por partido

#visualizamos las nuevas columnas
df.head()

df.shape

#Total de goles ---- temporada EPL 2020-2021 ultima temporada
total_goals = df['Goals'].sum()
total_goals

#Goles x Penales ---- temporada EPL 2020-2021 ultima temporada
total_penalty_goals = df['Penalty_Goals'].sum()
total_penalty_goals

# Total Penales ---- temporada EPL 2020-2021 ultima temporada
total_penalty_attempts = df['Penalty_Attempted'].sum()
total_penalty_attempts

### Gráfico Pie chart **Penales Marcados** y **Penales Atajados**.

# Gráficos de penales
plt.figure(figsize=(13,6))
plt_not_scored = df['Penalty_Attempted'].sum() - total_penalty_goals
data = [plt_not_scored, total_penalty_goals]
nom = ['Penales Atajados', 'Penales Marcados']
colores = sns.color_palette('Set2')
plt.pie(data, labels = nom, colors = colores, autopct = '%.0f%%')
plt.show()

# Posiciones únicas de cada jugador 
# Portero (GK), defensor (DF), centrocampista (MF) delantero (FW)
df['Position'].unique()

# Filtrar jugadores delanteros (FW)
df_FW = df[df['Position'] == 'FW']

# Cantidad jugadores delanteros (FW)
df_FW['Name'].count()

#  Nacionalidad de los Jugadores
np.size(df['Nationality'].unique())

# Nacionalidad de la mayoría de los jugadores
nationality = df.groupby('Nationality').size().sort_values(ascending = False)

nationality.head(10).plot(kind = 'bar', figsize = (12,6), color = sns.color_palette('magma'))

plt.show()

# Los Club con maximo numero de jugadores en la temporada
df['Club'].value_counts().nlargest(5).plot(kind = 'bar', color = sns.color_palette('viridis'))

plt.show()

# Los Club con menor numero de jugadores en la temporada
df['Club'].value_counts().nsmallest(5).plot(kind = 'bar', color = sns.color_palette('viridis'))

plt.show()

### Edad de los jugadores

# Grupo de edades de los Jugadores
under_20 = df[df['Age'] <= 20] 
age20_25 = df[(df['Age'] > 20) & (df['Age'] <= 25)]
age20_30 = df[(df['Age'] > 20) & (df['Age'] <= 30)]
above_30 = df[df['Age'] > 30]

# Pie Chart de los grupos de jugadores por edad
x = np.array([under_20['Name'].count(),
    age20_25['Name'].count(),
    age20_30['Name'].count(),
    above_30['Name'].count()])

mylabels = ['<=20', '>20 & <=25', '>25 & <=30', '>30']

plt.figure(figsize = (13, 6))
plt.title('Total de Jugadores por grupo de Edad', fontsize = 20)
plt.pie(x, labels = mylabels, autopct = '%.1f%%')
plt.show()

# Total de jugadores menores de 20 años en cada club
players_under_20 = df[df['Age'] < 20]
players_under_20['Club'].value_counts().plot(kind = 'bar', color = sns.color_palette('cubehelix'))
plt.show()

# Jugadores menores de 20 años en  club Manchester United (7)
players_under_20[players_under_20['Club'] == 'Manchester United']

# Jugadores menores de 20 años en  club Chelsea (7)
players_under_20[players_under_20['Club'] == 'Chelsea']

# Gráfico BoxPlot de la edad promedio de los jugadores de cada club
plt.figure(figsize = (13,6))
sns.boxplot(x = 'Club', y = 'Age', data = df)
plt.xticks(rotation = 90)
plt.show()

# Clubs con Edades promedio mas altas
num_player = df.groupby('Club').size()
data = (df.groupby('Club')['Age'].sum()) / num_player

data.sort_values(ascending = False)

# Grafica de Total de asistencias gol por cada club
assists_by_club = pd.DataFrame(df.groupby('Club', as_index = False)['Assists'].sum())
sns.set(style = 'whitegrid', color_codes = True)
ax = sns.barplot(x = 'Club', y = 'Assists', data = assists_by_club.sort_values(by='Assists'), palette='Set2')
ax.set_xlabel('Club', fontsize = 30)
ax.set_ylabel('Assits', fontsize = 20)
plt.xticks(rotation = 75)

plt.rcParams['figure.figsize'] = (20,9)
plt.title('Gráfica de Club vs Total de Asistencias', fontsize=20)
plt.show()



# Jugadores top de 10 Asistencias Gol
top_10_assits = df[['Name','Club','Assists','Matches',]].nlargest(n=10, columns = 'Assists')
top_10_assits

# Grafica del total de goles de cada club
goals_by_clubs = pd.DataFrame(df.groupby('Club', as_index=False)['Goals'].sum())
sns.set(style='whitegrid',color_codes=True)
ax = sns.barplot(x='Club', y='Goals', data=goals_by_clubs.sort_values(by='Goals'),palette='rocket')
ax.set_xlabel('Club', fontsize=30)
ax.set_ylabel('Goals', fontsize=20)
plt.rcParams['figure.figsize'] = (20,0)
plt.title('Gráfica de Club vs Total de Goles', fontsize=20)
plt.show()


#Top 10 de  Goles por Jugador
top_10_goals = df[['Name','Club','Goals','Matches',]].nlargest(n=10, columns = 'Goals')
top_10_goals

df.columns

df.head()

# Top 10 Goles por partido
top_10_goals_per_match = df[['Name','Club','Goals','Matches',]].nlargest(n=10, columns = 'Goals')
top_10_goals_per_match

# Grafica Pi Chart - Goles con asistencia y Goles sin asistencia
plt.figure(figsize = (14,7))
assists = df['Assists'].sum()
data = [total_goals - assists, assists]
nom = ['Goles sin Asistencia', 'Goles con Asistencia']
colores = sns.color_palette('Set1')
plt.pie(data, labels = nom, colors = colores, autopct = '%.0f%%')
plt.show()

df.columns

#Top 10 jugadores con más tarjetas amarillas
yellow_cards = df.sort_values(by='Yellow_Cards', ascending=False)[:10]
plt.figure(figsize=(20,6))
plt.title('Top 10 jugadores con más tarjetas amarillas', fontsize=20)
c = sns.barplot(x = yellow_cards['Name'], y = yellow_cards['Yellow_Cards'],
               label = 'players', color = 'yellow')
plt.ylabel('Número de Tarjetas Amarillas')      
c.set_xticklabels(c.get_xticklabels(), rotation = 45) 
c
plt.show()
