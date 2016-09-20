import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+"/algo")
from affine import *
from shift import *

from socket import *

from PyQt4 import QtGui
from PyQt4 import QtGui
from PyQt4.QtCore import QThread, QRect
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from time import strftime # For message timestamps

_PORT 	= 13000
_BUFFER = 1024

# This is a test comment (git)

class sender_thread(QThread):

	def __init__(self):
		QThread.__init__(self)

	def run(self):
		# Called when the thread is started
		self.port = _PORT

	def connect(self, host):
		
		self.host = host
		self.addr = (host, self.port)
		self.UDPSock = socket(AF_INET, SOCK_DGRAM)
		print "Sender thread online."
		return True

	def send(self, message):

		self.UDPSock.sendto(str(message), self.addr)

class receive_thread(QThread):

	def __init__(self):
		QThread.__init__(self)

	def run(self):
		# Called when the thread is started
		print "Receiver thread online."
		host 	= ""
		port 	= _PORT
		buf 	= _BUFFER
		
		addr 	= (host, port)
		UDPSock = socket(AF_INET, SOCK_DGRAM)
		UDPSock.bind(addr)

		while True:
			
			(data, addr) = UDPSock.recvfrom(buf)
			self.emit(SIGNAL("got_message(QString)"), data)

		UDPSock.close()

