#!/usr/bin/env python3

import socket
import random
import hamming.functions as f


HOST = '127.0.0.1'
PORT = 54322


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = ''.join([random.choice('01') for k in range(4)])
        print('Data to send: ' + data)

        encoded_string = f.encode(data)
        print('Encoded string: ' + encoded_string)
        encoded_string = f.create_error(encoded_string)

        s.sendall(str.encode(encoded_string))  # encoded_string to byte array

        server_reply = s.recv(1024)

        print('Received: ', repr(server_reply))
