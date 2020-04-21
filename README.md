# Twitch Trivia Bot

trivia bot modified for [Outpost 13](https://www.twitch.tv/outpost13)

## Instructions for Channel Admins and Mods
This assumes no development or shell experience. Use your own way if you have opinions and preferences.

### MacOS Catalina first-time install:

 1. Follow this link to [Install Atom](https://atom.io/)

 1. Join [GitHub](https://github.com/join)

 ###### Open the Terminal, press `return` after copy-pasting each of the following commands:

 ###### Install [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and Xcode
 1.  `git --version` - Say yes to Xcode popup
 ###### Install [Homebrew](https://brew.sh/)
 1. `mkdir homebrew && curl -L https://github.com/Homebrew/brew/tarball/master | tar xz --strip 1 -C homebrew`
 ###### Install [Python](https://docs.python-guide.org/starting/install3/osx/)
 1. `brew install python`
 ###### Install [Pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)
 1. `pip3 install pandas`
 ###### Point the terminal to the right python
 1. `atom ~/.profile`
  - copy/paste this:
  ```
  export PATH="/usr/local/opt/python/libexec/bin:$PATH"
  ```
  - save and close atom.
 1. `atom ~/.zshrc`
  - copy/paste this:
  ```
  alias python=/usr/local/bin/python3
  alias Python=/usr/local/bin/python3
  ```
  - save and close atom.

 1. `source ~/.zshrc && source ~/.profile`

 ###### Make a cozy home for the bot
 1. `mkdir TwitchBots`

 ###### If you have installed before on this machine, follow from here:

 1. `cd TwitchBots`
 1. `git clone https://github.com/IanDCarroll/twitchtriviabot.git`
 1. Give yourself a high five you're installed!

### Running the Bot on Twitch:

 1. `cd TwitchBots/twitchtriviabot`
 1. `atom config.txt`
  - modify these configuration settings so it can log on

  ```
  [Admin Settings]
  admins = <A_TWITCH_ACCOUNT_USERNAME_WHO_WILL_CONTROL_THE_BOT>

  [Bot Settings]
  host = irc.twitch.tv
  port = 6667
  nick = <A_TWITCH_ACCOUNT_USERNAME_THE_BOT_WILL_USE>
  pass = oauth:1awesomerandompassofthislength
  chan = #<THE_CHANNEL_THE_BOT_WILL_RUN_ON>
  ```
  - Save via `<CMND> s`
  - Note: `chan` needs a `#` in front of the name as shown.
  - Also Note: you need to be logged in to twitch under the bot's name to get a pass.
  - Also Also Note: You can [get that pass (oauth token) from here](https://twitchapps.com/tmi/).
  - Finally Note: oauth passes expire. You'll need a new one from time to time.

 1. `python twitchtriviabot.py`
 1. You should see the terminal giving you info on what the bot sees from chat, and you should also see a logged-in message in chat from the bot.

### Stopping the Bot:

 - in the terminal, type `<CTRL> c`
