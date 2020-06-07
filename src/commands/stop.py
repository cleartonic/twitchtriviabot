from src.messages import Chat

class stop:
    command = "!stop"
    validate = [ "admin_only" ]

    def tuple():
        return (stop.command, stop.graceful_shutdown, stop.validate)

    def graceful_shutdown(connection, _message):
        connection.send(Chat.good_night)
        connection.keep_IRC_running = False
