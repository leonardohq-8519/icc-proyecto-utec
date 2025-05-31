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

#Crea una lista con todos los tipos elementales
types = ["Normal","Fire","Water","Grass","Electric","Ice","Fighting","Poison","Ground","Flying","Psychic","Bug","Rock","Ghost","Dragon","Dark","Steel","Fairy"]

#Modifica y limpia (por seguridad) la lista. Se crea un patron tal que:
#Tipo1|Tipo2|Tipo3|Tipo4|...|Tipo18
pattern = "|".join(map(re.escape, types))

'''A partir de un lambda se busca los tipos en cada instancia de la columna "moves", removiendo todas las palabras
y partes de estas que no estén dentro de la lista.'''
#.apply itera en la columna y el lambda busca los tipos por cada elemento
smogon["moves"] = smogon["moves"].apply(lambda columna: ' '.join(re.findall(pattern, str(columna), re.IGNORECASE)))

#Se realiza TD-IDF con las stopwords de NLTK solo para unigramas
vec = TfidfVectorizer(stop_words=stopwords.words("english"))
clasificacion = vec.fit_transform(raw_documents=smogon["moves"])
tokens = vec.vocabulary_.keys()

#Imprime los tokenes y el número total de estos
print(f"Tokens: {tokens}\nNúmero de tokens: {len(tokens)}")

#A partir del agrupamiento del TF-IDF (Pasado a un array) se genera un DataFrame nuevo
smogon_agrupado = pd.DataFrame(data=clasificacion.toarray(),columns=sorted(tokens))

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

#Imprime el DataFrame para analizarlo
print(smogon_agrupado)
