import threading
import socket


#https://www.youtube.com/watch?v=3UOyky9sEQY
#this video was used for reference in making this chat client thingy

host = '127.0.0.1' #this is local host
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()


clients = [] #holds client info
nicknames = [] #client chosen nickname

def broadcast(message):
    for client in clients:
        client.send(message) #sends a message to all clients connected
        
def handle(client):
    while True:
        try:
            if message != 'bye':
                message = client.recv(1024)
                broadcast(message)
        except:
            index = clients.index(client) #needed to remove client
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname) #takes client who lefts nickname out of list
            break
            

def receive(): #main method
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        clients.append(client)
        
        print(f'Name of the client is {nickname}!')
        broadcast(f'{nickname} just joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))
        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
        
print("The server is listening........")
receive()