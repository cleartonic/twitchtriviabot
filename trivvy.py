from src.bot import Trivvy
from src.configuration import Configuration
from src.connection import Connection
from test.mocks import socket
# import socket

log = print
configFile = 'test/mocks/config.txt' # 'config.txt'
connect_to = Configuration(configFile, log).get_connection_constants()
twitch_connection = Connection(connect_to, socket, log)
app = Trivvy(twitch_connection)
app.run()
