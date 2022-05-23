# Group Project - Client/Server Network Application
Library for communicating messages between a client server network

## Cloning the repository

```shell
git clone -c https://gitlab.csc.liv.ac.uk/sgalukow/client_server_network.git
```

## Installing dependencies

```shell
pip install -r requirements.txt
```

## Installing the repository
(After installing dependencies)

```shell
python setup.py install
```

## Running the application
### LOCAL
Local server is required to be running before client attempts to connect.
1. Run main-server.py (or custom server.py implementation)
2. Run main-client.py (or custom client.py implementation)

### REMOTE (AWS)
An EC2 instance has been set up with the server running as an always-on service. The user will not have to run their own server.
1. Set host = 18.135.93.207
2. Set port = 80
3. Run main-client.py (or custom client.py implementation)

## Stopping the application
The client is required to disconnect from server so the server can gracefully close client connection before the server is stopped. The client will disconnect if the script comes to an end naturally. If a script keeps the connection in a loop, the client script must be stopped first.
1. Stop main-client.py
2. Stop main-server.py (local only)

## Examples

### Through code
#### server.py
```Python
import socket
from client_server_network.server import Server

SERVER_HOST = socket.gethostname()
SERVER_PORT = 5432

s = Server(SERVER_HOST, SERVER_PORT)
s.recvall()
```

#### client.py

```Python
from client_server_network.client import Client
from client_server_network.interface import UserInterface
import socket

SERVER_HOST = socket.gethostname()
SERVER_PORT = 5432

c = Client(SERVER_HOST, SERVER_PORT)
c.connection()
data = {"Hello": "World"}
c.transfer_object("json", data, encrypt=True)
```


### Through config

#### server.py
```Python
import socket
import configparser
from client_server_network.server import Server

config = configparser.ConfigParser()
config.read("config.cfg")
host = config['LocalServer']['host']
SERVER_HOST = socket.gethostname() if host.lower() == "localhost" else host
SERVER_PORT = config['LocalServer'].getint('port')

s = Server(SERVER_HOST, SERVER_PORT)
s.recvall()
```

#### client.py
```Python
from client_server_network.interface import UserInterface

ui = UserInterface()
ui.run(config="Config.cfg")
```
Configuration file:
![Screenshot](images/config.png)

### Through GUI (Tkinter)

#### server.py
```Python
from client_server_network.client import Client
from client_server_network.interface import UserInterface
import socket

SERVER_HOST = socket.gethostname()
SERVER_PORT = 5432

c = Client(SERVER_HOST, SERVER_PORT)
c.connection()
```

#### client.py
```Python
from client_server_network.interface import UserInterface
import socket

SERVER_HOST = socket.gethostname()
SERVER_PORT = 5432

ui = UserInterface(SERVER_HOST, SERVER_PORT)
ui.run()
```


### GUI
![Screenshot](images/user_interface.png)

### Client Log
![Screenshot](images/gui_log_output.png)

### Server Log
![Screenshot](images/server_log_output.png)