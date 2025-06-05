import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import file_to_json

#Se define el repositorio a buscar y el directorio del archivo
repo = "smogon/pokemon-showdown"
file_path = "data/pokedex.ts"

#Trae la información del archivo de GitHub a una variable
#Modifica la información recabada para pasarla a formato json
tipos_json = file_to_json.convert(repo,file_path) #Accede al archivo file_to_json.py para más información

#Se lee el archivo csv de smogon
smogon = pd.read_csv("smogon.csv")

#Se cargan los nombres de los Pokemon
pkm_nombres = smogon[["Pokemon"]]["Pokemon"]

#Se lee el archivo del TF-IDF realizado a la columna moves
data = pd.read_csv("smogon_agrupado_1.csv")

#Se retiran las columnas innecesarias del final
data.drop(data[["Type1","Type2","Cluster"]],axis="columns",inplace=True)
print(data)

#Se retira el doble índice y nombres
data.drop(data.columns[[0,1]],axis="columns",inplace=True)
print(data)

#Se asigna un 70% de varianza deseada a los componentes
pca = PCA(n_components=0.70)

#Imprime las filas y columnas del DataFrame original
print(f"Columnas DataFrame original: {len(data.columns)}")
print(f"Filas DataFrame original: {len(data[["power"]])}")
x_pca = pca.fit_transform(data)

col = len(x_pca[0])
#Imprime las filas y columnas de la matriz de PCA
print(f"\nColumnas DataFrame PCA: {col}")
print(f"Filas DataFrame PCA: {len(x_pca)}")

#Se asigna nombre a cada columna
columnas = [f"PCA{i+1}" for i in range(col)]

#Se crea un DataFrame para el PCA
data_pca = pd.DataFrame(data=x_pca,columns=columnas)

#Se inserta los nombres de los Pokemon en el índice 0 del DataFrame
data_pca.insert(0,"Pokemon",pkm_nombres)
print(data_pca)

#Se realiza KMeans a la matriz x_pca
km = KMeans(n_clusters=21, n_init=20)
clusters = km.fit_predict(x_pca)

#Se sacan lista de tipos primarios y secundarios a partir de una función relacionada con el .json
lista_tipos,lista_tipos_sec = file_to_json.retornar_tipos(pkm_nombres,tipos_json) #Más información en file_to_json.py

#Se agregan los tipos al DataFrame para facilitar el analisis al usar print
data_pca["Type1"] = lista_tipos
data_pca["Type2"] = lista_tipos_sec

#Agrega los clusters designados a cada Pokemon al DataFrame con el PCA
data_pca["Cluster"] = clusters

#Se crea el archivo .csv a partir del nuevo DataFrame
data_pca.to_csv("smogon_agrupado_PCA.csv")

print(data_pca)