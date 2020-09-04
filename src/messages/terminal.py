from src.helpful.mr_clean import Mr

class Log:
    options_bad = "\nWhoa there honcho! Somthing you typed in is not an option yet"
    options_too_many = "\nWhoa there honcho! You can either go live or do a dry run. Not both."
    options_too_few = "\nWhoa there honcho! Do you want to go live or do a dry run?"

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

    def log_options(options):
        options_menu = ""
        for option in options:
            options_menu += f"\t{Mr.title(option)}:\tTrivvy.py --{option}\n"
        return options_menu

    def connect_response(username, response_body):
        return f'Chat Message From: {username} : {response_body}'

    def question_load_problem(message):
        one = f'\n\tLuke, we\'ve got a malfunction in fire control...\n\n{message}\n'
        two = 'Better go fix the triviaset.csv file before trying to shoot this thing off'
        return one + two

    def bad_admin(username, command):
        return f"{username} tried to issue a {command} command, but they are not on the admin list."

    def good_admin(username, command):
        return f"The bot has recieved a {command} command issued by {username}."

    def good_command(username, command):
        return f"The bot has recieved a non-admin {command} command issued by {username}."

    def in_progress(username, command):
        return f"{username} issued a {command} command, but that command is already running."
