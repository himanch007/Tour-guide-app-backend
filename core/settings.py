import os
from dotenv import load_dotenv

load_dotenv()


SECRET_KEY = os.environ.get('SECRET_KEY')


# Database name
DATABASE_NAME = 'Project_1_My_FastAPI_App'
