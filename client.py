import socket
import shutil

def client_main(client = socket):
    #initialize client cocket
    client.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #set the client's target ip address(server ip address)
    client.target_ip = input('Enter target ip: ')
    #set the client's target port(server port)
    client.target_port = input('Enter target port: ')
    #connect the client to the server
    client.s.connect((client.target_ip,int(client.target_port)))
    
    #listen
    while 1:
        print 'Instruction List:'
        print '"copy[filename]" retrieves a copy of a file from the server.'
        print '"rename[filename, newFileName]" renames a file from the server.'
        print '"delete[filename]" deletes a file on the server.'
        print '"ld" lists file directory on server.'
        print '"done" quits program.'
        
        #get the user's command
        cmd = input('Enter a command: ')
        if cmd == 'ld':
            sl()
            break
        else if cmd == 'copy':
            
        #Convert command to protocol format for client_message
        #send command to server using client.s.send(client_message.encode())
        #recieve message from server using server_message = client.s.recv(1024)
        #   Note: may need to use while 1 loop to get all of the message contents
        #   and break when no longer recieving anything
        #decode server message using server_message.decode()
        #   Note: check out shutil library for file copying??

        #shut down the connection
        client.s.shutdown(socket.SHUT_RDWR)
        #close the socket
        client.s.close()
        #open the socket
        client.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #connect to the server
        client.s.connect((client.target_ip,int(client.target_port)))

    #shut down the connection
    client.s.shutdown(socket.SHUT_RDWR)
    #close the socket
    client.s.close()
    #open the socket
    client.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


#use client_main() as the main function
if __name__ == "__main__":
    client_main()