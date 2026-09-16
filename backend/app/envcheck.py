from dotenv import load_dotenv
import os

load_dotenv()

print(os.getenv("COGNITO_CLIENT_ID"))
print(os.getenv("COGNITO_CLIENT_SECRET"))
