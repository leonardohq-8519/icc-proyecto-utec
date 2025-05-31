import type_file
import json
import re

'''
repo = "smogon/pokemon-showdown"
file_path = "data/pokedex.ts"
'''

def convert(repo:str, file_path:str):
    #Se obtiene un string del archivo de Github
    content = type_file.get_files(repo_name=repo,file_path=file_path)

    #Se retiran los comentarios del objeto de .ts
    no_comments_content = re.sub(r'\s*//.*', '',content[70:-2])

    #Se quitan los saltos de linea y tabulaciones
    no_spaces_content =  re.sub(r"\s+", " ", no_comments_content).strip()

    #Se agregan comillas a las llaves del json
    quotes_fixed = re.sub(r"(\w+):",r'"\1":', no_spaces_content)

    #Se quitan comas adicionales, despues de llaves y corchetes
    dex = re.sub(r",\s*}",r"}",quotes_fixed)
    dex = re.sub(r",\s*(\}|\])", r"\1",dex)

    #Se reemplazan comillas simples por dobles
    dex = re.sub(r"\'(\w+)\'",r'"\1"',dex)

    #Hotfix de TypeNull
    dex = re.sub(r"\"(\w*)\"(\w*)\"",r'"\1\2',dex)
    dex_json = json.loads(dex)

    return dex_json

def retornar_tipos(nombres,tipos_json):
    lista_tipos = []
    lista_tipos_sec = []

    #Recorre los nombres de todos los Pokemon
    for nombre in nombres:
        #Limpia el nombre de caracteres extraños
        name = re.sub(r"\W+","",nombre)
        #Brute Force a meowsticm (Está como meowstic en el otro archivo)
        if name.lower() == "meowsticm":
            name = name[:-1]
        #Revisa el tipo primario según el .json y lo añade a la lista correspondiente
        lista_tipos.append(tipos_json[name.lower()]["types"][0])
        #De existir un tipo secundario en la lista del .json, lo añade a la lista de tipos secundarios
        #De lo contrario se pone "None"
        if len(tipos_json[name.lower()]["types"]) == 2:
            lista_tipos_sec.append(tipos_json[name.lower()]["types"][1])
        else:
            lista_tipos_sec.append("None")
    #Retorna ambas listas
    return lista_tipos, lista_tipos_sec