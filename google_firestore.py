import bcrypt
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
import os

file_path = os.getenv("file_path")

if not firebase_admin._apps:
    cred = credentials.Certificate(file_path)
    app_firebase = firebase_admin.initialize_app(cred)
    
store = firestore.client()


def encript_password(password):
    password_str = str(password)
    # converting password to array of bytes 
    bytes = password_str.encode('utf-8') 
  
    # generating the salt 
    salt = bcrypt.gensalt() 
  
    # Hashing the password 
    hash = bcrypt.hashpw(bytes, salt) 

    return hash

def adiciona_usuario(user, password):
    
    # Checa se o usuário existe
    user_query = store.collection('app_logins').where('user', '==', user).get()
    if user_query:
        print(f"Usuário '{user}' já existe!")
        return False
    
    password_str = str(password)
    hashed_password = encript_password(password_str)
    
    doc_ref = store.collection(u'app_logins')
    doc_ref.add({
        u'user': user, 
        u'hash': hashed_password.decode('utf-8')
    })

    print(f"User '{user}' added successfully!")
    return True


def valida_login(user, userPassword):
    userPassword_str = str(userPassword)
    
    user_query = store.collection('app_logins').where('user', '==', user).get()
    if not user_query:
        return False
    
    user_data = user_query[0].to_dict()
    stored_hash = user_data.get('hash')

    # Compara os hashs
    return bcrypt.checkpw(userPassword_str.encode('utf-8'), stored_hash.encode('utf-8'))
        



