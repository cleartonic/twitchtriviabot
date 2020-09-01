import logging
import time
import traceback

from .triviabot import TriviaBot

from PyQt5.QtWidgets import QLabel, QFrame, QLineEdit, QPushButton, QCheckBox, QApplication, QMainWindow, \
                            QFileDialog, QDialog, QScrollArea, QMessageBox, QWidget, QTextEdit
from PyQt5 import QtCore, QtGui, QtTest
from PyQt5.QtGui import QPixmap, QIntValidator, QPalette, QColor
from PyQt5.QtCore import QThread, pyqtSignal, QTimer

class MainWindow(QWidget):
    SCREEN_HEIGHT = 400
    SCREEN_WIDTH = 320
    
    def __init__(self, version):
        self.BORDER = False
        self.app = QApplication([])
        super(MainWindow, self).__init__()
        self.version = version
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
            

        self.title_bar_text = QLabel("Twitch Trivia Bot version %s" % self.version,self.window)
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
