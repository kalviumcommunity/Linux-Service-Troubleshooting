import socket
import time

HOST = '127.0.0.1'
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(1)
    print(f'Rogue service listening on {HOST}:{PORT}')
    while True:
        conn, addr = sock.accept()
        with conn:
            conn.sendall(b'Port reserved by rogue service\n')
