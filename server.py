import socket
import os
from os import path
import string
import shutil


def server_main(server=socket):
    # create and initialize server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # get the server's ip address
    # ip = socket.gethostbyname(socket.gethostname())
    host = socket.gethostbyname(socket.gethostname())
    print(socket.gethostname())
    # ip = input("Enter IP Address: ")
    # get the port number for the host
    #port = int(input('Enter desired port: '))
    port = 49159
    # bind the socket using the ip address and port number
    server.bind((host, port))
    print("bound")
    # listen for connection requests
    server.listen(1000000)

    print('Listening on IP: ' + host + ', ' + str(port))
    # accept the connection request
    server.accept()
    print("Connection accepted")

    while 1:


        # recieve message from client using client_message = server.recv(1024)
        data = server.recv(1024)
        print("recieving data")
        # Add the data to the client message
        client_message = data
        data = server.recv(1024)
        # while there is still data coming in
        #   Note: may need to use while 1 loop to get all of the message contents
        #   and break when no longer recieving anything
        while data:
            # add the data to the client message
            client_message += data
            # recieve the data
            data = server.recv(1024)

        print("decoding data")
        # decode server message using client_message.decode()
        client_message.decode()

        # split the client message to get the command type and parameters
        # in separate strings in an array of strings
        cmd = client_message.split(" ")
        print(cmd)

        # do stuff based on the message contents and protocol format (flags, etc)
        #   Note: look at os library for file management functions??
        #   Note: look at shutil library for file copying??
        if cmd[0] == 'copy':
            # maybe append current directory onto front of filenames
            server_message = copy(cmd[1])
            print(server_message)
            server.send(server_message.encode())
        elif cmd[0] == 'rename':
            # maybe append current directory onto front of filenames
            server_message = rename(cmd[1], cmd[2])
            print(server_message)
            server.send(server_message.encode())
        elif cmd[0] == 'delete':
            # maybe append current directory onto front of filenames
            server_message = delete(cmd[1])
            print(server_message)
            server.send(server_message.encode())
        elif cmd[0] == 'ld':
            server_message = ld()
            print(server_message)
            server.send(server_message.encode())
        elif cmd[0] == 'done':
            server_message = 'done'
            print(server_message)
            server.send(server_message.encode())
            # shutdown connection with client
            server.shutdown(socket.SHUT_RDWR)
            # close server socket
            server.close()
            break

        # shutdown connection with client
        server.shutdown(socket.SHUT_RDWR)
        print("shutdown")
        # close server socket
        server.close()
        print("close")


# Function to copy a file
def copy(filename=string):
    currWorkingDir = os.getcwd()
    fullpath = currWorkingDir + "/" + filename
    copyfullpath = "COPY" + fullpath

    # do stuff for copying a file

    # return message about success
    if path.exists('copyfullpath'):
        return "File Copy Success"
    else:
        return "Error: File Copy Failed"
    print(fullpath)


# Function to rename a file
def rename(filename1=string, filename2=string):
    currWorkingDir = os.getcwd()
    fullpath1 = currWorkingDir + "/" + filename1
    fullpath2 = currWorkingDir + "/" + filename2
    print(fullpath1)
    print(fullpath2)

    #rename file
    os.rename(r'fullpath1', r'fullpath2')

    #check for existence of new filename
    if path.exists('fullpath2'):
        return "File Rename Success"
    else:
        return "Error: File Rename Failed"
    # return messages about success


# Function to delete a file
def delete(filename=string):
    currWorkingDir = os.getcwd()
    fullpath = currWorkingDir + "/" + filename
    print(fullpath)

    # do stuff to delete the file

    # return message about success
    #check for existence of new filename
    if path.exists('fullpath'):
        return "Error: File Rename Failed"
    else:
        return "File Delete Success"


# Function to get the list of files from the directory
def ld():
    currWorkingDir = os.getcwd()
    print("FIXME")
    # Do stuff to send the list from directory
    # return string of filenames in the directory
    # or message about success
    return "FIXME"


# use server_main() as the main function
if __name__ == "__main__":
    server_main()
