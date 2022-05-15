


# Import Socket Module
import socket

# Create a Socket Object and get host name
s = socket.socket()
host = socket.gethostname()
print("Socket successfully created")

# Reserve a port on Computer
port = 56789

# Bind the port
s.bind(('', port))
print(f'socket binded to port{port}')

# Put socket into a listening mode
s.listen(5)
print("socket is listening")

# Loop that keeps running until an interruption occurs
while True:
    c, addr = s.accept()
    print("Got connection from", addr)
    message = ("Thank you for connecting")
    c.send(message.encode())
    c.close()
