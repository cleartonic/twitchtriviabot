class Log:
    config_loading = 'Loading config...'
    config_success = 'Configuration is Go'
    config_failure = 'Config not loaded! Check config file and reboot bot'

    connect_loading = 'Attempting connection...'
    connect_pass = 'Sending Oauth Token'
    connect_nick = 'Sending Bot Name'
    connect_join = 'Sending Channel Join request'
    connect_hi = 'Sending a good morning greeting to the chat'
    connect_complete = '*** All systems are Go. Trivvy Bot Launched! ***'
    connect_failure = 'Connection failed. Check config settings and reload bot.'
    connect_pong = 'pong sent'

    def connect_response(username, response_body):
        return f'Chat Message From: {username} : {response_body}'
