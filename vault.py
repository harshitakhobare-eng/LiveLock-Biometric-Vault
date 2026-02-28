import sqlite3
import numpy as np
from cryptography.fernet import Fernet
import os

if not os.path.exists("secret.key"):
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
else:
    with open("secret.key", "rb") as key_file:
        key = key_file.read()

cipher = Fernet(key)
SALT = b"Harshita_2026_NK_"

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY, username TEXT, embedding BLOB)''')
    conn.commit()
    conn.close()

def save_user(username, vector):
    vector_bytes = vector.astype(np.float64).tobytes()
    salted_data = vector_bytes + SALT
    encrypted_vector = cipher.encrypt(salted_data)
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, embedding) VALUES (?, ?)",
                   (username, encrypted_vector))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, embedding FROM users")
    data = cursor.fetchall()
    conn.close()
    return data

if __name__ == "__main__":
    init_db()