from src.connection import Connection
from src.commander import Commander
from concurrent.futures import ThreadPoolExecutor
import time

class Trivvy:

    def __init__(self, connection, commander):
        self.connection = connection
        self.router = commander

    def run(self):
        with ThreadPoolExecutor(max_workers=2) as e:
            e.submit(self.connection.scan_for_messages)
            e.submit(self.router.listen_for_commands)
