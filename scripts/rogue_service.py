#!/usr/bin/env python3
import socket
import time
import sys
import os

HOST = '127.0.0.1'
PORT = 8080

def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen(5)
            # Write a small file with the PID of rogue service for verification or clean shutdown
            pid_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rogue.pid')
            with open(pid_file, 'w') as f:
                f.write(str(os.getpid()))
                
            while True:
                try:
                    conn, addr = s.accept()
                    with conn:
                        # Receive request
                        conn.recv(1024)
                        # Respond with simulated conflict error
                        response_body = (
                            '{{"error": "Port conflict detected", '
                            '"message": "Port 8080 is occupied by rogue_service.py", '
                            '"pid": {}}}\n'
                        ).format(os.getpid())
                        
                        response = (
                            "HTTP/1.1 409 Conflict\r\n"
                            "Content-Type: application/json\r\n"
                            "Connection: close\r\n"
                            "Content-Length: {}\r\n\r\n"
                            "{}"
                        ).format(len(response_body), response_body)
                        conn.sendall(response.encode('utf-8'))
                except Exception:
                    pass
    except OSError as e:
        sys.stderr.write(f"Rogue service failed to bind: {e}\n")
        sys.exit(1)

if __name__ == '__main__':
    main()
