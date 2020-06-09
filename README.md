# Twitch Trivia Bot

Twitch Trivia Bot (TTB) is a Python script to run a trivia session in Twitch chat. The bot will load a quiz set, run a session of trivia, assign a winner and save scores dynamically. 

![img](https://i.imgur.com/YYznPaN.png)

# Features:
+ Loads csv files for trivia questions, and answers, and handles any amount of questions (limited only by csv constraints)
+ Dynamically selects a random set of questions from the pool of questions
+ Automatically asks questions, generates dynamic hints, and skips questions based on configurable time delays
+ BONUS mode, allowing for extra points to be rewarded
+ Stores trivia performance over multiple sessions, allowing participants to retrieve scores at any time
+ Trivia sessions cut short by bot disconnect can be reloaded via actively created backups

# Setup
The latest Python 3 install is required for this bot. You will need to install Python 3 to be able to run. One can either use standard Python 3 distribution with IDLE, or use something like the Anaconda distribution with Spyder (what I use). 

You will likely need to install a few dependencies, including `PyYaml` and `PyQt5`. You can do this via command line `pip install [x]` or `pip3 install [x]` (e.g. "pip install PyYaml"). On your first few runs if the program/GUI does not load, make sure to check `config/output_log.log` to read the error codes to identify what needs to be installed. 

Please use the [latest Release](/releases/latest/) download for initial install. 

+ “twitchtriviabot.py” does not need to be reconfigured. This will be loaded via Python console, and will connect to Twitch chat.
A trivia set file (csv) needs to be set up (more on this below). Default with this package is ‘triviaset.csv’ with the appropriate columns pre-identified. 
+ “auth_config.yml” and “trivia_config.yml” need to be configured. All inputs should be **without** brackets or number signs. Open these files in a text editor.
  + Under “trivia_config.yml”, the first two filename & filetype should match the trivia set file (default is ‘triviaset.csv’) All numeric fields represent seconds:
    + question_count = # of questions for the trivia session to include. This will be pulled randomly for the trivia list from csv. To be clear, this number isn't the number of questions in your trivia set, it's the number of questions you want a trivia session to hold
    + hint_time1 / hint_time2 = Time delay before hints 1 and 2 are supplied. Hints are described below
    + skip_time = Time delay before question is skipped. This is also used during `poll` modes for how long to wait before polling
    + question_delay = Time delay after question is answered, before next question is asked
    + question_bonusvalue = Value assigned to BONUS round questions. Bonus round described below
    + mode = There are three settings:
        + `single` - Standard trivia, first to answer wins the point
        + `poll` - In this mode, during the entirety of the skip_time, questions are polled for answers from players. At the end of each question, the first and second player to respond earn more points, then all others get some less amount of point
        + `poll2` - This is the same as above, but every question has a separate answer pool for "answer" and "answer2". This means, for example, one question can have two separate answers, and players can score on each answer separately
    + music_mode = `true` or `false`. Music mode is a manually-driven mode where the admin can start and stop questions via "Start Q" and "End Q" buttons on the GUI. Instead of loading the trivia set csv file, every question is loaded from `/config/music/artist.txt` and `track.txt`. Questions do not automatically start after their alloted time is up to answer - instead, the admin will manually choose when the next song is ready to be played. 
        + Functionally, the admin would prepare these artist/track files, start playing the song for their audience, then press "Start Q" when everything is ready. Answers come in, and when the question is done scoring, the system will wait until the admin chooses to start the next song
        + In the config file, mode `poll2` and length `infinite` must be selected for music_mode `true`
    + order = `random` of `ordered`. This allows the questions to be answered in order of the original trivia set, or to be chosen randomly. If `ordered` is chosen, likely it is advised to set `question_count` equal to the number of questions in the trivia set, which will yield all questions in order. 
    + length = `finite` of `infinite`. When using `infinite`, questions will never stop being asked until the admin chooses to end trivia. Questions are not reshuffled - they will continually be reasked in the same order. `finite` ends trivia after the `question_count` defined above
    + admins - separate by commas
        + E.g., admins = player
        + E.g., admins = player,respondent
  + “auth_config.yml” :
    + host = default irc.twitch.tv
    + port = default 6667 (for twitch)
    + nick = username for the bot
    + pass = password in “oath:xxxxxx... “ format. Retrieve from https://twitchapps.com/tmi/ for the bot
    + chan = twitch channel to connect the bot to, where trivia will take place. This has changed in version 2, where no number sign (#) is needed (i.e. cleartonic). This must match the channel name with capitalizations exactly.
    + encoding = either `utf-8` or `ISO-8859-1`. Somewhat experimental, default to `utf-8` for safety

To set up triviaset.csv properly, consider the following:
5 headers in this release are specified: ‘category, ‘question’, ‘answer’, ‘answer2’, ‘creator’. Keep them in this order.
Fill out row by row each question, filling in topic/game, and at least 1 Answer column. Creator is not required. 

A log will be saved per run to `config/output_log.log`. This will accumulate over time, and is useful for debugging problems. At any point, you can delete this file if it becomes too large. 

# Running the bot

With a command line/terminal open:
`python twitchtriviabot.py` or `python3 twitchtriviabot.py`

From here, you can monitor the bot’s activity. All user responses in the Twitch channel will appear in the console. Each question’s answer will appear in the console. 

If you need to close the GUI and stop the program, usually holding Ctrl+C will kill the program in the console/terminal. 

# Misc. Functionalities

### Hints and question timing 

All timings can be manually adjusted in config.txt. By default, after a question is asked, automatically generated hints will trigger (specified by trivia_config.yml). Later, the question will be skipped. After the specified session question limit is hit, the game will end, and a winner will be assigned. 
+ The first hint replaces 2 out of 3 characters in the answer with “_”
+ The second hint replaces all vowels with “_”

### BONUS

Bonus can be activated by an admin via !bonus command. Bonus mode makes questions worth more points, default 3 points (configurable in config.txt). Can be toggled on/off at any time. 

# Commands
The GUI and these commands below will yield the same results. Some commands are available only during active trivia sessions.

#### Admin only:
+ !triviastart - Begins a new trivia round with conditions specified in ‘config.txt’
+ !triviaend - Ends the trivia round & assigns a win. 
+ !next/!skip - Skips to the next question. All questions will automatically lapse after enough time specified in ‘config.txt’, but this allows for manually skipping.
+ !bonus - Switches questions to bonus mode (toggle on/off)
+ !stopbot - Severs the bot connection. 

#### All users:
+ !score - Reports user’s score (reports session score, total score for all trivia, and total wins for all trivia)

# Credits
Thanks to cormac-obrien’s publicly available instructions to navigate Twitch's IRC API via Python & socket, which was used in various forms within this release (http://www.instructables.com/id/Twitchtv-Moderator-Bot/)