#!/usr/bin/python python3

import socket
import threading
import sys
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
from cryptography.fernet import Fernet
import binascii

def start_socket(ip,port):
    
    s = socket.socket()
    s.bind((ip, port))
    s.listen(5)
    print("Waiting for connections")
    return(s.accept())

def generate_keys(key_size):

    key = RSA.generate(key_size)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return(private_key, public_key)

def generate_session_key():

    return(Fernet.generate_key())

def encrypt_session_key(public_key, session_key):

    public_rsa = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(key=public_rsa)
    return(cipher.encrypt(session_key))

def decrypt_session_key(private_key, session_key):

    private_rsa = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(key=private_rsa)
    return(cipher.decrypt(session_key))

def recv_msg():
    while True:
        recv_msg = conn.recv(1024)
        if not recv_msg:
            sys.exit(0)
        decrypted_msg = fernet.decrypt(recv_msg)
        print("> ",decrypted_msg.decode())

def send_msg():
    while True:
        send_msg = input()
        encrypted_msg = fernet.encrypt(send_msg.encode())
        conn.send(encrypted_msg)
        

if __name__ == '__main__':
#set up key echange


    conn, addr = start_socket("",8080)
    private_key, public_key = generate_keys(2048)
    conn.send(public_key)
    session_key_encrypted = conn.recv(1024)
    session_key = decrypt_session_key(private_key, session_key_encrypted)
    
    message = "Encrypted connection fully established"
    fernet = Fernet(session_key)
    encMessage = fernet.encrypt(message.encode())
    conn.sendall(encMessage)
    print(message)
    print()

    t = threading.Thread(target=recv_msg)
    t.start()

    send_msg() 
