import github
import os
import dotenv

#Carga un .env personal por PC
#El .env debe contener un GITHUB_TOKEN = "Inserte token de Github"
dotenv.load_dotenv()

def get_files(repo_name:str,file_path:str):

    #Lee el token del .env
    token = os.getenv("GITHUB_TOKEN")

    #Autentifica el usuario con el token
    auth = github.Auth.Token(token)

    #Se accede al Github por medio de la autentificación
    g = github.Github(auth=auth)

    try:
        #Se intenta acceder al repositorio
        repo = g.get_repo(repo_name)

        #Se busca el archivo en el repositorio (Agregar directorio)
        file_as_object = repo.get_contents(file_path)

        #Se decodifica el archivo a un string
        file_content = file_as_object.decoded_content.decode("utf-8")

        #Retorna el string
        return file_content
    except Exception as e:
        #Imprime el error ocurrido
        print("Error: ",e)
