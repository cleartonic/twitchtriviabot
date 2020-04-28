from src.bot import Trivvy
from src.configuration import Configuration
from src.connection import Connection
from test import socket
# import socket

connect_to = Configuration('config.txt').get_connection_constants()
twitch_connection = Connection(connect_to, socket)
app = Trivvy(twitch_connection)
app.run()
