# chat_server.py

import socket
import threading
from cryptography.fernet import Fernet

# Gunakan kunci hasil generate kamu
key = b'44JiwPLMhYmiWaXnTfLU_fSKSUkNxqZ_KvkXp3zDkBs='
fernet = Fernet(key)

clients = []

def handle_client(conn, addr):
    print(f"[+] Koneksi dari {addr}")
    while True:
        try:
            encrypted_msg = conn.recv(1024)
            msg = fernet.decrypt(encrypted_msg).decode()
            print(f"[{addr}] {msg}")

            # Kirim ke semua client lain
            for c in clients:
                if c != conn:
                    c.send(fernet.encrypt(msg.encode()))
        except:
            clients.remove(conn)
            conn.close()
            break

def main():
    host = ''
    
    port = 12345

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"[*] Server aktif di {host}:{port}")

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()
