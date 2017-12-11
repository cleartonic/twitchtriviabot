# -*- coding: utf-8 -*-
"""
@author: cleartonic
"""
import random
import json
import pandas as pd
import collections
import time
import socket
import re
import configparser
import os

# SETTINGS
class var():   
    infomessage = 'Twitch Trivia Bot loaded. Version 0.1.2. Developed by cleartonic.'

    # SETTINGS FOR END USERS
    trivia_filename = 'triviaset'               # Specify the filename (default "triviaset")
    trivia_filetype = 'csv'                     # Specify the file type. CSV (MUST be UTF-8), XLS, XLSX
    
    trivia_questions = 'INIT'                    # Total questions to be answered for trivia round
    trivia_hinttime_1 = 'INIT'                   # Seconds to 1st hint after question is asked
    trivia_hinttime_2 = 'INIT'                   # Seconds to 2nd hint after question is asked
    trivia_skiptime = 'INIT'                     # Seconds until the question is skipped automatically
    trivia_questiondelay = 'INIT'                # Seconds to wait after previous question is answered before asking next question
    trivia_bonusvalue = 'INIT'                   # BONUS: How much points are worth in BONUS round
    admins = 'INIT'

    # FUNCTION VARIABLES 
    if trivia_filetype == 'csv':                # open trivia source based on type
        ts = pd.read_csv(trivia_filename+"."+trivia_filetype)   
    if trivia_filetype == 'xlsx' or trivia_filetype == 'xls':
        ts = pd.read_excel(trivia_filename+"."+trivia_filetype) # open trivia source based on type        
    if trivia_filetype != 'xlsx' and trivia_filetype != 'xls' and trivia_filetype != 'csv':
        print("Warning! No file loaded. Type !stopbot and try loading again.")
    tsrows = ts.shape[0]                    # Dynamic # of rows based on triviaset
    qs = pd.DataFrame(columns=list(ts))     # Set columns in quizset to same as triviaset
    userscores = {}                         # Dictionary holding user scores, kept in '!' and loaded/created upon trivia. [1,2,3] 1: Session score 2: Total trivia points 3: Total wins
    COMMANDLIST = ["!triviastart","!triviaend","!top3","!hint","!bonus","!score","!next","!stop","!loadconfig","!backuptrivia","!loadtrivia","!creator"] # All commands
    SWITCH = True                           # Switch to keep bot connection running
    trivia_active = False                   # Switch for when trivia is being played
    trivia_questionasked = False            # Switch for when a question is actively being asked
    trivia_questionasked_time = 0           # Time when the last question was asked (used for relative time length for hints/skip)
    trivia_hintasked = 0                    # 0 = not asked, 1 = first hint asked, 2 = second hint asked
    session_questionno = 0                  # Question # in current session
    session_answervalue = 1                 # How much each question is worth (altered by BONUS only)
    session_bonusround = 0                  # 0 - not bonus, 1 - bonus
    TIMER = 0                               # Ongoing active timer 

class chatvar():                            # Variables for IRC / Twitch chat function
    HOST = 'INIT'
    PORT = 'INIT'
    NICK = 'INIT'
    PASS = 'INIT'
    CHAN = 'INIT'
    RATE = (120) # messages per second
    CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")    
    
    
# CODE


##### Trivia start build. ts = "Trivia set" means original master trivia file. qs = "Quiz set" means what's going to be played with for the session
def trivia_start():
    sendmessage("Trivia has been initiated. Generating trivia base for session...")
    qs_buildrows = 0                        # starts at zero, must reach trivia_questions to be complete during while loop        
           
    ### Loop through TS and build QS until qs_buildrows = trivia_numbers 
    
    if var.tsrows < var.trivia_questions:
        var.trivia_questions = int(var.tsrows)
        print("Warning: Trivia questions for session exceeds trivia set's population. Setting session equal to max questions.")
    numberlist = []
    for i in range(var.tsrows):             # Create a list of all indices
        numberlist.append(i)
    while qs_buildrows < var.trivia_questions:  
        temprando = random.choice(numberlist)
        numberlist.remove(temprando)
        try: 
            var.qs = var.qs.append(var.ts.loc[temprando],verify_integrity=True)    # Check for duplicates with last argument, skip if so
            qs_buildrows += 1
        except:                             # pass on duplicates and re-roll
            print("Duplicate index. This should not happen, dropping row from table. Please check config.txt's trivia_questions are <= total # of questions in trivia set.")
            var.ts.drop(var.ts.index[[temprando]])
    print("Quizset built.")
    var.trivia_active = True
    sendmessage("Trivia has begun! Question Count: "+str(var.trivia_questions)+". Trivia will start in "+str(var.trivia_questiondelay)+" seconds.")
    time.sleep(var.trivia_questiondelay)
    trivia_callquestion()

