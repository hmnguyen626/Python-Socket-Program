# Hieu Nguyen - hmnguyen626@gmail.com

import socket
import os

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# CWD + server directory
current_path = os.path.dirname(__file__) + '/server/'

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:

            data = connection.recv(1024)
            print('received {!r}'.format(data))
            data = data.decode()
            if data == 'quit':
                break;
            if data == 'ls':
                getls = os.listdir("server")
                data_ls = ''
                for i in range(len(getls)):
                    if i == len(getls) - 1:
                        data += getls[i]
                    else:
                        data += ' ' + getls[i] + ' '
                data_ls = data.encode()
                print('sending data back to the client')
                connection.sendall(data_ls)

                # ftp> get logic -hieu
            elif data[0] == 'g' and data[1] == 'e' and data[2] == 't':
                print('Sending to client the file: ' + data[4:])

                # File searching logic -hieu
                file_location = current_path + data[4:]
                try:
                    with open(file_location, 'r') as fin:
                        data = fin.read()
                except:
                    print('Error finding file')
                data_get = data.encode()
                connection.sendall(data_get)

            elif data[0] == 'p' and data[1] == 'u' and data[2] == 't':
                check_for_txt = str(data)
                if '.txt' in check_for_txt:
                    data_put = connection.recv(1024)
                    newline = data_put.decode()

                    # new file location
                    new_file = current_path + data[4:]

                    # Write to file, create new if not existing
                    try:
                        with open(new_file, 'w') as write_put:
                            write_put.write(newline)
                        print('Successfully received the file ' + data[4:])
                    except:
                        print('Error saving the file ' + data[4:])

                    print('sending data back to the client')
                    server_folder = os.path.dirname(os.path.abspath('server'))
            else:
                print('no data from', client_address)

    finally:
        # Clean up the connection
        connection.close()
