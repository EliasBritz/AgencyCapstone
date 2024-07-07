from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

# Database
DATABASE_PATH = os.getenv('DATABASE_PATH')

# Auth0
AUTH_DOMAIN = os.getenv('AUTH_DOMAIN')
ALGORITHMS = os.getenv('ALGORITHMS')
API_AUDIENCE = os.getenv('API_AUDIENCE')
