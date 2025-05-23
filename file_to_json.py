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