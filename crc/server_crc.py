#!/usr/bin/env python3

import socket
import crc.functions as f

poly = 0xEDB88320

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65433        # Port to listen on (non-privileged ports are > 1023)

key = "1001"


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print('Socket is listening.')
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)

                # decoded_data = f.decodeData(data, key)
                # If remainder is all zeros then no error occured
                # temp = "0" * (len(key) - 1)
                # if decoded_data == temp:
                #     conn.sendall(data + b" received.\nNO ERROR.")
                # else:
                #     conn.sendall(b"ERROR in data")

                data_with_error = f.xor(data, "1")
                decoded_data_with_error = f.decodeData(str.encode(data_with_error), key)
                temp = "0" * (len(key) - 1)
                if decoded_data_with_error == temp:
                    conn.sendall(data + b" received.\nNO ERROR.")
                else:
                    conn.sendall(b"ERROR in data")
