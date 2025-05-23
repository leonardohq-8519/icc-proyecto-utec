import github
import os
import dotenv

dotenv.load_dotenv()

def get_files(repo_name:str,file_path:str):
    token = os.getenv("GITHUB_TOKEN")
    auth = github.Auth.Token(token)
    g = github.Github(auth=auth)

    try:
        repo = g.get_repo(repo_name)
        file_as_object = repo.get_contents(file_path)
        file_content = file_as_object.decoded_content.decode("utf-8")

        return file_content
    except Exception as e:
        print("Error: ",e)
