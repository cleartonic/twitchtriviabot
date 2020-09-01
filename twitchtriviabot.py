# -*- coding: utf-8 -*-
"""
@author: cleartonic
"""
import copy
import csv
import datetime
import json
import logging
import os
import pickle
import random
import shutil
import sys
import time
import traceback
import yaml

from twitchtriviabot.chatbot import ChatBot
from twitchtriviabot.session import Session, NullSession

from PyQt5.QtWidgets import QLabel, QFrame, QLineEdit, QPushButton, QCheckBox, QApplication, QMainWindow, \
                            QFileDialog, QDialog, QScrollArea, QMessageBox, QWidget, QTextEdit
from PyQt5 import QtCore, QtGui, QtTest
from PyQt5.QtGui import QPixmap, QIntValidator, QPalette, QColor
from PyQt5.QtCore import QThread, pyqtSignal, QTimer

try:
    THIS_FILEPATH = os.path.dirname(__file__)
    THIS_FILENAME = os.path.basename(__file__)
except:
    THIS_FILEPATH = os.path.dirname(sys.executable)
    THIS_FILENAME = os.path.basename(sys.executable)

    
logging.basicConfig(format='%(asctime)s %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S %p',
                filename=os.path.join(THIS_FILEPATH,'config','output_log.log'),
                filemode='a',
                level=logging.DEBUG)

VERSION_NUM = "2.1.0"

AUTH_CONFIG_PATH=os.path.abspath(os.path.join(THIS_FILEPATH,'config','auth_config.yml'))
TRIVIA_CONFIG_PATH=os.path.abspath(os.path.join(THIS_FILEPATH,'config','trivia_config.yml'))

if not os.path.exists(os.path.abspath(os.path.join(THIS_FILEPATH,'config'))):
    os.makedirs(os.path.abspath(os.path.join(THIS_FILEPATH,'config')))
if not os.path.exists(AUTH_CONFIG_PATH):
    shutil.copyfile(
        os.path.abspath(os.path.join(THIS_FILEPATH,'init_config','auth_config.yml')),
        AUTH_CONFIG_PATH)
if not os.path.exists(TRIVIA_CONFIG_PATH):
    shutil.copyfile(
        os.path.abspath(os.path.join(THIS_FILEPATH,'init_config','trivia_config.yml')),
        TRIVIA_CONFIG_PATH)
if not os.path.exists(os.path.abspath(os.path.join(THIS_FILEPATH,'config','scores'))):
    os.makedirs(os.path.abspath(os.path.join(THIS_FILEPATH,'config','scores')))
if not os.path.exists(os.path.abspath(os.path.join(THIS_FILEPATH,'config','music'))):
    os.makedirs(os.path.abspath(os.path.join(THIS_FILEPATH,'config','music')))
    
    with open(os.path.abspath(os.path.join(THIS_FILEPATH,'config','music','track.txt')),'w') as f:
        f.write('Null track')
    with open(os.path.abspath(os.path.join(THIS_FILEPATH,'config','music','artist.txt')),'w') as f:
        f.write('Null artist')
    

