class Game:

    trivia_active = False
    userscores = {}                         # Dictionary holding user scores, kept in '!' and loaded/created upon trivia. [1,2,3] 1: Session score 2: Total trivia points 3: Total wins
    trivia_questionasked = False            # Switch for when a question is actively being asked
    trivia_questionasked_time = 0           # Time when the last question was asked (used for relative time length for hints/skip)
    trivia_hintasked = 0                    # 0 = not asked, 1 = first hint asked, 2 = second hint asked
    session_questionno = 0                  # Question # in current session
    session_answervalue = 1                 # How much each question is worth (altered by BONUS only)
    session_bonusround = 0                  # 0 - not bonus, 1 - bonus
    TIMER = 0                               # Ongoing active timer

#                 if cleanmessage in var.COMMANDLIST:
#                     print("Command recognized.")
#                     trivia_commandswitch(cleanmessage,username)
#                     time.sleep(1)
#                 try:
#                     if bool(re.match("\\b"+var.qs.iloc[var.session_questionno,2]+"\\b",message,re.IGNORECASE)):   # strict new matching
#                         print("Answer recognized.")
#                         trivia_answer(username, cleanmessage)
#                     if bool(re.match("\\b"+var.qs.iloc[var.session_questionno,3]+"\\b",message,re.IGNORECASE)):   # strict new matching
#                         print("Answer recognized.")
#                         trivia_answer(username, cleanmessage)
#                 except:
#                     pass
