import socket
import threading
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 12345))

name = input("Enter your name: ")
s.send(name.encode())

def receive_messages():
    while True:
        try:
            response = s.recv(1024).decode()
            sender_name, message = response.split(": ", 1)
            if sender_name != name:
                print(response)
                sys.stdout.write(f"{name}: ")
                sys.stdout.flush()
        except:
            s.close()
            print("Connection closed.")
            break

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

while True:
    message = input()
    s.send(message.encode())
    if message == "exit":
        break

s.close()