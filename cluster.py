import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer,  TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
import file_to_json
import re

repo = "smogon/pokemon-showdown"
file_path = "data/pokedex.ts"
tipos_json = file_to_json.convert(repo,file_path)

smogon = pd.read_csv("smogon.csv")
#TF-IDF tf(x,y) * log (N/df)
vec = TfidfVectorizer(stop_words=stopwords.words("english"), ngram_range=(1,3))
clasificacion = vec.fit_transform(raw_documents=smogon["moves"])
tokens = vec.vocabulary_.keys()

smogon_agrupado = pd.DataFrame(data=clasificacion.toarray(),columns=sorted(tokens))
km = KMeans(n_clusters=18, n_init=100)
lista = km.fit_predict(smogon_agrupado)

smogon_agrupado["Cluster"] = lista
#Sacar de smogon nombres
pkm_nombres = smogon[["Pokemon"]]
lista_tipos = []
lista_tipos_sec = []
for nombre in pkm_nombres["Pokemon"]:
    name = re.sub(r"\W+","",nombre)
    #Brute Force a meowsticm
    if name.lower() == "meowsticm":
        name = name[:-1]
    lista_tipos.append(tipos_json[name.lower()]["types"][0])
    if len(tipos_json[name.lower()]["types"]) == 2:
        lista_tipos_sec.append(tipos_json[name.lower()]["types"][1])
    else:
        lista_tipos_sec.append("None")

smogon["Type1"] = lista_tipos
smogon["Type2"] = lista_tipos_sec
#Retirar columna types
#Comparar nombres de smogon con las keys del json
#Agregar tipo 1 y tipo 2 por pokemon a smogon

smogon.drop(smogon.columns[[1,2,3]],axis='columns',inplace=True)
smogon.to_csv("prueba.csv")
smogon["Cluster"] = lista
smogon.to_csv("prueba_con_cluster.csv")
print(smogon_agrupado)
'''print(f"Tokens: {tokens}")
print(f"El número total de tokens es: {len(tokens)}")
'''
