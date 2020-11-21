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
        print(' ')
        print("Connected to server")
        print(' ')
        print('------------------------------------------------------------------')
        print('Instruction List:')
        print('"list" lists file directory on server.')
        print('"copy[filename]" retrieves a copy of a file from the server.')
        print('"rename[filename, newFileName]" renames a file from the server.')
        print('"delete[filename]" deletes a file on the server.')
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
                client.send(bytes(cmd, "utf-8"))
                break
            else:
                client.send(bytes(cmd, "utf-8"))
                data = client.recv(1024)
                print(data.decode("utf-8"))
        else:
            print('Please enter valid command!')

    
        # shut down the connection
        #client.shutdown(socket.SHUT_RDWR)
        # close the socket
        client.close()
        # open the socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # shut down the connection
    #client.shutdown(socket.SHUT_RDWR)
    print("shutdown")
    # close the socket
    client.close()
    print("close")


# use client_main() as the main function
if __name__ == "__main__": client_main()