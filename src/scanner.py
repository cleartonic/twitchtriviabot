def scanloop():
    print("Doin' my scan thang...")

# def scanloop():
#     try:
#         response = s.recv(1024).decode("utf-8")
#         if response == "PING :tmi.twitch.tv\r\n":
#             s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
#             print("Pong sent")
#         else:
#             username = re.search(r"\w+", response).group(0)
#             if username == chatvar.NICK:  # Ignore this bot's messages
#                 pass
#             else:
#                 message = chatvar.CHAT_MSG.sub("", response)
#                 cleanmessage = re.sub(r"\s+", "", message, flags=re.UNICODE)
#                 print("USER RESPONSE: " + username + " : " + message)
#                 if cleanmessage in var.COMMANDLIST:
#                     print("Command recognized.")
#                     trivia_commandswitch(cleanmessage,username)
#                     time.sleep(1)
#                 try:
# #                   if re.match(var.qs.iloc[var.session_questionno,2], message, re.IGNORECASE):   # old matching
#
#
#                     if bool(re.match("\\b"+var.qs.iloc[var.session_questionno,2]+"\\b",message,re.IGNORECASE)):   # strict new matching
#                         print("Answer recognized.")
#                         trivia_answer(username, cleanmessage)
#                     if bool(re.match("\\b"+var.qs.iloc[var.session_questionno,3]+"\\b",message,re.IGNORECASE)):   # strict new matching
#                         print("Answer recognized.")
#                         trivia_answer(username, cleanmessage)
#                 except:
#                     pass
#     except:
#         pass