def loadscores():
    ### Load score list
    try:
        with open('userscores.txt', 'r') as fp:
            print("Score list loaded.")
            var.userscores = json.load(fp)
    except:
        with open('userscores.txt', "w") as fp:
            print("No score list, creating...")
            var.userscores = {'trivia_dummy':[0,0,0]}   
            json.dump(var.userscores , fp)

def loadconfig():
    config = configparser.ConfigParser()
    config.read('config.txt')
    var.trivia_filename = config['Trivia Settings']['trivia_filename']
    var.trivia_filetype = config['Trivia Settings']['trivia_filetype']
    var.trivia_questions = int(config['Trivia Settings']['trivia_questions'])
    var.trivia_hinttime_1 = int(config['Trivia Settings']['trivia_hinttime_1'])
    var.trivia_hinttime_2 = int(config['Trivia Settings']['trivia_hinttime_2'])
    var.trivia_skiptime = int(config['Trivia Settings']['trivia_skiptime'])
    var.trivia_questiondelay = int(config['Trivia Settings']['trivia_questiondelay'])
    var.trivia_bonusvalue = int(config['Trivia Settings']['trivia_bonusvalue'])
    
    admin1 = config['Admin Settings']['admins']
    var.admins = admin1.split(',')

    chatvar.HOST = str(config['Bot Settings']['HOST'])
    chatvar.PORT = int(config['Bot Settings']['PORT'])
    chatvar.NICK = config['Bot Settings']['NICK']
    chatvar.PASS = config['Bot Settings']['PASS']
    chatvar.CHAN = config['Bot Settings']['CHAN']    

def dumpscores():
    try:
        with open('userscores.txt', 'w') as fp:
            json.dump(var.userscores , fp)
    except:
        print("Scores NOT saved!")
        pass
    
### Trivia command switcher 
def trivia_commandswitch(cleanmessage,username):
    
    # ADMIN ONLY COMMANDS
    if username in var.admins:    
        if cleanmessage == "!triviastart":
            if var.trivia_active:
                print("Trivia already active.")
            else:
                trivia_start()
        if cleanmessage == "!triviaend":
            if var.trivia_active:
                trivia_end()
        if cleanmessage == "!stop":
                stopbot()
        if cleanmessage == "!loadconfig":
                loadconfig()                
                sendmessage("Config reloaded.")
        if cleanmessage == "!backuptrivia":
                trivia_savebackup()
                sendmessage("Backup created.")
        if cleanmessage == "!loadtrivia":
                trivia_loadbackup()
        if cleanmessage == "!next":
                trivia_skipquestion()                      

    # ACTIVE TRIVIA COMMANDS            
    if var.trivia_active:
        if cleanmessage == "!top3":
                topscore = trivia_top3score()
                print("topscore",topscore)
                print("Len",len(topscore))
                try:
                    if (len(topscore) >= 3):
                        msg = "In 1st: "+str(topscore[0][0])+" "+str(topscore[0][1])+" points. 2nd place: "+str(topscore[1][0])+" "+str(topscore[1][1])+" points. 3rd place: "+str(topscore[2][0])+" "+str(topscore[2][1])+" points."
                        sendmessage(msg)
                    if (len(topscore) == 2):
                        msg = "In 1st: "+str(topscore[0][0])+" "+str(topscore[0][1])+" points. 2nd place: "+str(topscore[1][0])+" "+str(topscore[1][1])+" points."
                        sendmessage(msg)
                    if (len(topscore) == 1):
                        msg = "In 1st: "+str(topscore[0][0])+" "+str(topscore[0][1])+" points."
                        sendmessage(msg)
                except:
                    msg = "No scores yet."
                    sendmessage(msg)     
        if cleanmessage == "!hint":
            if var.trivia_hintasked == 0:
                trivia_askhint(0)
            if var.trivia_hintasked == 1:
                trivia_askhint(0)
            if var.trivia_hintasked == 2:
                trivia_askhint(1)                   

        if cleanmessage == "!bonus":
                if var.session_bonusround == 0:
                    trivia_startbonus()
                    var.session_bonusround = 1
                if var.session_bonusround == 1:
                    trivia_endbonus()
                    var.session_bonusround = 0
                    
    # GLOBAL COMMANDS                     
    if cleanmessage == "!score":
        trivia_userscore(username) 

           
