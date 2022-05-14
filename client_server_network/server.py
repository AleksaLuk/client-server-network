

#####.....Server.....#####

#####.....Step1 is Import Socket Module.....#####
import socket

#####.....Step2 is Create a Socket Object and get host name.....#####
s = socket.socket()
host = socket.gethostname()
print("Socket successfully created")

#####.....Step3 is Reserve a port on Computer.....#####
port = 56789

#####.....Step4 is to bind the port.....#####
# the bind takes two requests the IP and the port. we leave the IP blank so that it can listen to other request
s.bind(('', port))
print(f'socket binded to port{port}')

#####.....Step5 is to put the socket into a listening mode.....#####
s.listen(5)
print("socket is listening")

#####.....Step6 is a Loop that keeps running until an interruption occurs....#####
while True:
    c, addr = s.accept()
    print("Got connection from", addr)
    message = ("Thank you for connecting")
    c.send(message.encode())
    c.close()