class MainWindow(QWidget):
    SCREEN_HEIGHT = 400
    SCREEN_WIDTH = 320
    
    def __init__(self):
        self.BORDER = False
        self.app = QApplication([])
        super(MainWindow, self).__init__()
        self.window = QMainWindow()
        self.window.setFixedSize(self.SCREEN_WIDTH,self.SCREEN_HEIGHT)
        self.window.setWindowTitle('Twitch Trivia Bot')
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap("ico.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.window.setWindowIcon(self.icon)
        self.connection_active = False
        self.bot_status_dict = {"connect_status":"Inactive",
                                "trivia_status":"Inactive"}
        self.bot_status_dict_init = {"connect_status":"Inactive",
                                "trivia_status":"Inactive"}
      
        self.tb = None
            
        self.title_bar = QLabel("",self.window)
        self.title_bar.setGeometry(QtCore.QRect(0, 0, 320, 20))
        self.title_bar.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
        if self.BORDER:
            self.title_bar.setStyleSheet("border:2px solid rgb(255,255,255); ")     
            

        self.title_bar_text = QLabel("Twitch Trivia Bot version %s" % VERSION_NUM,self.window)
        self.title_bar_text.setGeometry(QtCore.QRect(0, 0, 320, 20))
        self.title_bar_text.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
        self.title_bar_text.setStyleSheet("background :rgb(72,72,72); ")
        
        self.connect_status_label = QLabel("Bot status:", self.window)
        self.connect_status_label.setGeometry(QtCore.QRect(0, 40, 80, 20))
        self.connect_status_label.setAlignment(QtCore.Qt.AlignLeft)
        if self.BORDER:
            self.connect_status_label.setStyleSheet("border:2px solid rgb(255,255,255); ")    
            
        self.connect_status = QLabel(self.bot_status_dict['connect_status'],self.window)
        self.connect_status.setGeometry(QtCore.QRect(80, 40, 80, 20))
        self.connect_status.setAlignment(QtCore.Qt.AlignLeft)
        self.connect_status.setStyleSheet("QLabel { color : red; }");      
        if self.BORDER:
            self.connect_status.setStyleSheet("border:2px solid rgb(255,255,255); ")    
            
        self.trivia_status_label = QLabel("Trivia status:", self.window)
        self.trivia_status_label.setGeometry(QtCore.QRect(160, 40, 80, 20))
        self.trivia_status_label.setAlignment(QtCore.Qt.AlignLeft)
        if self.BORDER:
            self.trivia_status_label.setStyleSheet("border:2px solid rgb(255,255,255); ")    
            
        self.trivia_status = QLabel(self.bot_status_dict['trivia_status'],self.window)
        self.trivia_status.setGeometry(QtCore.QRect(240, 40, 80, 20))
        self.trivia_status.setAlignment(QtCore.Qt.AlignLeft)
        self.trivia_status.setStyleSheet("QLabel { color : red; }");      
        if self.BORDER:
            self.trivia_status.setStyleSheet("border:2px solid rgb(255,255,255); ")    
            
        self.category_label = QLabel("Category:",self.window)
        self.category_label.setGeometry(QtCore.QRect(0, 80, 80, 20))
        self.category_label.setAlignment(QtCore.Qt.AlignLeft)
        self.category_label.setStyleSheet("QLabel { font-weight : bold; }");      
        if self.BORDER:
            self.category_label.setStyleSheet("border:2px solid rgb(255,255,255); ")   
            
        self.category_variable_text = QLabel("Sample category",self.window)
        self.category_variable_text.setGeometry(QtCore.QRect(80, 80, 240, 20))
        self.category_variable_text.setAlignment(QtCore.Qt.AlignLeft)
        if self.BORDER:
            self.category_variable_text.setStyleSheet("border:2px solid rgb(255,255,255); ")   
            

        
        self.question_label = QLabel("Question:",self.window)
        self.question_label.setGeometry(QtCore.QRect(0, 100, 80, 20))
        self.question_label.setAlignment(QtCore.Qt.AlignLeft)
        self.question_label.setStyleSheet("QLabel { font-weight : bold; }");      
        if self.BORDER:
            self.question_label.setStyleSheet("border:2px solid rgb(255,255,255); ")  
            
        self.question_variable_text = QLabel("Sample question",self.window)
        self.question_variable_text.setGeometry(QtCore.QRect(80, 100, 240, 60))
        self.question_variable_text.setAlignment(QtCore.Qt.AlignLeft)
        if self.BORDER:
            self.question_variable_text.setStyleSheet("border:2px solid rgb(255,255,255); ")  
            
        self.question_no_variable_text = QLabel("",self.window)
        self.question_no_variable_text.setGeometry(QtCore.QRect(0, 120, 80, 20))
        self.question_no_variable_text.setAlignment(QtCore.Qt.AlignLeft)
        if self.BORDER:
            self.question_no_variable_text.setStyleSheet("border:2px solid rgb(255,255,255); ")  

        self.top3_label = QLabel("Top 3:",self.window)
        self.top3_label.setGeometry(QtCore.QRect(0, 160, 80, 20))
        self.top3_label.setAlignment(QtCore.Qt.AlignLeft)
        self.top3_label.setStyleSheet("QLabel { font-weight : bold; }");      
        if self.BORDER:
            self.top3_label.setStyleSheet("border:2px solid rgb(255,255,255); ")  
            
        self.top3_variable_text = QLabel("Top 3 sample",self.window)
        self.top3_variable_text.setGeometry(QtCore.QRect(80, 160, 240, 60))
        self.top3_variable_text.setAlignment(QtCore.Qt.AlignLeft)
        if self.BORDER:
            self.top3_variable_text.setStyleSheet("border:2px solid rgb(255,255,255); ")   

            
        self.answer_label = QLabel("Answer(s):",self.window)
        self.answer_label.setGeometry(QtCore.QRect(0, 240, 80, 20))
        self.answer_label.setAlignment(QtCore.Qt.AlignLeft)
        self.answer_label.setStyleSheet("QLabel { font-weight : bold; }");      
        if self.BORDER:
            self.answer_label.setStyleSheet("border:2px solid rgb(255,255,255); ")  
            
        self.answer_variable_text = QLabel("Sample answer",self.window)
        self.answer_variable_text.setGeometry(QtCore.QRect(80, 240, 240, 20))
        self.answer_variable_text.setAlignment(QtCore.Qt.AlignLeft)
        if self.BORDER:
            self.answer_variable_text.setStyleSheet("border:2px solid rgb(255,255,255); ")   

       
        self.category_label.setVisible(False)
        self.question_label.setVisible(False)
        self.answer_label.setVisible(False)            
        self.top3_label.setVisible(False)            
        self.category_variable_text.setVisible(False)
        self.question_variable_text.setVisible(False)
        self.answer_variable_text.setVisible(False)
        self.top3_variable_text.setVisible(False)
        self.question_no_variable_text.setVisible(False)

        self.category_variable_text.setWordWrap(True)
        self.question_variable_text.setWordWrap(True)
        self.answer_variable_text.setWordWrap(True)
        
        
        
        self.connect_button = QPushButton("Connect",self.window)
        self.connect_button.setGeometry(QtCore.QRect(0, 340, 70, 30))
        self.connect_button.clicked.connect(self.toggle_connect)
        
        self.trivia_start_button = QPushButton("Start Trivia",self.window)
        self.trivia_start_button.setGeometry(QtCore.QRect(80, 340, 70, 30))
        self.trivia_start_button.clicked.connect(self.toggle_start_trivia)
        self.trivia_start_button.setVisible(False)
        
        self.trivia_skip_button = QPushButton("Skip",self.window)
        self.trivia_skip_button.setGeometry(QtCore.QRect(160, 340, 70, 30))
        self.trivia_skip_button.clicked.connect(self.skip_question)
        self.trivia_skip_button.setVisible(False)
        
        self.trivia_startq_button = QPushButton("Start Q",self.window)
        self.trivia_startq_button.setGeometry(QtCore.QRect(160, 340, 70, 30))
        self.trivia_startq_button.clicked.connect(self.start_question)
        self.trivia_startq_button.setVisible(False)
        
        self.trivia_endq_button = QPushButton("End Q",self.window)
        self.trivia_endq_button.setGeometry(QtCore.QRect(240, 340, 70, 30))
        self.trivia_endq_button.clicked.connect(self.end_question)
        self.trivia_endq_button.setVisible(False)

        self.footer_bar_text = QLabel("Developed by @cleartonic  |  twitch.tv/cleartonic",self.window)
        self.footer_bar_text.setGeometry(QtCore.QRect(0, 380, 320, 20))
        self.footer_bar_text.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
        self.footer_bar_text.setStyleSheet("background :rgb(72,72,72); ")

        # Final settings
        self.app.setStyle('Fusion')
        self.app.setFont(QtGui.QFont("Roboto", 9))
        
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(0, 0, 0))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, QColor(120, 120, 0))
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        self.app.setPalette(palette)


    def update_gui(self):
        '''
        This takes all variables from the active tb 
        '''
        self.connect_status.setText(self.bot_status_dict['connect_status'])
        if self.bot_status_dict['connect_status'] == 'Active':
            self.connect_status.setStyleSheet("QLabel { color : green; }");    
        else:
            self.connect_status.setStyleSheet("QLabel { color : red; }");    

            
        try:
            self.bot_status_dict['trivia_status'] = self.tb.active_session.trivia_status
        except:
            self.bot_status_dict['trivia_status'] = "Inactive"
        self.trivia_status.setText(self.bot_status_dict['trivia_status'])
        if self.bot_status_dict['trivia_status'] == 'Active':
            self.trivia_status.setStyleSheet("QLabel { color : green; }");    
        elif self.bot_status_dict['trivia_status'] == 'Finished':
            self.trivia_status.setStyleSheet("QLabel { color : blue; }");    
        else:
            self.trivia_status.setStyleSheet("QLabel { color : red; }");    
            
        
        
        if self.tb:
            self.trivia_start_button.setVisible(True)
            if self.tb.trivia_active:
                self.category_label.setVisible(True)
                self.question_label.setVisible(True)
                self.answer_label.setVisible(True)
                self.top3_label.setVisible(True)
                self.top3_variable_text.setText(self.tb.active_session.check_top_3())
                if str(self.tb.active_session.session_config['music_mode']) == 'true' or self.tb.active_session.session_config['music_mode'] == True:
                    self.trivia_startq_button.setVisible(True)
                else:
                    self.trivia_skip_button.setVisible(True)
                if self.tb.active_session.session_config['mode'] == 'poll' or self.tb.active_session.session_config['mode'] == 'poll2':    
                    self.trivia_endq_button.setVisible(True)
                if self.tb.active_session.questionasked:
                    self.category_variable_text.setVisible(True)
                    self.question_variable_text.setVisible(True)
                    self.answer_variable_text.setVisible(True)
                    self.top3_variable_text.setVisible(True)
                    self.question_no_variable_text.setVisible(True)
                    self.category_variable_text.setText(self.tb.active_session.active_question.category)
                    self.question_variable_text.setText(self.tb.active_session.active_question.question)
                    self.answer_variable_text.setText(', '.join(self.tb.active_session.active_question.answers))
                    self.question_no_variable_text.setText(self.tb.active_session.report_question_numbers())
                else:
                    self.category_variable_text.setVisible(False)
                    self.question_variable_text.setVisible(False)
                    self.answer_variable_text.setVisible(False)
                    self.question_no_variable_text.setVisible(False)
                    self.category_variable_text.setText("")
                    self.question_variable_text.setText("")
                    self.answer_variable_text.setText("")
                    self.top3_variable_text.setText("")
                    self.question_no_variable_text.setText("")

        else:
            self.set_all_invisible()
            
        # special cases
        if self.bot_status_dict['trivia_status'] == "Finished":
            self.trivia_start_button.setText("Start Trivia")
            self.trivia_skip_button.setVisible(False)
            self.trivia_endq_button.setVisible(False)
            
    def set_all_invisible(self):
        self.category_label.setVisible(False)
        self.question_label.setVisible(False)
        self.answer_label.setVisible(False)            
        self.top3_label.setVisible(False)
        self.category_variable_text.setVisible(False)
        self.question_variable_text.setVisible(False)
        self.question_no_variable_text.setVisible(False)
        self.answer_variable_text.setVisible(False)
        self.top3_variable_text.setVisible(False)
        self.trivia_start_button.setVisible(False)
        self.trivia_skip_button.setVisible(False)
        self.trivia_startq_button.setVisible(False)
        self.trivia_endq_button.setVisible(False)
    
    def toggle_connect(self):
        logging.debug("Connect %s " % self.connection_active)
        if self.connection_active:
            self.bot_status_dict['connect_status'] = 'Inactive'
            self.bot_status_dict = self.bot_status_dict_init
            self.set_all_invisible()
            self.update_gui()
            self.end_connection()
        else:
            self.bot_status_dict['connect_status'] = 'Active'
            self.connect()
            
    def toggle_start_trivia(self):
        if not self.tb.active_session.trivia_active:
            self.trivia_start_button.setText("Stop Trivia")
            self.tb.start_session()
        else:
            self.trivia_start_button.setText("Start Trivia")
            self.tb.active_session.force_end_of_trivia()
        
    def skip_question(self):
        if self.tb.active_session.trivia_active:
            try:
                self.tb.active_session.skip_question()
            except:
                logging.debug("Error on skipping question : %s" % traceback.print_exc())
                
    def start_question(self):
        if self.tb.active_session.trivia_active:
            try:
                self.tb.active_session.start_question()
            except:
                logging.debug("Error on starting question : %s" % traceback.print_exc())
                
    def end_question(self):
        if self.tb.active_session.trivia_active:
            try:
                logging.info("Ending question")
                self.tb.active_session.end_question()
            except:
                logging.debug("Error on ending question : %s" % traceback.print_exc())
        
    def connect(self):
        self.tb = TriviaBot()  
        if self.tb.valid:
            self.connect_button.setText("Disconnect")
            self.connection_active = True
            logging.debug("Starting connect loop")
            iternum = 0
            while self.tb.valid:
                iternum += 1
                if iternum % 120 == 0:
                    # only update once every second
                    self.update_gui() 
                self.tb.main_loop(command_line_mode = False)
                QtCore.QCoreApplication.processEvents()
                time.sleep(1/120)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error message")
            msg.setText("Error message:\n%s" % self.tb.error_msg)
            msg.exec_()
            
    def hide_other_buttons(self):
        self.trivia_start_button.setVisible(False)
        self.trivia_skip_button.setVisible(False)
        self.trivia_endq_button.setVisible(False)
        self.trivia_startq_button.setVisible(False)
        self.trivia_start_button.setText("Start Trivia")
    def end_connection(self):
        logging.debug("Ending connection.")
        self.connection_active = False
        self.connect_button.setText("Connect")
        self.hide_other_buttons()
        self.tb.stop_bot()



