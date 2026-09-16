# Contains the OAuth registration and JWT validation
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
import os

load_dotenv()

oauth = OAuth()

oauth.register(
    name="cognito",
    client_id=os.getenv("COGNITO_CLIENT_ID"),
    client_secret=os.getenv("COGNITO_CLIENT_SECRET"),
    server_metadata_url=os.getenv("COGNITO_METADATA_URL"),
    client_kwargs={
        "scope": "openid email profile",
    },
)