class main_window(QtGui.QWidget):

	def __init__(self, parent=None):

		super(main_window, self).__init__()
		self.IP_validator = QtGui.QIntValidator(0, 999, self)
		self.fetchIP()
		self.initUI()
		#self.

	def fetchIP(self):

		self.cur_IP = gethostbyname(gethostname())
		self.cur_split_IP = self.cur_IP.split(".")

	def initUI(self):

		self.resize(400, 650)
		self.setWindowTitle("Wifi Local Messenger")

		self.cur_IP_label = QtGui.QLabel("Your Local IP Address: ", self)
		self.cur_IP_label.resize(self.cur_IP_label.sizeHint())
		self.cur_IP_label.move(25, 25)
		
		self.cur_IP_text1 = QtGui.QLineEdit(self.cur_split_IP[0], self)
		self.cur_IP_text1.move(210, 23) # 180
		self.cur_IP_text1.setEnabled(False)
		self.cur_IP_text1.setFixedWidth(30)

		self.cur_IP_text2 = QtGui.QLineEdit(self.cur_split_IP[1], self)
		self.cur_IP_text2.move(250, 23) # 220
		self.cur_IP_text2.setEnabled(False)
		self.cur_IP_text2.setFixedWidth(30)

		self.cur_IP_text3 = QtGui.QLineEdit(self.cur_split_IP[2], self)
		self.cur_IP_text3.move(290, 23) # 260
		self.cur_IP_text3.setEnabled(False)
		self.cur_IP_text3.setFixedWidth(30)

		self.cur_IP_text4 = QtGui.QLineEdit(self.cur_split_IP[3], self)
		self.cur_IP_text4.move(330, 23) # 300
		self.cur_IP_text4.setEnabled(False)
		self.cur_IP_text4.setFixedWidth(30)

		dot1 = QtGui.QLabel(".",self)
		dot1.move(243,30) # 211

		dot2 = QtGui.QLabel(".", self)
		dot2.move(283, 30) # 251

		dot3 = QtGui.QLabel(".", self)
		dot3.move(323, 30) # 291

		self.other_IP_label = QtGui.QLabel("Enter Local IP Of Other User: ", self)
		self.other_IP_label.resize(self.other_IP_label.sizeHint())
		self.other_IP_label.move(25, 75)
		
		self.other_IP_text1 = QtGui.QLineEdit("", self)
		self.other_IP_text1.move(210, 73)
		self.other_IP_text1.setEnabled(True)
		self.other_IP_text1.setFixedWidth(30)
		self.other_IP_text1.textChanged.connect(self.otherIPChanged)
		self.other_IP_text1.setValidator(self.IP_validator)

		self.other_IP_text2 = QtGui.QLineEdit("", self)
		self.other_IP_text2.move(250, 73)
		self.other_IP_text2.setEnabled(True)
		self.other_IP_text2.setFixedWidth(30)
		self.other_IP_text2.textChanged.connect(self.otherIPChanged)
		self.other_IP_text2.setValidator(self.IP_validator)

		self.other_IP_text3 = QtGui.QLineEdit("", self)
		self.other_IP_text3.move(290, 73)
		self.other_IP_text3.setEnabled(True)
		self.other_IP_text3.setFixedWidth(30)
		self.other_IP_text3.textChanged.connect(self.otherIPChanged)
		self.other_IP_text3.setValidator(self.IP_validator)

		self.other_IP_text4 = QtGui.QLineEdit("", self)
		self.other_IP_text4.move(330, 73)
		self.other_IP_text4.setEnabled(True)
		self.other_IP_text4.setFixedWidth(30)
		self.other_IP_text4.textChanged.connect(self.otherIPChanged)
		self.other_IP_text4.setValidator(self.IP_validator)


		dot4 = QtGui.QLabel(".",self)
		dot4.move(243,80)

		dot5 = QtGui.QLabel(".", self)
		dot5.move(283, 80)

		dot6 = QtGui.QLabel(".", self)
		dot6.move(323, 80)

		self.connect_button = QtGui.QPushButton("Connect", self)
		self.connect_button.setEnabled(False)
		self.connect_button.move(160, 110)
		self.connect_button.clicked.connect(self.connect)

		self.divider = QtGui.QFrame(self)
		self.divider.setFrameShape(QFrame.HLine)
		self.divider.move(30, 145)
		self.divider.setFixedWidth(340)

		self.textbox = QtGui.QTextEdit(self)
		self.textbox.move(20, 180)
		self.textbox.setFixedWidth(360)
		self.textbox.setFixedHeight(400)

		self.sendbox = QtGui.QLineEdit("", self)
		self.sendbox.move(20, 600)
		self.sendbox.setFixedWidth(250)

		self.send_button = QtGui.QPushButton("Send", self)
		self.send_button.resize(self.send_button.sizeHint())
		self.send_button.clicked.connect(self.send)
		self.send_button.move(306, 598)
		self.send_button.setEnabled(False)
		
		self.send_thread = sender_thread()
		self.send_thread.start()
		self.rec_thread  = receive_thread()
		self.rec_thread.start()

		QtCore.QObject.connect(self.rec_thread, QtCore.SIGNAL("got_message(QString)"), self.receive)
		QtCore.QObject.connect(self, QtCore.SIGNAL("send_message(QString)"), self.send_thread.send)

		self.received_messages 	= []
		self.sent_messages 		= []

		self.connected = False
		self.show()

	def keyPressEvent(self, event):
		
		# Responds when user clicks key
		if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
			self.send()

	def receive(self, message):

		self.received_messages.append(message)
		self.textbox.append("[THEM - "+strftime("%H:%M:%S")+"] --> "+message)

	def send(self):

		if self.connected == False:
			return
		else:

			self.send_thread.send(self.sendbox.text())
			self.sent_messages.append(str(self.sendbox.text()))
			self.textbox.append("[YOU - "+strftime("%H:%M:%S")+"] --> "+self.sendbox.text())
			self.sendbox.setText("")

	def connect(self):

		if self.send_thread.connect(self.other_IP) == True:
			self.connect_button.setText("Connected")
			self.connected = True
			self.send_button.setEnabled(True)
		else:
			print "ERROR: Could not connect to other IP"

	def otherIPChanged(self):

		self.other_split_IP = []
		self.other_split_IP.append(self.other_IP_text1.text())
		self.other_split_IP.append(self.other_IP_text2.text())
		self.other_split_IP.append(self.other_IP_text3.text())
		self.other_split_IP.append(self.other_IP_text4.text())

		self.other_IP = self.other_split_IP[0]+"."+self.other_split_IP[1]+"."+self.other_split_IP[2]+"."+self.other_split_IP[3]

		self.other_IP_valid = True

		for section in self.other_split_IP:
			if section == "":
				self.other_IP_valid = False

		if self.other_IP_valid:
			self.connect_button.setEnabled(True)
		else:
			self.connect_button.setEnabled(False)

	def updateCurrentIP(self):

		self.fetchIP()
		self.cur_IP_text1.setText(self.cur_split_IP[0])
		self.cur_IP_text2.setText(self.cur_split_IP[1])
		self.cur_IP_text3.setText(self.cur_split_IP[2])
		self.cur_IP_text4.setText(self.cur_split_IP[3])

def main():

	app = QtGui.QApplication(sys.argv)
	app.setWindowIcon(QtGui.QIcon('resources/icon_300x300.png'))
	_ = main_window()
	sys.exit(app.exec_())



if __name__ == '__main__':
	main()