### Call trivia question
def trivia_callquestion():
    var.trivia_questionasked = True
    var.trivia_questionasked_time = round(time.time()) 

    msg = "Question "+str(var.session_questionno+1)+": ["+var.qs.iloc[var.session_questionno,0]+"] "+var.qs.iloc[var.session_questionno,1]

    sendmessage(msg)
    print("Question "+str(var.session_questionno+1)+": | ANSWER: "+var.qs.iloc[var.session_questionno,2])

def trivia_answer(username,cleanmessage):
    var.trivia_questionasked = False
    try:
        var.userscores[username][0] += var.session_answervalue
        var.userscores[username][1] += var.session_answervalue
    except:
        print("Failed to find user! Adding new")  
        var.userscores[username] = [var.session_answervalue,var.session_answervalue,0]  # sets up new user 
    dumpscores() # Save all current scores
    if var.session_answervalue == 1:
        msg = str(username)+" answers question #"+str(var.session_questionno+1)+" correctly! The answer is ** "+str(var.qs.iloc[var.session_questionno,2])+" ** for "+str(var.session_answervalue)+" point. "+str(username)+" has "+str(var.userscores[username][0])+" points!"
    else:
        msg = str(username)+" answers question #"+str(var.session_questionno+1)+" correctly! The answer is ** "+str(var.qs.iloc[var.session_questionno,2])+" ** for "+str(var.session_answervalue)+" points. "+str(username)+" has "+str(var.userscores[username][0])+" points!"
    sendmessage(msg)
    time.sleep((var.trivia_questiondelay))
    var.session_questionno += 1
    var.trivia_hintasked = 0
    var.trivia_questionasked = False
    var.trivia_questionasked_time = 0
    trivia_savebackup()
    if var.trivia_questions == var.session_questionno:          # End game check
        trivia_end()
    else:
        trivia_callquestion()
    
    
    
### Finishes trivia by getting top 3 list, then adjusting final message based on how many participants. Then dumpscore()  
def trivia_end():        
   
    topscore = trivia_top3score()            # Argument "1" will return the first in the list (0th position) for list of top 3
    trivia_clearscores()
    if (len(topscore) == 0):
            msg = "No answered questions. Results are blank."
            sendmessage(msg)

    else:
        msg = "Trivia is over! Calculating scores..."
        sendmessage(msg)
        time.sleep(2)
        trivia_assignwinner(topscore[0][0])
        if (len(topscore) >= 3):
            msg = " *** "+str(topscore[0][0])+" *** is the winner of trivia with "+str(topscore[0][1])+" points! 2nd place: "+str(topscore[1][0])+" "+str(topscore[1][1])+" points. 3rd place: "+str(topscore[2][0])+" "+str(topscore[2][1])+" points."
            sendmessage(msg)
        if (len(topscore) == 2):
            msg = " *** "+str(topscore[0][0])+" *** is the winner of trivia with "+str(topscore[0][1])+" points! 2nd place: "+str(topscore[1][0])+" "+str(topscore[1][1])+" points."
            sendmessage(msg)
        if (len(topscore) == 1):
            msg = " *** "+str(topscore[0][0])+" *** is the winner of trivia with "+str(topscore[0][1])+" points!"
            sendmessage(msg)

    dumpscores()
    time.sleep(3)
    msg2 = "Thanks for playing! See you next time!"
    sendmessage(msg2)    
    
    var.session_questionno = 0                # reset variables for trivia
    var.trivia_active = False
    var.trivia_hintasked = 0
    var.trivia_questionasked = False
    var.trivia_questionasked_time = 0
    var.qs = pd.DataFrame(columns=list(var.ts))
    
    # Clear backup files upon finishing trivia
    os.remove('backup/backupquizset.csv', dir_fd=None)
    os.remove('backup/backupscores.txt', dir_fd=None)
    os.remove('backup/backupsession.txt', dir_fd=None)


