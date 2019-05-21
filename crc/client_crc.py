#!/usr/bin/env python3

import socket
import crc.functions as f

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65433        # The port used by the server

key = "1001"


# Function used at the sender side to encode
# data by appending remainder of modular divison
# at the end of data.
def encodeData(data, key):
    l_key = len(key)

    # Appends n-1 zeroes at end of data
    appended_data = data + '0' * (l_key - 1)
    remainder = f.mod2div(appended_data, key)

    # Append remainder in the original data
    codeword = data + remainder
    return codeword


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        input_string = input("Your string to send: ")
        data = (''.join(format(ord(x), 'b') for x in input_string))
        print(data)

        encoded_string = encodeData(data, key)
        print(encoded_string)
        s.sendall(str.encode(encoded_string))  # encoded_string to byte array

        server_reply = s.recv(1024)

        print('Received: ', repr(server_reply))
