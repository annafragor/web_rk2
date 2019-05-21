import random

# the encoding matrix
G = ['1101', '1011', '1000', '0111', '0100', '0010', '0001']
# the parity-check matrix
H = ['1010101', '0110011', '0001111']
Ht = ['100', '010', '110', '001', '101', '011', '111']
# the decoding matrix
R = ['0010000', '0000100', '0000010', '0000001']


def encode(data):
    return ''.join([str(bin(int(i, 2) & int(data, 2)).count('1') % 2) for i in G])


def decode(data):
    z = ''.join([str(bin(int(j, 2) & int(data, 2)).count('1') % 2) for j in H])
    if int(z, 2) > 0:
        e = int(Ht[int(z, 2) - 1], 2)
    else:
        e = 0
    print('Which bit found to have error (0: no error): ' + str(e))

    msg = 'No error during transmission. '

    # correct the error
    if e > 0:
        msg = 'Error was corrected. '
        data = list(data)
        data[e - 1] = str(1 - int(data[e - 1]))
        data = ''.join(data)

    return msg, ''.join([str(bin(int(k, 2) & int(data, 2)).count('1') % 2) for k in R])


def create_error(data):
    # add 1 bit error
    e = random.randint(0, 7)
    # counted from left starting from 1
    print('Which bit got error during transmission (0: no error): ' + str(e))

    if e > 0:
        data = list(data)
        data[e - 1] = str(1 - int(data[e - 1]))
        data = ''.join(data)
    print('Encoded bit string that got error during tranmission: ' + data)
    return data
