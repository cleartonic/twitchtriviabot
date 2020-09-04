from src.bot import Trivvy
from src.startup import Configuration, Option_Worker
from src.connection import Connection
from src.commander import Commander
from src.commands import all
import sys

def main(user_input):
    worker = Option_Worker(user_input)
    config_file, socket = worker.setWithOptions()

    config = Configuration(config_file)
    connect_to = config.get_connection_constants()
    twitch_connection = Connection(connect_to, socket)
    route_commander = Commander(all.commands(), config.get_admins(), twitch_connection)
    app = Trivvy(twitch_connection, route_commander)
    app.run()

if __name__ == "__main__":
    main(sys.argv[1:])
