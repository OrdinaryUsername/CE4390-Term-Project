import socket
import os
# from os import path
# import string
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
        print(' ')
        # accept the connection request
        conn, addr = server.accept()

        data = conn.recv(1024)
        request = parse_message(data)
        if request[0] == 'Connection request':
            print('Connection requested by client...')
            packet = conn_accept()
            conn.send(bytes(str(packet), "utf-8"))


        # recieve message from client using client_message = server.recv(1024)
        data = conn.recv(1024)
        print("Recieving data....")

        # do stuff based on the message contents and protocol format (flags, etc)
        #   Note: look at os library for file management functions??
        #   Note: look at shutil library for file copying??
        user_input = parse_message(data)

        if user_input[0] == 'list':
            server_message = ld()
            conn.send(bytes(str(server_message), "utf-8"))
            print("Sending of file directory complete.")
        elif user_input[0] == 'copy':
            # maybe append current directory onto front of filenames
            server_message = copy(user_input[1])
            conn.send(bytes(str(server_message), "utf-8"))
        elif user_input[0] == 'rename':
            # maybe append current directory onto front of filenames
            server_message = rename(user_input[1], user_input[2])
            conn.send(bytes(str(server_message), "utf-8"))
        elif user_input[0] == 'delete':
            # maybe append current directory onto front of filenames
            server_message = delete(user_input[1])
            conn.send(bytes(server_message, "utf-8"))
        elif user_input[0] == 'done':
            print('Client has requested to end the session...')
            server_message = 'done'
            # print(server_message)
            conn.send(bytes(server_message, "utf-8"))
            # close server socket
            print('Shutting down session...')
            conn.close()
            print("Session shutdown complete.")
            break

        # shutdown connection with client
        print("Closing connection with client...")
        # close server socket
        conn.close()
        print("Connection with client closed.")
        print(' ')



# Function to parse a message
def parse_message(data):
    request = []
    decoded_data = data.decode("utf-8")
    msg = decoded_data.replace('\r', '')
    message = msg.split('\n')

    if message[0] == '1':
        if message[1] == '1':
            request.append('Connection request')
    elif message[0] == '2':
        if message[1] == '3':
            request.append('list')
        elif message[1] == '4':
            request.append('copy')
            request.append(message[2])
        elif message[1] == '5':
            request.append('rename')
            filenames = message[2].split(',')
            request.append(filenames[0])
            request.append(filenames[1])
        elif message[1] == '6':
            request.append('delete')
            request.append(message[2])
        elif message[1] == '7':
            request.append('done')

    return request


# Function to format the message to be sent
def message_format(status):
    mtype = str(status[0])
    code = str(status[1])
    if status[3] != '':
        filenames = str(status[2]) + ',' + str(status[3])
    else:
        filenames = str(status[2])
    payload = str(status[4])
    length = str(len(mtype + '\n' + code + '\r\n' + filenames + '\n' + '\r\n\r\n' + payload))
    return mtype + '\n' + code + '\r\n' + filenames + '\n' + length + '\r\n\r\n' + payload

#function for accepting a connection
def conn_accept():
    print("Connection accepted")
    status = []
    # type 1 for connection
    status.append('1')
    # code 2 for connection accepted
    status.append('2')
    # set all other fields to empty
    status.append('')
    status.append('')
    status.append('')
    # return "Connection accpeted"
    return message_format(status)

# Function to copy a file
def copy(filename):
    print('Copying file ' + filename + '...')
    status = []
    cwd = os.getcwd()
    fullpath = cwd + "/" + filename
    fname = filename.split('.')
    new_filename = fname[0] + '(1).' + fname[1]

    i = 1
    while os.path.exists(new_filename):
        new_filename = fname[0] + '(' + str(i) + ').' + fname[1]
        i = i + 1

    new_fullpath = cwd + "/" + new_filename
    if os.path.exists(fullpath):
        shutil.copy2(fullpath, new_fullpath)
        print("Copying of file " + filename + " complete.")
        # type 3 for response
        status.append('3')
        # code 11 for command success
        status.append('11')
        # set all other fields to empty
        status.append('')
        status.append('')
        status.append('')
        # return "File Copy Success"
        return message_format(status)
    else:
        print("ERROR: File " + filename + " does not exist!")
        # type 4 for error
        status.append('4')
        # code 8 for file does not exist
        status.append('8')
        # set filename for file that does not exist
        status.append(filename)
        # set all other fields to empty
        status.append('')
        status.append('')
        # return "Error: File " + filename + " does not exist!"
        return message_format(status)


# Function to rename a file
def rename(filename1, filename2):
    print('Renaming file ' + filename1 + ' to ' + filename2 + '...')
    status = []
    cwd = os.getcwd()
    fullpath1 = cwd + "/" + filename1
    fullpath2 = cwd + "/" + filename2

    if os.path.exists(fullpath1):
        if os.path.exists(fullpath2):
            print("ERROR: File " + filename2 + " already exists!")
            # Type 4 for error
            status.append('4')
            # code 9 for file name already exists
            status.append('9')
            # set filename for file that already exists
            status.append(filename2)
            # set all other fields to empty
            status.append('')
            status.append('')
            # return 'ERROR: File ' + filename2 + ' already exists!'
            return message_format(status)
        else:
            # rename file
            os.rename(fullpath1, fullpath2)
            print("Renaming of file " + filename1 + " to " + filename2 + " complete.")
            # Type 3 for response
            status.append('3')
            # code 11 for command success
            status.append('11')
            # set all other fields to empty
            status.append('')
            status.append('')
            status.append('')
            # return "File Rename Success"
            return message_format(status)
    else:
        print("ERROR: File " + filename1 + " does not exist!")
        # Type 4 for error
        status.append('4')
        # code 8 for file does not exist
        status.append('8')
        # set filename for file that does not exist
        status.append(filename1)
        # set all other fields to empty
        status.append('')
        status.append('')
        # return "ERROR: File " + filename1 + " does not exist!"
        return message_format(status)


# Function to delete a file
def delete(filename):
    print('Deleting file ' + filename + '...')
    status = []
    cwd = os.getcwd()
    fullpath = cwd + "/" + filename

    if os.path.exists(fullpath):
        os.remove(fullpath)
        print("Deletion of file " + filename + " complete.")
        # type 3 for response
        status.append('3')
        # code 11 for command success
        status.append('11')
        # set all other fields to empty
        status.append('')
        status.append('')
        status.append('')
        # return "File delete success"
        return message_format(status)
    else:
        print("ERROR: File " + filename + " does not exist!")
        # Type 4 for error
        status.append('4')
        # code 8 for file does not exist
        status.append('8')
        # set filename for file that does not exist
        status.append(filename)
        # set to be empty
        status.append('')
        status.append('')
        # return "ERROR: File " + filename + " does not exist!"
        return message_format(status)


# Function to get the list of files from the directory
def ld():
    print('Client requesting file directory...')
    status = []
    cwd = os.getcwd()
    directory = os.listdir(cwd)
    # Type 3 for response
    status.append('3')
    # code 11 for command success
    status.append('12')
    status.append('')
    status.append('')
    status.append(directory)
    print(status[4])
    # return directory
    return message_format(status)


# use server_main() as the main function
if __name__ == "__main__":
    server_main()
