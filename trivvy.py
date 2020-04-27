from src.bot import Trivvy
from src.connection import Connection
from test import socket
# import socket

twitch_connection = Connection(socket)
app = Trivvy(twitch_connection)
app.run()