# SETTINGS
# TriviaBot object sets up and manages Session objects
        
class TriviaBot(object):
    
    def __init__(self):
        logging.debug("Begin setting up Trivia Bot...")
        self.valid = True
        self.trivia_active = False
        self.error_msg = ""
        self.active_session = NullSession()
        with open(os.path.join('config','trivia_config.yml'),'r') as f:
            temp_config = yaml.safe_load(f)
            self.validate_trivia_config(temp_config, os.path.abspath(f.name))
        with open(os.path.join('config','auth_config.yml'),'r') as f:
            temp_config = yaml.safe_load(f)
            self.validate_auth_config(temp_config)
            
        if self.valid:
            try:
                logging.debug("Setting up Chat Bot...")
                self.cb = ChatBot(self.auth_config)
            except:
                logging.debug("Failure to connect to Twitch chat. Check auth config and retry")
                self.valid = False
            self.admin_commands_list = {'!triviastart':self.start_session,
                                  '!stopbot':self.stop_bot,
                                  '!loadsession':self.load_trivia_session,
                                  '!savesession':self.save_trivia_session}
            
            self.commands_list = {'!score':self.check_active_session_score}
            self.admins = [i.strip() for i in self.trivia_config['admins'].split(",")]
                
            logging.debug("Finished setting up Trivia Bot.")
        else:
            logging.debug("Invalid setup - please check trivia_config.yml file")
            
            
    def validate_trivia_config(self,temp_config,config_path):
        for k, v in temp_config.items():
            if k == 'filename':
                if not v.endswith(".csv"):
                    self.error_msg = "Config error: Filename %s does not end with .csv" % v
                    logging.debug(self.error_msg)
                    self.valid = False
            elif k in ['question_count','hint_time1','hint_time2','skip_time','question_delay','question_bonusvalue']:
                if type(v) != int:
                    self.error_msg = "Config error: Error with %s -> %s not being an integer" % (k,v)
                    logging.debug(self.error_msg)
                    self.valid = False
            elif k == 'mode':
                if v not in ['single','poll','poll2']:
                    self.error_msg = "Config error: Mode must be 'single', 'poll', 'poll2'"
                    logging.debug(self.error_msg)
                    self.valid = False
            elif k == 'admins':
                if type(v) != str:
                    self.error_msg = "Config error: Admins must be text only, separated by commas"
                    logging.debug(self.error_msg)
                    self.valid = False
            elif k == 'order':
                if v not in ['random','ordered']:
                    self.error_msg = "Config error: Order must be 'ordered' or 'random' only"
                    logging.debug(self.error_msg)
                    self.valid = False
            elif k == 'music_mode':
                if type(v) != bool:
                    self.error_msg = "Config error: Music mode must be set to true or false"
                    logging.debug(self.error_msg)
                    self.valid = False                 
                if v == True:
                    if "poll2" not in temp_config['mode']:
                        self.error_msg = "Config error: When using music mode, mode 'poll2' must be chosen"
                        logging.debug(self.error_msg)
                        self.valid = False
                    if "infinite" not in temp_config['length']:
                        self.error_msg = "Config error: When using music mode, length 'infinite' must be chosen"
                        logging.debug(self.error_msg)
                        self.valid = False
                    

        if self.valid:
            logging.debug("Passed trivia_config validation.")
            self.trivia_config = temp_config
            self.trivia_config['path_dir'] = os.path.dirname(config_path)
            
    def validate_auth_config(self,temp_config):
        for k, v in temp_config.items():
            if k == 'host':
                if v != 'irc.twitch.tv':
                    logging.debug("Config issue: Host name %s is not default irc.twitch.tv - change at discretion only" % v)
            elif k == 'port':
                if int(v) != 6667:
                    logging.debug("Config issue: Port %s is not default 6667 - change at discretion only" % v)
            elif k == 'nick':
                if type(k) != str:
                    self.error_msg = "Config error: Bot name %s should be text string only" % v
                    logging.debug(self.error_msg)
                    self.valid = False
            elif k == 'pass':
                if "oauth:" not in v:
                    self.error_msg = "Config error: Invalid password %s. Password should be in format 'oauth:xxx'" % v
                    logging.debug(self.error_msg)
                    self.valid = False
            elif k == 'chan':
                if "#" in v or type(v) != str:
                    self.error_msg = "Config error: Invalid channel name %s. Channel name should be text only with NO number sign" % v
                    logging.debug(self.error_msg)
                    self.valid = False
            
                    

        if self.valid:
            logging.debug("Passed auth_config validation.")
            self.auth_config = temp_config
        
    def start_session(self, start_new_override=True):
        logging.debug("Starting session...")
        if not self.trivia_active:
            if not self.active_session or start_new_override: #if there's already a session, ignore, unless from command
                self.active_session = Session(self.cb, self.trivia_config)    
            self.active_session.trivia_status = "Active"
            logging.debug(self.active_session.trivia_status)
            self.cb.s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            
            # setup
            try:
                if self.trivia_config['length'] == 'infinite':
                    self.cb.send_message("Trivia has begun! Infinite question mode. Trivia will start in %s seconds." % (self.active_session.session_config['question_delay']))
                else:
                    self.cb.send_message("Trivia has begun! Question Count: %s. Trivia will start in %s seconds." % (self.active_session.question_count, self.active_session.session_config['question_delay']))
                time.sleep(self.active_session.session_config['question_delay'])
                # get first question, ask, then begin loop
                self.active_session.trivia_active = True
                self.trivia_active = True
                self.active_session.call_question()
        
            except:
                logging.debug("Error on session %s" % traceback.print_exc())
        else:
            logging.debug("Trivia active - ignoring command to begin session.")
            
    def save_trivia_session(self):
        '''
        dump trivia session to pickle file
        '''
        if self.active_session and self.trivia_active:
            if self.active_session.trivia_active:
                save_session = self.active_session
                save_session.cb = None
                with open('latest_session.p', 'wb') as p:
                    pickle.dump(save_session,p)
                self.active_session.cb = self.cb
                logging.debug("Latest trivia session saved.")
        else:
            logging.debug("No trivia session saved.")

    def load_trivia_session(self):
        '''
        load trivia session to pickle file
        '''
        if not self.trivia_active:
            with open('latest_session.p', 'rb') as p:
                load_session = pickle.load(p)
                load_session.cb = self.cb
                self.active_session = load_session
            
            logging.debug("Latest trivia session loaded.")
            self.cb.send_message("Latest trivia session loaded. Beginning trivia...")
            self.start_session(False)
            
        else:
            if self.trivia_active:
                logging.debug("Trivia session active, cannot load during session.")
            else:
                logging.debug("No trivia session loaded.")

        
    def stop_bot(self):
        self.cb.send_message("Ending trivia bot. See you next trivia session!")
        self.valid = False
        try:
            self.active_session.valid = False
            self.active_session.trivia_active = False
        except:
            pass
    def handle_triviabot_message(self,username, message):
        '''
        This is the main function that decides what to do based on the latest message that came in
        For the TRIVIA BOT, primarily used for commands
        '''
        if message:
            #user = self.check_user(username) ########## TO DO

            if message in self.admin_commands_list.keys() and username in self.admins:
                func = self.admin_commands_list[message]
                if message == '!score':
                    func(username)
                else:
                    func()

            if message in self.commands_list.keys():
                func = self.commands_list[message]
                if message == '!score':
                    func(username)
                else:
                    func()
            
    def check_active_session_score(self, username):
        '''
        If there's an active session that has not yet been replaced (meaning, the last active 
        session after a game is over), this will allow users to call their scores
        '''
        if self.active_session != None and not self.active_session.trivia_active:
            user = self.active_session.check_user(username)
            # anti spam measure
            if user.validate_message_time():
                if user:
                    self.active_session.check_user_score(user, from_trivia_bot=True)
                else:
                    self.cb.send_message("%s had no points in the last game." % (username))

        
    def handle_active_session(self):
        username, message, clean_message = self.cb.retrieve_messages()
        
        self.handle_triviabot_message(username, clean_message)
        if message and username !='tmi':
            logging.debug(username)
            logging.debug(self.cb.bot_config['nick'])
            logging.debug("Message received:\n%s " % message)
        self.active_session.check_actions()   
        if self.active_session.session_config['mode'] == 'poll' or self.active_session.session_config['mode'] == 'poll2':
            self.active_session.manage_poll_question()
        self.active_session.handle_session_message(username, clean_message)

    def main_loop(self, command_line_mode = True):
        '''
        The main loop is always running from the start
        While trivia is not active, it will check only handle_triviabot_message for incoming messages
        While trivia is active, it will delegate to the active session
        '''
        
        if command_line_mode:
            iternum = 0
            while self.valid:
                iternum += 1
                if iternum % 300 == 0:
                    try:
                        logging.debug("Iternum %s : trivia_active %s active_session.trivia_active %s" % (iternum, self.trivia_active, self.active_session.trivia_active))
                    except:
                        logging.debug("Iternum %s : %s" % (iternum, self.trivia_active))
                        
                if self.active_session.trivia_active:
                    self.handle_active_session()
                else:
                    username, message, clean_message = self.cb.retrieve_messages()
        
                    if message and username !='tmi':
                        logging.debug(username)
                        logging.debug(self.cb.bot_config['nick'])
                        logging.debug("Message received:\n%s " % message)
                        
        
                    if message:
                        if not self.trivia_active: #when a session is NOT running
                            self.handle_triviabot_message(username, clean_message)
                        
                            
                    if self.trivia_active: # when a session is running
                        # check every iteration if trivia is active or not, to set the trivia bot to be inactive
                        if not self.active_session.trivia_active:
                            logging.debug("Setting trivia to inactive based on active_session...")
                            self.trivia_active = False
                        pass


                        
                
    
                time.sleep(1 / 120)
            logging.debug("Trivia bot no longer valid, ending program.")
        else:
            # when not in command line mode, the window program will handle the looping
            if self.active_session.trivia_active:
                self.handle_active_session()
            else:
                username, message, clean_message = self.cb.retrieve_messages()
    
                if message and username !='tmi':
                    logging.debug(username)
                    logging.debug(self.cb.bot_config['nick'])
                    logging.debug("Message received:\n%s " % message)
                    
    
                if message:
                    if not self.trivia_active: #when a session is NOT running
                        
                        # if theres a command thats recognized, the loop may happen elsewhere
                        # this happens with !triviastart 
                        self.handle_triviabot_message(username, clean_message)
                    
                        
                if self.trivia_active: # when a session is running
                    # check every iteration if trivia is active or not, to set the trivia bot to be inactive
                    if not self.active_session.trivia_active:
                        logging.debug("Setting trivia to inactive based on active_session...")
                        self.trivia_active = False
                    pass


if __name__ == '__main__':
    main_window = MainWindow()
    main_window.window.show()
    main_window.app.exec_()
