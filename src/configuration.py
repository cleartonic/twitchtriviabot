import configparser

class Configuration:
    COMMANDLIST = ["!triviastart","!triviaend","!top3","!hint","!bonus","!score","!next","!stop","!loadconfig","!backuptrivia","!loadtrivia","!creator"]

    def abruptly_end_the_app():
        exit()

    def __init__(self, config_file):
        print("Loading config...")
        try:
            config = configparser.ConfigParser()
            config.read(config_file)
            self.trivia_filename = config['Trivia Settings']['trivia_filename']
            self.trivia_filetype = config['Trivia Settings']['trivia_filetype']
            self.trivia_questions = int(config['Trivia Settings']['trivia_questions'])
            self.trivia_hinttime_1 = int(config['Trivia Settings']['trivia_hinttime_1'])
            self.trivia_hinttime_2 = int(config['Trivia Settings']['trivia_hinttime_2'])
            self.trivia_skiptime = int(config['Trivia Settings']['trivia_skiptime'])
            self.trivia_questiondelay = int(config['Trivia Settings']['trivia_questiondelay'])
            self.trivia_bonusvalue = int(config['Trivia Settings']['trivia_bonusvalue'])

            admin1 = config['Admin Settings']['admins']
            self.admins = admin1.split(',')

            self.HOST = str(config['Bot Settings']['HOST'])
            self.PORT = int(config['Bot Settings']['PORT'])
            self.NICK = config['Bot Settings']['NICK']
            self.PASS = config['Bot Settings']['PASS']
            self.CHAN = config['Bot Settings']['CHAN']
        except:
            print("Config not loaded! Check config file and reboot bot")
            Configuration.abruptly_end_the_app()

    def set_admins(config):
        separator = ','
        admin_list = config['Admin Settings']['admins'].split(separator)
        return [admin.strip() for admin in admin_list]

    def get_connection_constants(self):
        return {
            'irc_url': self.HOST,
            'irc_port': self.PORT,
            'bot_name': self.NICK,
            'oauth_token': self.PASS,
            'channel': self.CHAN
        }
