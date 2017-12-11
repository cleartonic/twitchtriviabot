# Twitch Trivia Bot

Twitch Trivia Bot (TTB) is a Python script to run a trivia session in Twitch chat. The bot will load a quiz set, run a session of trivia, assign a winner and save scores dynamically. 

![img](https://i.imgur.com/m0lVwSI.png)


# Features:
+ Loads Excel (xls, xlsx) and csv files for trivia questions, and answers, and handles any amount of questions (limited only by Excel/csv constraints)
+ Dynamically selects a random set of questions from the pool of questions
+ Automatically asks questions, generates dynamic hints, and skips questions based on configurable time delays
+ BONUS mode, allowing for extra points to be rewarded
+ Stores trivia performance over multiple sessions, allowing participants to retrieve scores at any time
+ Trivia sessions cut short by bot disconnect can be reloaded via actively created backups

# Setup
The latest Python 3 install is required for this bot. You will need to install Python 3 to be able to run. One can either use standard Python 3 distribution with IDLE, or use something like the Anaconda distribution with Spyder (what I use).

Three files are critical for the bot to run. Download “triviaset.csv”, “twitchtriviabot.py”, and “config.txt”, and place them in the same directory. 

+ “twitchtriviabot.py” does not need to be reconfigured. This will be loaded via Python console, and will connect to Twitch chat.
A trivia set file (either csv, xls or xlsx) needs to be set up (more on this below). Default with this package is ‘triviaset.csv’ with the appropriate columns pre-identified. 
+ “config.txt” needs to be configured. All inputs should be **without** brackets (defaults have brackets where input is necessary.) Open this file in a text editor.
  + Under “Trivia Settings”, the first two filename & filetype should match the trivia set file (default is ‘triviaset.csv’.) All numberic fields here are default and don’t need to be adjusted, and represent seconds:
    + Trivia_questions = # of questions for the trivia session to include. This will be pulled randomly for the trivia list from csv/xls/xlsx. 
    + Trivia_hinttime_1 and 2 = Time delay before hints 1 and 2 are supplied
    + Trivia_skiptime = Time delay before question is skipped
    + Trivia_questiondelay = Time delay after question is answered before next question is asked
    + Trivia_bonusvalue = Value assigned to BONUS round questions
  + Under “Admin Settings”, all admins need to be added here. This must be set up in advance in this version, there is no !addadmin [x] command. These need to be separated by exact twitch usernames with commas with no spaces between commas, specifically:
    + E.g., admins = salmon
    + E.g., admins = salmon,tuna
  + Under “Bot Settings”, all fields must be specifically identified:
    + Host = default irc.twitch.tv
    + Port = default 6667 (for twitch)
    + Nick = username for the bot
    + Pass = password in “oath:xxxxxx... “ format. Retrieve from https://twitchapps.com/tmi/ for the bot
    + Chan = twitch channel to connect the bot to, where trivia will take place

To set up triviaset.csv properly, consider the following:
5 headers in this release are specified: ‘Topic/Game, ‘Question’, ‘Answer’, ‘Answer 2’, ‘Creator’. Keep them in this order.
Fill out row by row each question, filling in topic/game, and at least 1 Answer column. Creator is not required. 
When saving the file:
+ If saving as a csv, the file format must be formatted as **CSV UTF-8**. 
+ If saving as an xls or xlsx, then **config.txt must be changed to the matching filetype**. (if you have Excel or can export from Google Sheets, this is recommended for ease of use with formatting). 

After running trivia, a few files will be generated:
+ Userscores.txt - User scores will be saved here. Do not touch this, unless a score needs to be manually adjusted. For each user that has guessed a correct answer, an entry will be made, reporting three numbers. [x,y,z], where x = total session points, y = total trivia points (all games), and z = total wins (all games) per participant. 
+ /backup/ - three backup files will be generated for reloading purposes in case of preemptive bot termination from the server.

# Running the bot

Once both the triviaset and config.txt are set up, the only thing that needs to happen is loading the python script (‘twitchtriviabot.py’) into a Python console and running the script. The initial connection to Twitch should look something like:

![img](https://i.imgur.com/Ds1TL8M.png "img")

From here, you can monitor the bot’s activity. All user responses in the Twitch channel will appear in the console. Each question’s answer will appear in the console. 

This script is an infinite loop, so in order to stop, either use the !stop command in chat, or manually kill the program. As stated earlier, active trivia sessions are backed up upon each answered question, and mid-game sessions can be reloaded, in case something goes wrong. 

# Misc. Functionalities

### Hints and question timing 

All timings can be manually adjusted in config.txt. By default, after a question is asked, automatically generated hints will trigger at 30 seconds and 60 seconds. At 90 seconds, the question will be skipped. After the specified session question limit is hit, the game will end, and a winner will be assigned. If for whatever reason a timing adjustment needs to be made within a game, config.txt can be updated, and the !loadconfig command will loads the new timings. 
+ The first hint replaces 2 out of 3 characters in the answer with “_”
+ The second hint replaces all vowels with “_”

### BONUS

Bonus can be activated by an admin via !bonus command. Bonus mode makes questions worth more points, default 3 points (configurable in config.txt). Can be toggled on/off at any time. 


### Reload a prior pre-emptively terminated session

If for whatever reason the bot is disconnected from the server due to a bot program error or a Twitch connection issue, simply rerun the bot in the Python console, and use the command !loadtrivia in Twitch chat. The prior game will reload.  Do not use !loadtrivia after using !triviastart- the !loadtrivia command will automatically start trivia with the prior session. 



# Commands
Some commands are available only during active trivia sessions.

#### Admin only:
+ !triviastart - Begins a new trivia round with conditions specified in ‘config.txt’
+ !triviaend - Ends the trivia round & assigns a win. 
+ !loadconfig - Reloads ‘config.txt’ at any time. During a trivia round, this affects hint/question waiting times.
+ !backuptrivia - Backs up current trivia round in /backup/ directory. This is a manual command to backup, but a backup is created every time a question is answered, so it’s largely unnecessary. 
+ !loadtrivia - Loads a trivia round from the backup. Use this upon loading the bot, and the backup session will be loaded and trivia will begin. Do not use this after using “!triviastart”. 
+ !next - Skips to the next question. All questions will automatically lapse after enough time specified in ‘config.txt’, but this allows for manually skipping.
+ !hint - Reposts the latest hint. Hints are given at specified intervals from ‘config.txt’
+ !bonus - Switches questions to bonus mode (toggle on/off)
+ !stop - Severs the bot connection. 

#### All users:
+ !score - Reports user’s score (reports session score, total score for all trivia, and total wins for all trivia)
+ !top3 - Report the top 3 point holders for the session
+ !creator - Reports the creator of the question 

# Future release requests
+ Tied game functionality
+ Complex question pulling algorithm (potentially based on game/another grouping)
+ Enable auto-bonus when X turns away from completing a session
+ New-age interface (long term)

# Credits
Thanks to cormac-obrien’s publicly available instructions to navigate Twitch's IRC API via Python & socket, which was used in various forms within this release (http://www.instructables.com/id/Twitchtv-Moderator-Bot/)


