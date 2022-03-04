from werkzeug.security import safe_str_cmp, generate_password_hash
from passlib.context import CryptContext

crypt_context = CryptContext(schemes=["bcrypt_sha256"])

def generate_hash(user_obj):
    return generate_password_hash(user_obj.password,method='pbkdf2:sha512')

def check_password(user_db, user_ext):
    hash_password = generate_hash(user_ext)
    print(hash_password)
    print(user_db.password)
    if safe_str_cmp(hash_password, user_db.password):
        return True
    

