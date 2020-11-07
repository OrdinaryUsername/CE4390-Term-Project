import socket
import shutil

class Client:

    def main(client):
        #initialize client cocket
        client.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #set the client's target ip address(server ip address)
        client.target_ip = input('Enter ip: ')
        #set the client's target port(server port)
        client.target_port = input('Enter port: ')
        #connect the client to the server
        client.s.connect((client.target_ip,int(client.target_port)))

        #listen
        while 1:
            #get the user's command
            cmd = input('Enter a command: ')
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

client = Client()
