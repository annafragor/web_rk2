#!/usr/bin/env python3

# 1. The receiver receives the encoded data string from the sender.
# 2. Receiver with the help of the key decodes the data and find out the remainder.
# 3. If the remainder is zero then it means there no error in data sent by the sender to receiver.
# 4. If the remainder comes out to be non-zero it means there was an error,
#    a Negative Acknowledgement is sent to the sender.
#    The sender then resends the data until the receiver receives correct data.

import socket
import crc.functions as f

poly = 0xEDB88320

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65433        # Port to listen on (non-privileged ports are > 1023)

key = "1001"


# Function used at the receiver side to decode
# data received by sender
def decodeData(data, key):
    l_key = len(key)

    # Appends n-1 zeroes at end of data
    appended_data = data.decode() + '0' * (l_key - 1)  # data.decode - to string from bytes
    remainder = f.mod2div(appended_data, key)

    return remainder


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

                # decoded_data = decodeData(data, key)

                data_with_error = f.xor(data, "1")
                decoded_data_with_error = decodeData(str.encode(data_with_error), key)
                temp = "0" * (len(key) - 1)
                if decoded_data_with_error == temp:
                    conn.sendall(data + b" received.\nNO ERROR.")
                else:
                    conn.sendall(b"ERROR in data")

                # If remainder is all zeros then no error occured
                # temp = "0" * (len(key) - 1)
                # if decoded_data == temp:
                #     conn.sendall(data + b" received.\nNO ERROR.")
                # else:
                #     conn.sendall(b"ERROR in data")
