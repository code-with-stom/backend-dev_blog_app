from passlib.context import CryptContext
import re
import secrets
    
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def generate_slug(title: str) -> str:
    # Convert the title to lowercase and remove leading/trailing whitespace
    title = title.lower().strip()
    
    # Remove any non-alphanumeric characters (except spaces and hyphens)
    title = re.sub(r"[^a-z0-9\s-]", "", title)
    
    # Replace spaces and consecutive hyphens with a single hyphen
    title = re.sub(r"[\s-]+", "-", title)
    
    # Remove leading and trailing hyphens
    title = title.strip("-")
    return title

def hash_password(pwd: str) -> str:
    return pwd_context.hash(pwd)

def verify_password(pwd: str, hash_pwd: str) -> bool:
    return pwd_context.verify(pwd, hash_pwd)

def generate_username(email: str) -> str:
    username = email.split("@")[0]
    
    username = re.sub(r"[^a-zA-Z0-9_]", "", username)
    
    secret_string = secrets.token_hex(16)
    
    return f"{username}-{secret_string}"