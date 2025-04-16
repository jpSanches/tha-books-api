import os
from dotenv import load_dotenv

load_dotenv()

# JWT Configs
SECRET_KEY = os.getenv("SECRET_ENCRYPTION_JWT_KEY", "")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # one day

# Access configs
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")
