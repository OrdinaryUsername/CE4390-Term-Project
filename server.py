import socket
import os
from os import path
import string
import shutil


def server_main(server=socket):
    print('------------------------------------------------------------------')
    # create and initialize server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set the server's ip address
    host = '10.0.0.1'
    print('Server Host name: ' + socket.gethostname())
    # set the port number for the host
    port = 49159
    # bind the socket using the ip address and port number
    server.bind((host, port))
    # listen for connection requests
    server.listen(1000000)
    print('Listening on IP: ' + host + ', ' + str(port) + '\n')


    while 1:
        # accept the connection request
        conn, addr = server.accept()
        print("Connection accepted")
        # recieve message from client using client_message = server.recv(1024)
        data = conn.recv(1024)
        print("Recieving data....")
        # decode server message using client_message.decode()
        cmd = data.decode("utf-8")
        print("Decoding data....")

        if cmd == 'list':
            print('Client requesting file directory...')
            server_message = ld()
            print('Sending directory....')
            conn.send(bytes(str(server_message), "utf-8"))
        # do stuff based on the message contents and protocol format (flags, etc)
        #   Note: look at os library for file management functions??
        #   Note: look at shutil library for file copying??
        userInput = cmd.split(' ')
        
        if userInput[0] == 'copy':
            # maybe append current directory onto front of filenames
            print('Attempting to copy file' + userInput[1] + '...')
            server_message = copy(userInput[1])
            print(server_message)
            conn.send(bytes(str(server_message), "utf-8"))
        elif userInput[0] == 'rename':
            print('Attempting to rename file' + userInput[1] + 'to ' + userInput[2])
            # maybe append current directory onto front of filenames
            server_message = rename(userInput[1], userInput[2])
            print(server_message)
            conn.send(bytes(str(server_message), "utf-8"))
        elif userInput[0] == 'delete':
            print('Attempting to delete file' + userInput[1] + '...')
            # maybe append current directory onto front of filenames
            server_message = delete(userInput[1])
            print(server_message)
            conn.send(bytes(server_message, "utf-8"))
        elif userInput[0] == 'done':
            print('Client has requested to close connection...')
            server_message = 'done'
            #print(server_message)
            conn.send(bytes(server_message, "utf-8"))
            # shutdown connection with client
            print('Closing connection with client')
            # close server socket
            print('Shutting down server...')
            conn.close()
            break

        # shutdown connection with client
        print("Closing connection with client...")
        # close server socket
        conn.close()
        print("Re-establising connection")


# Function to copy a file
def copy(filename):
    currWorkingDir = os.getcwd()
    fullpath = currWorkingDir + "/" + filename
    fname = filename.split('.')
    newfileName = fname[0] + '(1).' + fname[1]

    i = 1
    while os.path.exists(newfileName):
        newfileName = fname[0] + '(' + str(i) + ').' + fname[1]
        i = i + 1

    newLocation = currWorkingDir + "/" + newfileName
    if os.path.exists(fullpath):
        shutil.copy2(fullpath, newLocation)
        return "File Copy Success"
    else:
        return "Error: File " + filename + " does not exist!"


# Function to rename a file
def rename(filename1, filename2):
    currWorkingDir = os.getcwd()
    fullpath1 = currWorkingDir + "/" + filename1
    fullpath2 = currWorkingDir + "/" + filename2
    print(fullpath1)
    print(fullpath2)
    
    if os.path.exists(fullpath1):
        if os.path.exists(fullpath2):
            return 'ERROR: File ' + filename2 + ' already exists!'
        else:
            #rename file
            os.rename(fullpath1, fullpath2)
            return "File Rename Success"
    else:
        return "ERROR: File " + filename1 + " does not exist!"
 
# Function to delete a file
def delete(filename):
    currWorkingDir = os.getcwd()
    fullpath = currWorkingDir + "/" + filename
    print(fullpath)
    if os.path.exists(fullpath):
      os.remove(fullpath)
      return "File delete success"
    else:
      return "ERROR: File " + filename + " does not exist!"
      
    


# Function to get the list of files from the directory
def ld():
    currWorkingDir = os.getcwd()
    directory = os.listdir(currWorkingDir)
    return directory


# use server_main() as the main function
if __name__ == "__main__":
    server_main()