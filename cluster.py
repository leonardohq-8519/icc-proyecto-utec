import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer,  TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
import file_to_json
import re

#Se define el repositorio a buscar y el directorio del archivo
repo = "smogon/pokemon-showdown"
file_path = "data/pokedex.ts"

#Trae la información del archivo de GitHub a una variable
#Modifica la información recabada para pasarla a formato json
tipos_json = file_to_json.convert(repo,file_path) #Accede al archivo file_to_json.py para más información

#Se lee el archivo csv de smogon
smogon = pd.read_csv("smogon.csv")
#Se realiza TD-IDF con las stopwords de NLTK para unigramas, bigramas y trigramas
vec = TfidfVectorizer(stop_words=stopwords.words("english"), ngram_range=(1,3))
agrupamiento = vec.fit_transform(raw_documents=smogon["moves"])
tokens = vec.vocabulary_.keys()

#Imprime los tokenes y el número total de estos
print(f"El número total de tokens es: {len(tokens)}")
print(f"Tokens: {tokens}")

#A partir del agrupamiento del TF-IDF (Pasado a un array) se genera un DataFrame nuevo
smogon_agrupado = pd.DataFrame(data=agrupamiento.toarray(),columns=sorted(tokens))
print(smogon_agrupado)

#Se prepara un KMeans de 21 clusters
km = KMeans(n_clusters=21, n_init=100)
#Se realiza KMeans al DataFrame nuevo
lista = km.fit_predict(smogon_agrupado)


#Del DataFrame original se saca la columna con los nombres
pkm_nombres = smogon[["Pokemon"]]["Pokemon"]

#Se agrega la columna al nuevo DataFrame en el índice 0 para ubicarse mejor al analizar
smogon_agrupado.insert(0,"Pokemon",pkm_nombres)

#Se sacan lista de tipos primarios y secundarios a partir de una función relacionada con el .json
lista_tipos,lista_tipos_sec = file_to_json.retornar_tipos(pkm_nombres,tipos_json) #Más información en file_to_json.py

#Agrega los tipos como columnas en el Dataframe nuevo
smogon_agrupado["Type1"] = lista_tipos
smogon_agrupado["Type2"] = lista_tipos_sec

#Agrega los clusters designados a cada Pokemon
smogon_agrupado["Cluster"] = lista

#Genera un .csv a partir del nuevo DataFrame
smogon_agrupado.to_csv("smogon_agrupado_1.csv")

#Imprime el DataFrame para analizarlo (Uso en caso que no se pueda abrir el .csv)
print(smogon_agrupado)


