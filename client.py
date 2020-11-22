import socket
# import shutil


def client_main():
    # initialize client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    target_ip = '10.0.0.1'

    target_port = 49159

    # accepted cmds for input
    accepted_cmds = ['list', 'copy', 'rename', 'delete', 'done']

    # listen
    while 1:
        print(' ')
        print('Requesting connection with server...')
        client.connect((target_ip, target_port))
        packet = message_format('Request Connection')
        client.send(bytes(packet, "utf-8"))
        data = client.recv(1024)
        print(parse_message(data))
        print(' ')
        print('------------------------------------------------------------------')
        print('Instruction List:')
        print('"list" lists file directory on server.')
        print('"copy <filename>" creates a copy of a file on the server.')
        print('"rename <original_filename>, <new_filename>" renames a file from the server.')
        print('"delete <filename>" deletes a file on the server.')
        print('"done" quits program.')
        print('------------------------------------------------------------------')
        print(' ')
        # get the user's command
        cmd = input('Enter a command: ')
        print(' ')
        # Split cmd for check
        cmd_check = cmd.split(' ')
        # Checks if user input matches
        if cmd_check[0] in accepted_cmds:
            if cmd == 'done':
                packet = message_format(cmd)
                client.send(bytes(packet, "utf-8"))
                break
            else:
                packet = message_format(cmd)
                client.send(bytes(packet, "utf-8"))
                data = client.recv(1024)
                print(parse_message(data))
        else:
            print('Please enter valid command!')

        # shut down the connection
        # close the socket
        print("Closing connection with server...")
        client.close()
        print("Connection with server closed.")
        # open the socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # shut down the connection
    # client.shutdown(socket.SHUT_RDWR)
    print("shutdown")
    # close the socket
    client.close()
    print("close")


def parse_message(data):
    decoded_data = data.decode("utf-8")
    msg = decoded_data.replace('\r', '')
    message = msg.split('\n')

    response = "ERROR: message type and code are not valid"

    if message[0] == '1':
        if message[1] == '2':
            response = 'Connection accepted'
    elif message[0] == '3':
        if message[1] == '11':
            response = 'Command success'
        elif message[1] == '12':
            response = message[5]
    elif message[0] == '4':
        if message[1] == '8':
            filename1 = message[2]
            response = 'ERROR: File ' + filename1 + ' does not exist!'
        elif message[1] == '9':
            filename1 = message[2]
            response = 'ERROR: File name ' + filename1 + ' already exists!'
        elif message[1] == '10':
            filename1 = message[2]
            response = 'ERROR: ' + filename1 + ' is an invalid filename!'

    return response


def message_format(message):
    op = message.split(' ')

    if message == 'Request Connection':
        mtype = '1'
        code = '1'
        filenames = ''
        payload = ''
        length = str(len(mtype + '\n' + code + '\r\n' + filenames + '\n' + '\r\n\r\n' + payload))
    elif op[0] == 'list':
        mtype = '2'
        code = '3'
        filenames = ''
        payload = ''
        length = str(len(mtype + '\n' + code + '\r\n' + filenames + '\n' + '\r\n\r\n' + payload))
    elif op[0] == 'copy':
        mtype = '2'
        code = '4'
        filenames = op[1]
        payload = ''
        length = str(len(mtype + '\n' + code + '\r\n' + filenames + '\n' + '\r\n\r\n' + payload))
    elif op[0] == 'rename':
        mtype = '2'
        code = '5'
        filenames = op[1] + op[2]
        filenames.replace(', ', ',')
        payload = ''
        length = str(len(mtype + '\n' + code + '\r\n' + filenames + '\n' + '\r\n\r\n' + payload))
    elif op[0] == 'delete':
        mtype = '2'
        code = '6'
        filenames = op[1]
        payload = ''
        length = str(len(mtype + '\n' + code + '\r\n' + filenames + '\n' + '\r\n\r\n' + payload))
    elif op[0] == 'done':
        mtype = '2'
        code = '7'
        filenames = ''
        payload = ''
        length = str(len(mtype + '\n' + code + '\r\n' + filenames + '\n' + '\r\n\r\n' + payload))
    else:
        mtype = ''
        code = ''
        filenames = ''
        payload = ''
        length = str(len(mtype + '\n' + code + '\r\n' + filenames + '\n' + '\r\n\r\n' + payload))
    return mtype + '\n' + code + '\r\n' + filenames + '\n' + length + '\r\n\r\n' + payload


# use client_main() as the main function
if __name__ == "__main__":
    client_main()
