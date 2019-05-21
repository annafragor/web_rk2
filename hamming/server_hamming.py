#!/usr/bin/env python3

import socket
import hamming.functions as f

poly = 0xEDB88320

HOST = '127.0.0.1'
PORT = 54322


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
                msg, decoded_data = f.decode(data.decode())
                conn.sendall(str.encode(msg) + b"Decoded data: " + str.encode(decoded_data))

                # data_with_error = f.xor(data, "1")
                # decoded_data_with_error = decodeData(str.encode(data_with_error), key)
                # temp = "0" * (len(key) - 1)
                # if decoded_data_with_error == temp:
                #     conn.sendall(data + b" received.\nNO ERROR.")
                # else:
                #     conn.sendall(b"ERROR in data")
