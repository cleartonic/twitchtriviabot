from src.bot import Trivvy
from src.configuration import Configuration
from src.connection import Connection
from src.commander import Commander
from mocks import socket
# import socket

configFile = 'mocks/config.txt' # 'config.txt'
config = Configuration(configFile)
socket = socket.socket()
connect_to = config.get_connection_constants()
twitch_connection = Connection(connect_to, socket)
route_commander = Commander(config.get_admins(), twitch_connection)
app = Trivvy(twitch_connection, route_commander)
app.run()