def trivia_routinechecks():                   # after every time loop, routine checking of various vars/procs
    var.TIMER = round(time.time())
    
    if var.trivia_questions == var.session_questionno:          # End game check
        trivia_end()
    
    if ((var.TIMER - var.trivia_questionasked_time)>var.trivia_hinttime_2 and var.trivia_active and var.trivia_hintasked == 1):
        var.trivia_hintasked = 2
        trivia_askhint(1) # Ask second hint
        
    if ((var.TIMER - var.trivia_questionasked_time)>var.trivia_hinttime_1 and var.trivia_active and var.trivia_hintasked == 0):
        var.trivia_hintasked = 1
        trivia_askhint(0) # Ask first hint     
        
    if ((var.TIMER - var.trivia_questionasked_time)>var.trivia_skiptime and var.trivia_active):
        trivia_skipquestion()

    
    
def trivia_askhint(hinttype=0):                 # hinttype: 0 = 1st hint, 1 = 2nd hint
    if hinttype == 0:                           # type 0, replace 2 out of 3 chars with _
        prehint = str(var.qs.iloc[var.session_questionno,2])
        listo = []
        hint = ''
        counter = 0
        for i in prehint:
            if counter % 3 >= 0.7:
                listo += "_"
            else:
                listo += i
            counter += 1
        for i in range(len(listo)):
            hint += hint.join(listo[i])
        sendmessage("Hint #1: "+hint)     

    if hinttype == 1:                           # type 1, replace vowels with _
        prehint = str(var.qs.iloc[var.session_questionno,2])
        hint = re.sub('[aeiou]','_',prehint,flags=re.I)
        sendmessage("Hint #2: "+hint)
                    
    
def trivia_skipquestion():
    if var.trivia_active:
        var.session_questionno += 1
        var.trivia_hintasked = 0
        var.trivia_questionasked = False
        var.trivia_questionasked_time = 0
        try:
            sendmessage("Question was not answered in time. Answer: "+str(var.qs.iloc[var.session_questionno-1,2])+". Skipping to next question:")
        except:
            sendmessage("Question was not answered in time. Skipping to next question:")
        time.sleep(var.trivia_questiondelay)
        if var.trivia_questions == var.session_questionno:          # End game check
            trivia_end()
        else:
            trivia_callquestion()        

    
### B O N U S    
def trivia_startbonus():
    msg = "B O N U S Round begins! Questions are now worth "+str(var.trivia_bonusvalue)+" points!"
    sendmessage(msg)
    var.session_answervalue = var.trivia_bonusvalue
    
def trivia_endbonus():
    msg = "Bonus round is over! Questions are now worth 1 point."
    sendmessage(msg)
    var.session_answervalue = 1

    

### Top 3 trivia 
def trivia_top3score():
    data2 = {}                                  # temp dictionary just for keys & sessionscore
    for i in var.userscores.keys():
        if var.userscores[i][0] > 0:
            data2[i] = var.userscores[i][0]

    data3 = collections.Counter(data2)          #top 3 counter
    data3.most_common()
    top3 = []                                   #top 3 list
    for k, v in data3.most_common(3):
        top3 += [[k,v]]
    return top3
    
### clears scores and assigns a win to winner
def trivia_clearscores():           
    for i in var.userscores.keys():
        var.userscores[i][0] = 0
        
### Add +1 to winner's win in userscores
def trivia_assignwinner(winner):    
    var.userscores[winner][2] += 1
       

### temp function to give 100 score to each 
def trivia_givescores():
    for i in var.userscores.keys():
        var.userscores[i][0] = random.randrange(0,1000)
        
def trivia_userscore(username):
    try:
        msg = str(username)+" has "+str(var.userscores[username][0])+" points for this trivia session, "+str(var.userscores[username][1])+" total points and "+str(var.userscores[username][2])+" total wins."
        sendmessage(msg)
    except:
        msg = str(username)+" not found in database."
        sendmessage(msg)
        
### Chat message sender func
def sendmessage(msg):
    answermsg = ":"+chatvar.NICK+"!"+chatvar.NICK+"@"+chatvar.NICK+".tmi.twitch.tv PRIVMSG "+chatvar.CHAN+" : "+msg+"\r\n"
    answermsg2 = answermsg.encode("utf-8")
    s.send(answermsg2)

### STOP BOT (sets loop to false)
def stopbot():
    var.SWITCH = False

### CALL TIMER
def calltimer():
    print("Timer: "+str(var.TIMER))



### BACKUP SAVING/LOADING
    
