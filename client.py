# Hieu Nguyen - hmnguyen626@gmail.com

import socket
import sys
import os

if len(sys.argv) < 2:
    print("USAGE python " + sys.argv[0] + " <SERVER MACHINE> <PORT NUMBER>")

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)


# CWD + server directory -hieu
current_path = os.path.dirname(__file__) + '/client/'

try:

    while 1:
        line = input('ftp> ')
        strLine = str(line)

        if line == 'quit':
            line = line.encode()
            sock.sendall(line)
            quit()
        elif line[0] == 'p' and line[1] == 'u' and line[2] == 't':

            cmd_put = line.encode()
            sock.sendall(cmd_put)
            print('Sending to server the file: ' + line[4:])
            file_location = current_path + line[4:]
            try:
                with open(file_location, 'r') as put_file:
                    data_p = put_file.read()
            except:
                print('Error finding file')
            data_put = data_p.encode()
            sock.sendall(data_put)

        elif line == 'ls':
            line = line.encode()
            sock.sendall(line)
            data = sock.recv(1024)
            data_print = data.decode()
            print(data_print)
            line = line.decode()

        # ftp> Get logic
        elif line[0] == 'g' and line[1] == 'e' and line[2] == 't':
            check_for_txt = str(line)
            if '.txt' in check_for_txt:

                # new file location
                new_file = current_path + line[4:]

                # Encoding and decoding data to write
                cmd_get = line.encode()
                sock.sendall(cmd_get)
                data_get = sock.recv(1024)
                newline = data_get.decode("utf-8")

                # Write to file, create new if not existing
                try:
                    with open(new_file, 'w') as fin:
                        fin.write(newline)
                    print('Successfully received the file ' + line[4:])
                except:
                    print('Error saving the file ' + line[4:])
            else:
                print('Invalid File name')

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(1024)
        amount_received += len(data)
        print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()
