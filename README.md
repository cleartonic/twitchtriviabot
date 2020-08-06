# Twitch Trivia Bot [![Build Status](https://travis-ci.com/Coding-Koans/Trivvy.svg?branch=master)](https://travis-ci.com/Coding-Koans/Trivvy)

trivia bot modified for [Outpost 13](https://www.twitch.tv/outpost13)

## Instructions for Channel Admins and Mods
This assumes no development or shell experience. Use your own way if you have opinions and preferences.

### First-time install:

 - Follow this link to [Install Atom](https://atom.io/)

 - Join [GitHub](https://github.com/join)

 ###### MacOS: Open the Terminal, press `return` after copy-pasting each of the following commands:
 ###### Windows: Install and Open [Git Bash](https://gitforwindows.org/), press `enter` after copy-pasting each of the following commands:
 ###### Install [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) (and Xcode if on MacOs)
 -  `git --version` (MacOS: Say yes to Xcode popup) This should give you a version number if git is installed, otherwise google how to install git.
 ###### MacOS only: Install [Homebrew](https://brew.sh/)
 - `mkdir homebrew && curl -L https://github.com/Homebrew/brew/tarball/master | tar xz --strip 1 -C homebrew`
 ###### Install [Python](https://docs.python-guide.org/starting/install3/osx/)
 - MacOS: `brew install python`
 - Windows:
    - use the [full install](https://docs.python.org/3/using/windows.html#windows-full)
    - Be sure to check "Add Python 3.X to Path"
    - Be sure to remove the max_path limitation before completing the install.
 ###### Install [Pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)
 - MacOS: `pip3 install pandas`
 - Windows: `py -m pip install pandas`
 ###### MacOS only: Point the terminal to the right python
 - `atom ~/.profile`
   - copy/paste this:
   ```
   export PATH="/usr/local/opt/python/libexec/bin:$PATH"
   ```
   - save and close atom.
 - `atom ~/.zshrc`
   - copy/paste this:
   ```
   alias python=/usr/local/bin/python3
   alias Python=/usr/local/bin/python3
   ```
   - save and close atom.
 - `source ~/.zshrc && source ~/.profile`
 ###### Make a cozy home for the bot
 - `mkdir TwitchBots`
 ###### Clone this repo
 - `cd TwitchBots`
 - `git clone https://github.com/IanDCarroll/twitchtriviabot.git`
 - Give yourself a high five you're installed!

### Getting updates:
 - `cd TwitchBots`
 - `git pull`

### Running the tests:

 - MacOS in terminal: `python -m unittest discover`
 - Windows in Powershell: `py -m unittest discover`

### Running the Bot on Twitch:

 - `cd TwitchBots/twitchtriviabot`
 - `atom config.txt`
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
   - Also Also Also Note: usernames must be typed into the config in all lower case (and be spelled correctly!)
   - Alos Also Alos Also Note: Atom doesn't auto-save by default - Make sure to save via `<CMND> s`
   - Finally Note: oauth passes expire. You'll need a new one from time to time.

 - MacoOS in terminal: `python twitchtriviabot.py`
 - Windows in Powershell: `py twitchtriviabot.py` (Git Bash doesn't show print statements in real-time)
 - You should see the terminal giving you info on what the bot sees from chat, and you should also see a logged-in message in chat from the bot.

### Common admin chat commands:

- `!triviastart` - starts trivia
- `!stop` - kills the bot's connection to twitch, and stops trivia

### Stopping the Bot:

 - in the terminal, type `<CTRL> c`
