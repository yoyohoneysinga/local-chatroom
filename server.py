import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1", 12345))
s.listen(5)

clients = []

def broadcast(message, sender_name):
    full_message = "{}: {}".format(sender_name, message)
    for client_socket, _ in clients:
        if client_socket != sender_name:
            try:
                client_socket.send(full_message.encode())
            except:
                remove_client(client_socket)

def remove_client(client_socket):
    for idx, (sock, _) in enumerate(clients):
        if sock == client_socket:
            clients.pop(idx)
            break

def handle_client(c):
    name = c.recv(1024).decode()
    clients.append((c, name))
    while True:
        message = c.recv(1024).decode()
        if not message:
            break
        print("{}: {}".format(name, message))
        broadcast(message, name)

    remove_client(c)
    c.close()

while True:
    c, addr = s.accept()
    print("Got connection from", addr)
    t = threading.Thread(target=handle_client, args=(c,))
    t.start()