def trivia_savebackup():            # backup session saver
    # Save session position/variables 
    config2 = configparser.ConfigParser()
    config2['DEFAULT'] = {'session_questionno': var.session_questionno, 'session_answervalue': var.session_answervalue, 'session_bonusround': var.session_bonusround}
    with open ('backup/backupsession.txt','w') as c:
        config2.write(c)    
        
    # Save CSV of quizset 
    var.qs.to_csv('backup/backupquizset.csv',index=False,encoding='utf-8')
    # Save session scores
    try:
        with open('backup/backupscores.txt', 'w') as fp:
            json.dump(var.userscores, fp)
    except:
        print("Scores NOT saved!")
        pass
        

def trivia_loadbackup():            # backup session loader
    if var.trivia_active:
        sendmessage("Trivia is already active. Prior session was not reloaded.")
    else:
        # Load session position/variables 
        config2 = configparser.ConfigParser()
        config2.read('backup/backupsession.txt')
    
        var.session_questionno = int(config2['DEFAULT']['session_questionno'])
        var.session_answervalue = int(config2['DEFAULT']['session_answervalue'])
        var.session_bonusround = int(config2['DEFAULT']['session_bonusround'])
    
        # Load quizset 
        var.qs = pd.read_csv('backup/backupquizset.csv',encoding='utf-8')
    
        # Load session scores
    
        try:
            with open('backup/backupscores.txt', 'r') as fp:
                print("Score list loaded.")
                var.userscores = json.load(fp)
        except:
            with open('backup/backupscores.txt', "w") as fp:
                print("No score list, creating...")
                var.userscores = {'trivia_dummy':[0,0,0]}   
                json.dump(var.userscores , fp)
    
        print("Loaded backup.")
        var.trivia_active = True
        sendmessage("Trivia sessions reloaded. Trivia will begin again in "+str(var.trivia_questiondelay)+" seconds.")
        time.sleep(var.trivia_questiondelay)
        trivia_callquestion()




############### CHAT & BOT CONNECT ###############



## STARTING PROCEDURES
        
print("Bot loaded. Loading config and scores...")
try:
    loadconfig()
    print("Config loaded.")
except:
    print("Config not loaded! Check config file and reboot bot")
    var.SWITCH = False

try:
    loadscores()
    print("Scores loaded.")
except:
    print("Scores not loaded! Check or delete 'userscores.txt' file and reboot bot")
    var.SWITCH = False
    



          
if var.SWITCH:
    try:
        s = socket.socket()
        s.connect((chatvar.HOST, chatvar.PORT))
        s.send("PASS {}\r\n".format(chatvar.PASS).encode("utf-8"))
        s.send("NICK {}\r\n".format(chatvar.NICK).encode("utf-8"))
        s.send("JOIN {}\r\n".format(chatvar.CHAN).encode("utf-8"))
        time.sleep(1)
        sendmessage(var.infomessage)
        s.setblocking(0)
    except:
        print("Connection failed. Check config settings and reload bot.")
        var.SWITCH = False

def scanloop():
    try:
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            print("Pong sent")
        else:
            username = re.search(r"\w+", response).group(0) 
            if username == chatvar.NICK:  # Ignore this bot's messages
                pass
            else:
                message = chatvar.CHAT_MSG.sub("", response)
                cleanmessage = re.sub(r"\s+", "", message, flags=re.UNICODE)
                print("USER RESPONSE: " + username + " : " + message)
                if cleanmessage in var.COMMANDLIST:
                    print("Command recognized.")
                    trivia_commandswitch(cleanmessage,username)
                    time.sleep(1)
                try:                
#                   if re.match(var.qs.iloc[var.session_questionno,2], message, re.IGNORECASE):   # old matching
                    
                    
                    if bool(re.match("\\b"+var.qs.iloc[var.session_questionno,2]+"\\b",message,re.IGNORECASE)):   # strict new matching
                        print("Answer recognized.")
                        trivia_answer(username, cleanmessage)
                    if bool(re.match("\\b"+var.qs.iloc[var.session_questionno,3]+"\\b",message,re.IGNORECASE)):   # strict new matching
                        print("Answer recognized.")
                        trivia_answer(username, cleanmessage)                        
                except:
                    pass
    except:
        pass


# Infinite loop while bot is active to scan messages & perform routines
        
while var.SWITCH:
    if var.trivia_active:
        trivia_routinechecks()
    scanloop()
    time.sleep(1 / chatvar.RATE)    



        

# 0: Index
# 0: Game
# 1: Question
# 2: Answer
# 3: Answer 2
# 4: Grouping
# 5: Creator
