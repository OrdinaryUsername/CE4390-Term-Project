import socket
import os

def server_main(server=socket):
    #create and initialize server socket
    server.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #get the server's ip address
    ip = socket.gethostbyname(socket.gethostname())
    #get the port number for the host
    port = int(input('Enter desired port: '))
    #bind the socket using the ip address and port number
    server.s.bind((ip,port))
    #listen for connection requests
    server.s.listen(100)

    print('Listening on IP: '+ip+', '+str(port))

    while 1:
        #accept the connection request
        server.s.accept()
        #recieve message from client using client_message = server.recv(1024)
        #   Note: may need to use while 1 loop to get all of the message contents
        #   and break when no longer recieving anything
        #decode server message using client_message.decode()
        #do stuff based on the message contents and protocol format (flags, etc)
        #   Note: look at os library for file management functions??
        #   Note: look at shutil library for file copying??
        #send message to the client using server.send(server_message.encode())
        #shutdown connection with client
        server.shutdown(socket.SHUT_RDWR)
        #close server socket
        server.close()

#use server_main() as the main function
if __name__ == "__main__":
    server_main()