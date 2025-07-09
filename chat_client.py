# chat_client.py

import socket
import threading
from cryptography.fernet import Fernet

# Gunakan kunci yang sama dengan server
key = b'44JiwPLMhYmiWaXnTfLU_fSKSUkNxqZ_KvkXp3zDkBs='
fernet = Fernet(key)

def receive_msg(sock):
    while True:
        try:
            encrypted_msg = sock.recv(1024)
            msg = fernet.decrypt(encrypted_msg).decode()
            print("\n[Pesan Masuk] " + msg)
        except:
            print("[!] Terputus dari server.")
            break

def main():
    host = '192.168.222.155'
    port = 12345

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print("[*] Terhubung ke server.\n")

    threading.Thread(target=receive_msg, args=(sock,), daemon=True).start()

    while True:
        msg = input("> ")
        encrypted_msg = fernet.encrypt(msg.encode())
        sock.send(encrypted_msg)

if __name__ == "__main__":
    main()
