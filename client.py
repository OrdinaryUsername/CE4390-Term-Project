import socket
import shutil


def client_main():
    # initialize client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    target_ip = '10.0.0.1'

    target_port = 49159

    # accepted cmds for input
    acceptedCmds = ['list', 'copy', 'rename', 'delete', 'done']

    # listen
    while 1:
        client.connect((target_ip, target_port))
        packet = packetFormat('Request Connection')
        client.send(bytes(packet, "utf-8"))
        data = client.recv(1024)
        print(parse_message(data))
        print(' ')
        print("Connected to server")
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
        cmdCheck = cmd.split(' ')
        # Checks if user input matches
        if (cmdCheck[0] in acceptedCmds):
            if (cmd == 'done'):
                packet == packetFormat(cmd)
                client.send(bytes(packet, "utf-8"))
                break
            else:
                packet == packetFormat(cmd)
                client.send(bytes(packet, "utf-8"))
                data = client.recv(1024)
                print(data.decode("utf-8"))
        else:
            print('Please enter valid command!')

        # shut down the connection
        # close the socket
        client.close()
        # open the socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # shut down the connection
    # client.shutdown(socket.SHUT_RDWR)
    print("shutdown")
    # close the socket
    client.close()
    print("close")


def parse_message(data):
    data.decode("utf-8")
    msg = data.replace('\n', '')
    message = msg.split('\r')

    if message[0] == '1':
        if message[1] == '2':
            response = 'Connection accepted'
    elif message[0] == '3':
        if message[1] == '11':
            response = 'Command success'
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

def packetFormat(str):
    
    op = str.split(' ')
    
    if(str == 'Request Connection'):
        messageType = '1'
        messageCode = '1'
        filenames = None
        messageLength = '10'
        payload = None
    elif op[0] == 'list':
        messageType = '2'
        messageCode = '3'
        filenames = None
        messageLength = '10'
        payload = None
    elif op[0] == 'copy':
        messageType = '2'
        messageCode = '4'
        filenames = op[1]
        messageLength = str(10 + len(op[1]))
        payload = None
    elif op[0] == 'rename':
        messageType = '2'
        messageCode = '5'
        filenames = op[1]
        messageLength = str(10 + len(op[1]))
        payload = None
    elif op[0] == 'delete':
        messageType = '2'
        messageCode = '6'
        filenames = op[1]
        messageLength = str(10 + len(op[1]))
        payload = None
    elif op[0] == 'done':
        messageType = '2'
        messageCode = '7'
        filenames = op[1]
        messageLength = str(10 + len(op[1]))
        payload = None
        
    return (messageType + '\r' + messageCode + '\r\n' + filenames + '\r' + messageLength + '\r\n\r\n' + payload)
# use client_main() as the main function
if __name__ == "__main__": client_main()