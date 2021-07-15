#!/usr/bin/python python3

import socket
import threading
import sys
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
from cryptography.fernet import Fernet
import binascii

#set up key echange

def connect_socket(ip,port):
    
    s = socket.socket()
    s.connect((ip, port))
    print("Client has connected to sever at ", ip, str(port))
    return(s)
    
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
    print(threading.current_thread().getName())
    while True:
        recv_msg = s.recv(1024)
        if not recv_msg:
            sys.exit(0)

        decrypted_msg = fernet.decrypt(recv_msg)
        print("> ",decrypted_msg.decode())

def send_msg():
    while True:
        send_msg = input()
        encrypted_msg = fernet.encrypt(send_msg.encode())
        s.send(encrypted_msg)
        

if __name__ == '__main__':

    s = connect_socket("192.168.16.100", 8080)
    public_key = s.recv(2048)

    session_key=generate_session_key()
    session_key_encrypted = encrypt_session_key(public_key,session_key)

    s.sendall(session_key_encrypted)
    
#    print(session_key)


    encMessage = s.recv(1024)
    fernet = Fernet(session_key)
    decMessage = fernet.decrypt(encMessage).decode()
    print(decMessage)
    print()
    t = threading.Thread(target=recv_msg)
    t.start()


    send_msg()
    

