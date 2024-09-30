from os import getcwd
from os import getenv as ge
from os import path

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
client_secrets_file = ge('CLIENT_SECRETS_FILE')
client_token_pickle = ge('CLIENT_TOKEN_PICKLE')
if isinstance(client_secrets_file,str):
    client_secrets_file = path.join(getcwd(),client_secrets_file)
if isinstance(client_token_pickle,str):
    client_token_pickle = path.join(getcwd(),client_token_pickle)