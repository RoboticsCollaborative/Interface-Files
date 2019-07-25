#!/usr/bin/env python

# -*- coding: utf-8 -*-

#
#
#
# Form implementation generated from reading ui file 'glove_gui_teleop.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
#
#
########################
########################
#####    IMPORTS   #####
########################
########################



#Python widget imports
from PyQt4 import QtCore, QtGui
#ROS + standard imports
import math
import rospy
#Ros standard message types
from std_msgs.msg import Float32
from std_msgs.msg import Float64MultiArray
#Custom message type ROS interface
from rdda_interface.msg import JointCommands
from rdda_interface.msg import JointStates
#Relative path and child program imports
import os
from sys import executable
import subprocess
from subprocess import Popen
import inspect





#Check imports
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)









#########################
#########################
#####    UI CLASS   #####
#########################
#########################
class Ui_Form(object):





    #########################
    #    Callback Methods   #
    #########################
    #Teleop theta call
    def theta(self):
	theta1 = self.slideT1.value()
	theta2 = self.slideT2.value()
	#thetas in degrees are converted into radians
	theta1 =  (0.01745327777*theta1)
	theta2 =  (0.01745327777*theta2)
	self.teleopTheta = ((theta1 + theta2), (theta2 - theta1))
	print('Theta one has been changed to: '+ str(theta1))
	print('Theta two has been changed to: '+ str(theta2))
	self.pubTOut.publish(self.teleopTheta)
	self.pubToNet()

    #Home reset callbacks
    def homeTheta1(self):
	signalOut = 111
	self.pubHome.publish(signalOut)
    def homeTheta2(self):
	signalOut = 222
	self.pubHome.publish(signalOut)
    #Additional callbacks
    def maxVelocity(self):
	vel = float(float(self.slideVelocity.value())/20.0)
	velLabel = str(vel)
        self.labelVelocity.setText(_translate("Form", velLabel, None))
	velSat = Float64MultiArray()
	velSat.data = [vel]
	print('Maximum velocity has been changed to: ' + velLabel)
	self.pubVelSat.publish(velSat)
	self.vel_sat = (vel, vel)
	self.pubToNet()
    def maxTorque(self):
	tau = float(float(self.slideTorque.value())/20.0)
	tauLabel = str(tau)
        self.labelTorque.setText(_translate("Form", tauLabel, None))
	tauSat = Float64MultiArray()
	tauSat.data = [tau]
	print('Maximum torque has been changed to: ' + tauLabel)
	self.pubTauSat.publish(tauSat)
	self.tau_sat = (tau, tau)
	self.pubToNet()
    def stiffness(self):
	stiffVal = float(float(self.slideStiffness.value())/5)
	stiffLabel = str(stiffVal)
        self.labelStiffness.setText(_translate("Form", stiffLabel, None))
	stiffness = Float64MultiArray()
	stiffness.data = [stiffVal]
	print('Stiffness has been changed to: ' + stiffLabel)
	self.pubStiffness.publish(stiffness)
	self.stiff_val = (stiffVal, stiffVal)
	self.pubToNet()
    def faa(self):
	faaVal = self.slideFAA.value()
	print('Frequency anti alias value has been changed to: ' + str(faaVal))
	self.pubFAA.publish(faaVal)
	self.faa_val = faaVal
	self.pubToNet()





############################################

############################################
#		    PUB			   #
############################################
    #Publish
    def pubToNet(self):
	if(self.mode != 2):
	    self.offset_ref = (self.pos_ref[0] + self.offset[0], self.pos_ref[1] + self.offset[1]) 
	    self.amp_ref = (float(self.amplify*(float(self.offset_ref[0]))), float(self.amplify*(float(self.offset_ref[1]))))
	    #Check for values outside of min/max parameter
	    if(self.amp_ref[0] >= self.mPar):
	        self.amp_ref = (self.mPar, self.amp_ref[1])
	    elif(self.amp_ref[0] <= ((-1)*(self.mPar))):
	        self.amp_ref = ((-1)*(self.mPar), self.amp_ref[1])
	    if(self.amp_ref[1] >= self.mPar):
	        self.amp_ref = (self.amp_ref[0], self.mPar)
	    elif(self.amp_ref[1] <= ((-1)*(self.mPar))):
	        self.amp_ref = (self.amp_ref[0], (-1)*(self.mPar))
	elif(self.mode == 2):
	    self.amp_teleop = (float(self.amplify*(float(self.teleopTheta[0]))), float(self.amplify*(float(self.teleopTheta[1]))))
	    #Check for values outside of min/max parameter
	    if(self.amp_teleop[0] >= self.mPar):
	        self.amp_teleop = (self.mPar, self.amp_teleop[1])
	    elif(self.amp_teleop[0] <= ((-1)*(self.mPar))):
	        self.amp_teleop = ((-1)*(self.mPar), self.amp_teleop[1])
	    if(self.amp_teleop[1] >= self.mPar):
	        self.amp_teleop = (self.amp_teleop[0], self.mPar)
	    elif(self.amp_teleop[1] <= ((-1)*(self.mPar))):
	        self.amp_teleop = (self.amp_teleop[0], (-1)*(self.mPar))
	#State sensitive publishing (blocks signals while in safe mode)
	#While Safe
	if(self.mode == 0):
	    self.joint_pub.publish((0.0, 0.0), (1.0, 1.0), (0.0, 0.0), (0.0, 0.0), 10)
	#While DAQ
	elif(self.mode == 1):
	    self.joint_pub.publish(self.amp_ref, self.vel_sat, self.tau_sat, self.stiff_val, 10)
	#While Teleop
	elif(self.mode == 2):
	    self.joint_pub.publish(self.amp_teleop, self.vel_sat, self.tau_sat, self.stiff_val, 10)
	elif(self.mode == 3):
	    self.joint_pub.publish(self.state, (5.0, 5.0), (5.0, 5.0), (0.0, 0.0), 10)
############################################
#		   PUB			   #
############################################

############################################





    #####################################
    #    Specialized Callback Methods   #
    #####################################
    #DAQ callback
    def posCallback(self, data):
	self.pos_ref = (data.data[0], data.data[1])
	self.pubToNet()
    #Gamma callback
    def gammaCallback(self, data):
	self.gamma = (data.data[0], data.data[1])
	self.pubGamma.publish(data)
    #Stimulate gamma topic
    def stim(self, data):
	gam = Float64MultiArray()
	gam.data = [(self.gamma[0]), (self.gamma[1])]
	print(gam)
	self.pubGamma.publish(gam)
    #Amplify callback
    def amp(self):
	self.amplify = (float(float(self.slideAmp.value()))/20.0)-10.0
	self.labelAmp.setText(_translate("Form", str(self.amplify), None))
    #maxParameter callback
    def mParCallback(self):
	self.mPar = (float(self.slideMPar.value())/100)
	self.labelMPar.setText(_translate("Form", str(self.mPar), None))
    #Resize callback
    def resizeCallback(self):
	self.resizeVal = (float(self.slideResize.value())/10)
	self.resizeUi(self.resizeVal)
	self.labelResize.setText(_translate("Form", str(self.resizeVal), None))
    #Get motor position
    def stateCallback(self, data):
	self.state = data.act_pos

    #Kill child program
    def abort(self):
	if(self.mode == 1):
	    self.proc.kill()
	    os.system('clear')
	    self.mode = 0
	    self.labelMode.setText('   SAFE')
	else:
	    print("No child process to kill, mode not set to DAQ")
    #Relative path of file
    def getFileName(self):
	dirname = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
	self.fileName = os.path.join(dirname, 'ros_mc_signal_teleop4.py')

    #Change the operation mode
    def modeChange(self):
        if(self.mode == 0):
	    self.labelMode.setText('   DAQ')
	    self.getFileName()
	    self.proc = subprocess.Popen(self.fileName, shell = False )
	    self.mode = 1
	elif(self.mode == 1):
	    self.labelMode.setText(' TELEOP')
	    self.proc.kill()
	    os.system('clear')
	    self.mode = 2
	elif(self.mode == 2):
	    self.labelMode.setText('   SAFE')
	    self.mode = 0

    #Set custom gripper state
    def setHome(self):
	#First click
	if(self.homeState == 0):
	    self.homeState = 1
	    self.lastState = self.mode
	    self.mode = 3
	    if(self.stateCnt == 0):
	        self.oState = self.state
	        self.stateCnt = 1
	#Second click
	elif(self.homeState == 1):
	    self.mode = self.lastState
	    offset1 = self.state[0] - self.oState[0]
	    offset2 = self.state[1] - self.oState[1]
	    self.offset = (offset1, offset2)
	    self.homeState = 0
	    self.pubToNet()





    #########################
    #    Ui Setup Method    #
    #########################
    def setupUi(self, Form):
	#Setup ROS publishers
	self.pubTOut = rospy.Publisher('gui_theta_teleop', Float32, queue_size=10)
        self.pubHome = rospy.Publisher('gui_home', Float32, queue_size=10)
	self.pubVelSat = rospy.Publisher('gui_vel_sat', Float64MultiArray, queue_size=10)
	self.pubTauSat = rospy.Publisher('gui_tau_sat', Float64MultiArray, queue_size=10)
	self.pubStiffness = rospy.Publisher('gui_stiffness', Float64MultiArray, queue_size=10)
	self.pubFAA = rospy.Publisher('gui_faa', Float32, queue_size=10)
	self.pubGamma = rospy.Publisher('gamma_keep', Float64MultiArray, queue_size = 10)

	#Initialize ROS node
        rospy.init_node('gloveGUITeleop', anonymous=True)

	#Link ROS subscribers to callback functions
	rospy.Subscriber('daq_pos_ref', Float64MultiArray, self.posCallback)
	rospy.Subscriber('gamma_store', Float64MultiArray, self.gammaCallback)
	rospy.Subscriber('stimulate', Float32, self.stim)

	self.joint_pub = rospy.Publisher("rdd/joint_cmds", JointCommands, queue_size=1)
	rospy.Subscriber("rdd/joint_stats", JointStates, self.stateCallback)
	
	#Object variables
	self.gamma = (0.0, 0.0)
	self.pos_ref = (0.0, 0.0)
	self.offset_ref = (0.0, 0.0)
	self.amp_ref = (0.0, 0.0)
	self.teleopTheta = (0.0, 0.0)
	self.amp_teleop = (0.0, 0.0)
	self.vel_sat = (1.0, 1.0)
	self.tau_sat = (1.0, 1.0)
	self.stiff_val = (1.0, 1.0)
	self.oState = (0.0, 0.0)
	self.state = (0.0, 0.0)
	self.offset = (0.0, 0.0)
	self.faa_val = 10
	self.mode = 0
	self.amplify = 1.0
        self.mPar = 1.0
	self.startCnt = 0
	self.fileName = ""
	self.homeState = 0
	self.lastState = 0
	self.stateCnt = 0

	#Object resize variables + variable object
	self.resizeVal = 1.0
	self.Shape = Form

	#Define widget dimmensions
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(390, 635)

	#Main text
        self.textMain = QtGui.QTextEdit(Form)
        self.textMain.setGeometry(QtCore.QRect(130, 15, 130, 50))
        self.textMain.setObjectName(_fromUtf8("textEdit"))
	#Home text
        self.textH1 = QtGui.QTextEdit(Form)
        self.textH1.setGeometry(QtCore.QRect(50, 115, 100, 40))
        self.textH1.setObjectName(_fromUtf8("textEdit_2"))
        self.textH2 = QtGui.QTextEdit(Form)
        self.textH2.setGeometry(QtCore.QRect(240, 115, 100, 40))
        self.textH2.setObjectName(_fromUtf8("textEdit_3"))
	#Text for additional sliders
        self.textVelocity = QtGui.QTextEdit(Form)
        self.textVelocity.setGeometry(QtCore.QRect(10, 205, 120, 30))
        self.textVelocity.setObjectName(_fromUtf8("textEdit_4"))
        self.textTorque = QtGui.QTextEdit(Form)
        self.textTorque.setGeometry(QtCore.QRect(10, 245, 121, 31))
        self.textTorque.setObjectName(_fromUtf8("textEdit_5"))
        self.textStiffness = QtGui.QTextEdit(Form)
        self.textStiffness.setGeometry(QtCore.QRect(10, 285, 120, 30))
        self.textStiffness.setObjectName(_fromUtf8("textEdit_6"))
        self.textFAA = QtGui.QTextEdit(Form)
        self.textFAA.setGeometry(QtCore.QRect(10, 325, 120, 30))
        self.textFAA.setObjectName(_fromUtf8("textEdit_7"))
	#Text for mode
        self.textMode = QtGui.QTextEdit(Form)
        self.textMode.setGeometry(QtCore.QRect(10, 365, 120, 30))
        self.textMode.setObjectName(_fromUtf8("textEdit_8"))
	#Text for amplitude
        self.textAmp = QtGui.QTextEdit(Form)
        self.textAmp.setGeometry(QtCore.QRect(10, 475, 120, 30))
        self.textAmp.setObjectName(_fromUtf8("textEdit_9"))
	#Text for mPar
        self.textMPar = QtGui.QTextEdit(Form)
        self.textMPar.setGeometry(QtCore.QRect(10, 515, 120, 30))
        self.textMPar.setObjectName(_fromUtf8("textEdit_10"))
	#Text for resize
        self.textResize = QtGui.QTextEdit(Form)
        self.textResize.setGeometry(QtCore.QRect(10, 555, 120, 30))
        self.textResize.setObjectName(_fromUtf8("textEdit_11"))
	#Text for setting home
	self.textSetHome = QtGui.QTextEdit(Form)
        self.textSetHome.setGeometry(QtCore.QRect(10, 595, 120, 30))
        self.textSetHome.setObjectName(_fromUtf8("textEdit_12"))

	#Home pushbuttons
        self.pushHome1 = QtGui.QPushButton(Form)
        self.pushHome1.setGeometry(QtCore.QRect(50, 165, 100, 27))
        self.pushHome1.setObjectName(_fromUtf8("pushButton"))
        self.pushHome2 = QtGui.QPushButton(Form)
        self.pushHome2.setGeometry(QtCore.QRect(240, 165, 100, 27))
        self.pushHome2.setObjectName(_fromUtf8("pushButton_2"))
	#Mode pushbutton
        self.pushMode = QtGui.QPushButton(Form)
        self.pushMode.setGeometry(QtCore.QRect(240, 365, 120, 30))
        self.pushMode.setObjectName(_fromUtf8("pushButton_3"))
	#ABORT pushbutton
        self.pushAbort = QtGui.QPushButton(Form)
        self.pushAbort.setGeometry(QtCore.QRect(100, 405, 200, 60))
        self.pushAbort.setObjectName(_fromUtf8("pushButton_4"))
	#Reset pushbuttons
        self.pushResetBuild = QtGui.QPushButton(Form)
        self.pushResetBuild.setGeometry(QtCore.QRect(10, 10, 110, 40))
        self.pushResetBuild.setObjectName(_fromUtf8("pushButton_5"))
        self.pushResetMemory = QtGui.QPushButton(Form)
        self.pushResetMemory.setGeometry(QtCore.QRect(270, 10, 110, 40))
        self.pushResetMemory.setObjectName(_fromUtf8("pushButton_6"))
	#Home setting pushbuttons
        self.pushSetHome = QtGui.QPushButton(Form)
        self.pushSetHome.setGeometry(QtCore.QRect(200, 595, 110, 30))
        self.pushSetHome.setObjectName(_fromUtf8("pushButton_7"))

	#Teleop sliders
        self.slideT1 = QtGui.QSlider(Form)
        self.slideT1.setGeometry(QtCore.QRect(20, 75, 160, 30))
        self.slideT1.setMaximum(360)
        self.slideT1.setOrientation(QtCore.Qt.Horizontal)
        self.slideT1.setObjectName(_fromUtf8("horizontalSlider"))
        self.slideT2 = QtGui.QSlider(Form)
        self.slideT2.setGeometry(QtCore.QRect(210, 75, 160, 30))
        self.slideT2.setMaximum(360)
        self.slideT2.setOrientation(QtCore.Qt.Horizontal)
        self.slideT2.setObjectName(_fromUtf8("horizontalSlider_2"))
	#Additional slider
        self.slideVelocity = QtGui.QSlider(Form)
        self.slideVelocity.setGeometry(QtCore.QRect(220, 205, 160, 30))
        self.slideVelocity.setOrientation(QtCore.Qt.Horizontal)
        self.slideVelocity.setObjectName(_fromUtf8("horizontalSlider_3"))
	self.slideVelocity.setMinimum(0)
	self.slideVelocity.setMaximum(100)
	self.slideVelocity.setValue(20)
	self.slideVelocity.setTickInterval(1)
	#Torque slider
        self.slideTorque = QtGui.QSlider(Form)
        self.slideTorque.setGeometry(QtCore.QRect(220, 245, 160, 30))
        self.slideTorque.setOrientation(QtCore.Qt.Horizontal)
        self.slideTorque.setObjectName(_fromUtf8("horizontalSlider_4"))
	self.slideTorque.setMinimum(0)
	self.slideTorque.setMaximum(100)
	self.slideTorque.setValue(20)
	self.slideTorque.setTickInterval(1)
	#Stiffness slider
        self.slideStiffness = QtGui.QSlider(Form)
        self.slideStiffness.setGeometry(QtCore.QRect(220, 285, 160, 30))
        self.slideStiffness.setOrientation(QtCore.Qt.Horizontal)
        self.slideStiffness.setObjectName(_fromUtf8("horizontalSlider_5"))
	self.slideStiffness.setMinimum(0)
	self.slideStiffness.setMaximum (100)
	self.slideStiffness.setValue(5)
	self.slideStiffness.setTickInterval(1)
	#FAA slider
        self.slideFAA = QtGui.QSlider(Form)
        self.slideFAA.setGeometry(QtCore.QRect(220, 325, 160, 30))
        self.slideFAA.setOrientation(QtCore.Qt.Horizontal)
        self.slideFAA.setObjectName(_fromUtf8("horizontalSlider_6"))
	self.slideFAA.setValue(10)
	#Amp slider
        self.slideAmp = QtGui.QSlider(Form)
        self.slideAmp.setGeometry(QtCore.QRect(220, 475, 160, 30))
        self.slideAmp.setOrientation(QtCore.Qt.Horizontal)
        self.slideAmp.setObjectName(_fromUtf8("horizontalSlider_7"))
	self.slideAmp.setMinimum(0)
	self.slideAmp.setMaximum (400)
	self.slideAmp.setValue(220)
	self.slideAmp.setTickInterval(1)
	#mPar slider
        self.slideMPar = QtGui.QSlider(Form)
        self.slideMPar.setGeometry(QtCore.QRect(220, 515, 160, 30))
        self.slideMPar.setOrientation(QtCore.Qt.Horizontal)
        self.slideMPar.setObjectName(_fromUtf8("horizontalSlider_8"))
	self.slideMPar.setMinimum(0)
	self.slideMPar.setMaximum (328)
	self.slideMPar.setValue(100)
	self.slideMPar.setTickInterval(1)
	#Resize slider
        self.slideResize = QtGui.QSlider(Form)
        self.slideResize.setGeometry(QtCore.QRect(220, 555, 160, 30))
        self.slideResize.setOrientation(QtCore.Qt.Horizontal)
        self.slideResize.setObjectName(_fromUtf8("horizontalSlider_9"))
	self.slideResize.setMinimum(10)
	self.slideResize.setMaximum (50)
	self.slideResize.setValue(10)
	self.slideResize.setTickInterval(1)

	#Labels for additional sliders
        self.labelVelocity = QtGui.QLabel(Form)
        self.labelVelocity.setGeometry(QtCore.QRect(150, 210, 60, 20))
        self.labelVelocity.setObjectName(_fromUtf8("label_3"))
        self.labelTorque = QtGui.QLabel(Form)
        self.labelTorque.setGeometry(QtCore.QRect(150, 250, 60, 20))
        self.labelTorque.setObjectName(_fromUtf8("label_4"))
        self.labelStiffness = QtGui.QLabel(Form)
        self.labelStiffness.setGeometry(QtCore.QRect(150, 290, 60, 20))
        self.labelStiffness.setObjectName(_fromUtf8("label_5"))
        self.labelFAA = QtGui.QLabel(Form)
        self.labelFAA.setGeometry(QtCore.QRect(150, 330, 60, 20))
        self.labelFAA.setObjectName(_fromUtf8("label_6"))
	#Label for amp
        self.labelAmp = QtGui.QLabel(Form)
        self.labelAmp.setGeometry(QtCore.QRect(150, 480, 60, 20))
        self.labelAmp.setObjectName(_fromUtf8("label_8"))
	#Label for mPar
        self.labelMPar = QtGui.QLabel(Form)
        self.labelMPar.setGeometry(QtCore.QRect(150, 520, 60, 20))
        self.labelMPar.setObjectName(_fromUtf8("label_9"))
	#Label for resize
        self.labelResize = QtGui.QLabel(Form)
        self.labelResize.setGeometry(QtCore.QRect(150, 555, 60, 20))
        self.labelResize.setObjectName(_fromUtf8("label_10"))
	#Label for mode
        self.labelMode = QtGui.QLabel(Form)
        self.labelMode.setGeometry(QtCore.QRect(150, 355, 60, 50))
        self.labelMode.setObjectName(_fromUtf8("label_7"))
	#Teleop labels
        self.labelT1 = QtGui.QLabel(Form)
        self.labelT1.setGeometry(QtCore.QRect(40, 55, 70, 20))
        self.labelT1.setObjectName(_fromUtf8("label"))
        self.labelT2 = QtGui.QLabel(Form)
        self.labelT2.setGeometry(QtCore.QRect(280, 55, 70, 20))
        self.labelT2.setObjectName(_fromUtf8("label_2"))

	#Ui retranslate
        self.retranslateUi(Form)

	#Create theta teleop objects w/ callbacks
        QtCore.QObject.connect(self.slideT1, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.labelT1.setNum)
	QtCore.QObject.connect(self.slideT1, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.theta)
        QtCore.QObject.connect(self.slideT2, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.labelT2.setNum)
	QtCore.QObject.connect(self.slideT2, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.theta)
	#Create home reset objects w/ callbacks
	QtCore.QObject.connect(self.pushHome1, QtCore.SIGNAL(_fromUtf8("clicked()")), self.homeTheta1)
	QtCore.QObject.connect(self.pushHome2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.homeTheta2)
        QtCore.QMetaObject.connectSlotsByName(Form)
	#Create additional objects w/ callbacks
        QtCore.QObject.connect(self.slideVelocity, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.maxVelocity)
        QtCore.QObject.connect(self.slideTorque, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.maxTorque)
        QtCore.QObject.connect(self.slideStiffness, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.stiffness)
        QtCore.QObject.connect(self.slideFAA, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.labelFAA.setNum)
        QtCore.QObject.connect(self.slideFAA, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.faa)
	#Create specialized objects w/ callbacks
        QtCore.QObject.connect(self.slideAmp, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.amp)
        QtCore.QObject.connect(self.slideMPar, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.mParCallback)
        QtCore.QObject.connect(self.slideResize, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.resizeCallback)
	QtCore.QObject.connect(self.pushMode, QtCore.SIGNAL(_fromUtf8("clicked()")), self.modeChange)
	#Create ABORT object w/ callbacks
	QtCore.QObject.connect(self.pushAbort, QtCore.SIGNAL(_fromUtf8("clicked()")), self.abort)
	#Create Reset objects w/ callbacks
	QtCore.QObject.connect(self.pushResetBuild, QtCore.SIGNAL(_fromUtf8("clicked()")), self.resetBuild)
	QtCore.QObject.connect(self.pushResetMemory, QtCore.SIGNAL(_fromUtf8("clicked()")), self.resetMemory)
	QtCore.QObject.connect(self.pushSetHome, QtCore.SIGNAL(_fromUtf8("clicked()")), self.setHome)





    ##########################
    #    Ui Resize Method    #
    ##########################
    def resizeUi(self, size):
	#Resize variable
	self.rV = size

	#Widget resize
        Form.resize(int(round(390*self.rV)), int(round(635*self.rV)))

	#    TEXT
	#Main text
        self.textMain.setGeometry(QtCore.QRect(int(round(130*self.rV)), int(round(15*self.rV)), int(round(130*self.rV)), int(round(50*self.rV))))
	#Home text
        self.textH1.setGeometry(QtCore.QRect(int(round(50*self.rV)), int(round(115*self.rV)), int(round(100*self.rV)), int(round(40*self.rV))))
        self.textH2.setGeometry(QtCore.QRect(int(round(240*self.rV)), int(round(115*self.rV)), int(round(100*self.rV)), int(round(40*self.rV))))
	#Text for additional sliders
        self.textVelocity.setGeometry(QtCore.QRect(int(round(10*self.rV)), int(round(205*self.rV)), int(round(120*self.rV)), int(round(30*self.rV))))
        self.textTorque.setGeometry(QtCore.QRect(int(round(10*self.rV)), int(round(245*self.rV)), int(round(121*self.rV)), int(round(31*self.rV))))
        self.textStiffness.setGeometry(QtCore.QRect(int(round(10*self.rV)), int(round(285*self.rV)), int(round(120*self.rV)), int(round(30*self.rV))))
        self.textFAA.setGeometry(QtCore.QRect(int(round(10*self.rV)), int(round(325*self.rV)), int(round(120*self.rV)), int(round(30*self.rV))))
	#Text for mode
        self.textMode.setGeometry(QtCore.QRect(int(round(10*self.rV)), int(round(365*self.rV)), int(round(120*self.rV)), int(round(30*self.rV))))
        #Specialized texts resize
        self.textAmp.setGeometry(QtCore.QRect(int(round(10*self.rV)), int(round(475*self.rV)), int(round(120*self.rV)), int(round(30*self.rV))))
        self.textMPar.setGeometry(QtCore.QRect(int(round(10*self.rV)), int(round(515*self.rV)), int(round(120*self.rV)), int(round(30*self.rV))))
        self.textResize.setGeometry(QtCore.QRect(int(round(10*self.rV)), int(round(555*self.rV)), int(round(120*self.rV)), int(round(30*self.rV))))
        self.textSetHome.setGeometry(QtCore.QRect(int(round(10*self.rV)), int(round(595*self.rV)), int(round(120*self.rV)), int(round(30*self.rV))))

	#    PUSHBUTTONS
	#Home pushbutton
        self.pushHome1.setGeometry(QtCore.QRect(int(round(50*self.rV)), int(round(165*self.rV)), int(round(100*self.rV)), int(round(27*self.rV))))
        self.pushHome2.setGeometry(QtCore.QRect(int(round(240*self.rV)), int(round(165*self.rV)), int(round(100*self.rV)), int(round(27*self.rV))))
	#Mode pushbutton
        self.pushMode.setGeometry(QtCore.QRect(int(round(240*self.rV)), int(round(365*self.rV)), int(round(120*self.rV)), int(round(30*self.rV))))
	#ABORT pushbutton
        self.pushAbort.setGeometry(QtCore.QRect(int(round(100*self.rV)), int(round(405*self.rV)), int(round(200*self.rV)), int(round(60*self.rV))))
	#Resize reset pushbuttons
        self.pushResetBuild.setGeometry(QtCore.QRect(int(round(10*self.rV)), int(round(10*self.rV)), int(round(110*self.rV)), int(round(40*self.rV))))
        self.pushResetMemory.setGeometry(QtCore.QRect(int(round(270*self.rV)), int(round(10*self.rV)), int(round(110*self.rV)), int(round(40*self.rV))))
        self.pushSetHome.setGeometry(QtCore.QRect(int(round(200*self.rV)), int(round(595*self.rV)), int(round(110*self.rV)), int(round(30*self.rV))))

	#    SLIDERS
	#Teleop sliders
        self.slideT1.setGeometry(QtCore.QRect(int(round(20*self.rV)), int(round(75*self.rV)), int(round(160*self.rV)), int(round(30*self.rV))))
        self.slideT2.setGeometry(QtCore.QRect(int(round(210*self.rV)), int(round(75*self.rV)), int(round(160*self.rV)), int(round(30*self.rV))))
	#Additional sliders
        self.slideVelocity.setGeometry(QtCore.QRect(int(round(220*self.rV)), int(round(205*self.rV)), int(round(160*self.rV)), int(round(30*self.rV))))
        self.slideTorque.setGeometry(QtCore.QRect(int(round(220*self.rV)), int(round(245*self.rV)), int(round(160*self.rV)), int(round(30*self.rV))))
        self.slideStiffness.setGeometry(QtCore.QRect(int(round(220*self.rV)), int(round(285*self.rV)), int(round(160*self.rV)), int(round(30*self.rV))))
        self.slideFAA.setGeometry(QtCore.QRect(int(round(220*self.rV)), int(round(325*self.rV)), int(round(160*self.rV)), int(round(30*self.rV))))
	#Specialized slide resize
        self.slideAmp.setGeometry(QtCore.QRect(int(round(220*self.rV)), int(round(475*self.rV)), int(round(160*self.rV)), int(round(30*self.rV))))
        self.slideMPar.setGeometry(QtCore.QRect(int(round(220*self.rV)), int(round(515*self.rV)), int(round(160*self.rV)), int(round(30*self.rV))))
        self.slideResize.setGeometry(QtCore.QRect(int(round(220*self.rV)), int(round(555*self.rV)), int(round(160*self.rV)), int(round(30*self.rV))))

	#    LABELS
	#Teleop labels
        self.labelT1.setGeometry(QtCore.QRect(int(round(40*self.rV)), int(round(55*self.rV)), int(round(70*self.rV)), int(round(20*self.rV))))
        self.labelT2.setGeometry(QtCore.QRect(int(round(280*self.rV)), int(round(55*self.rV)), int(round(70*self.rV)), int(round(20*self.rV))))
	#Labels for additional sliders
        self.labelVelocity.setGeometry(QtCore.QRect(int(round(150*self.rV)), int(round(210*self.rV)), int(round(60*self.rV)), int(round(20*self.rV))))
        self.labelTorque.setGeometry(QtCore.QRect(int(round(150*self.rV)), int(round(250*self.rV)), int(round(60*self.rV)), int(round(20*self.rV))))
        self.labelStiffness.setGeometry(QtCore.QRect(int(round(150*self.rV)), int(round(290*self.rV)), int(round(60*self.rV)), int(round(20*self.rV))))
        self.labelFAA.setGeometry(QtCore.QRect(int(round(150*self.rV)), int(round(330*self.rV)), int(round(60*self.rV)), int(round(20*self.rV))))
	#Specialized label resize
        self.labelAmp.setGeometry(QtCore.QRect(int(round(150*self.rV)), int(round(480*self.rV)), int(round(60*self.rV)), int(round(20*self.rV))))
        self.labelMPar.setGeometry(QtCore.QRect(int(round(150*self.rV)), int(round(520*self.rV)), int(round(60*self.rV)), int(round(20*self.rV))))
        self.labelResize.setGeometry(QtCore.QRect(int(round(150*self.rV)), int(round(555*self.rV)), int(round(60*self.rV)), int(round(20*self.rV))))
	#Label for mode
        self.labelMode.setGeometry(QtCore.QRect(int(round(150*self.rV)), int(round(355*self.rV)), int(round(60*self.rV)), int(round(50*self.rV))))





    ###############################
    #    Ui Reset Build Method    #
    ###############################
    def resetBuild(self):

	self.vel_sat = (1.0, 1.0)
	self.tau_sat = (1.0, 1.0)
	self.stiff_val = (1.0, 1.0)
	self.faa_val = 10
	self.amplify = 1.0
        self.mPar = 1.0

        Form.resize(390, 635)

	#Main text
        self.textMain.setGeometry(QtCore.QRect(130, 15, 130, 50))
	#Home text
        self.textH1.setGeometry(QtCore.QRect(50, 115, 100, 40))
        self.textH2.setGeometry(QtCore.QRect(240, 115, 100, 40))
	#Text for additional sliders
        self.textVelocity.setGeometry(QtCore.QRect(10, 205, 120, 30))
        self.textTorque.setGeometry(QtCore.QRect(10, 245, 121, 31))
        self.textStiffness.setGeometry(QtCore.QRect(10, 285, 120, 30))
        self.textFAA.setGeometry(QtCore.QRect(10, 325, 120, 30))
	#Text for mode
        self.textMode.setGeometry(QtCore.QRect(10, 365, 120, 30))
	#Text for amplitude
        self.textAmp.setGeometry(QtCore.QRect(10, 475, 120, 30))
	#Text for mPar
        self.textMPar.setGeometry(QtCore.QRect(10, 515, 120, 30))
	#Text for resize
        self.textResize.setGeometry(QtCore.QRect(10, 555, 120, 30))
        self.textSetHome.setGeometry(QtCore.QRect(10, 595, 120, 30))

	#Home pushbuttons
        self.pushHome1.setGeometry(QtCore.QRect(50, 165, 100, 27))
        self.pushHome2.setGeometry(QtCore.QRect(240, 165, 100, 27))
	#Mode pushbutton
        self.pushMode.setGeometry(QtCore.QRect(240, 365, 120, 30))
	#ABORT pushbutton
        self.pushAbort.setGeometry(QtCore.QRect(100, 405, 200, 60))
	#Reset pushbuttons
        self.pushResetBuild.setGeometry(QtCore.QRect(10, 10, 110, 40))
        self.pushResetMemory.setGeometry(QtCore.QRect(270, 10, 110, 40))
        self.pushSetHome.setGeometry(QtCore.QRect(200, 595, 110, 30))
	#Teleop sliders
        self.slideT1.setGeometry(QtCore.QRect(20, 75, 160, 30))
        self.slideT2.setGeometry(QtCore.QRect(210, 75, 160, 30))
	#Additional slider
        self.slideVelocity.setGeometry(QtCore.QRect(220, 205, 160, 30))
	self.slideVelocity.setValue(20)
	#Torque slider
        self.slideTorque.setGeometry(QtCore.QRect(220, 245, 160, 30))
	self.slideTorque.setValue(20)
	#Stiffness slider
        self.slideStiffness.setGeometry(QtCore.QRect(220, 285, 160, 30))
	self.slideStiffness.setValue(5)
	#FAA slider
        self.slideFAA.setGeometry(QtCore.QRect(220, 325, 160, 30))
	self.slideFAA.setValue(10)
	#Amp slider
        self.slideAmp.setGeometry(QtCore.QRect(220, 475, 160, 30))
	self.slideAmp.setValue(220)
	#mPar slider
        self.slideMPar.setGeometry(QtCore.QRect(220, 515, 160, 30))
	self.slideMPar.setValue(100)
	#Resize slider
        self.slideResize.setGeometry(QtCore.QRect(220, 555, 160, 30))
	self.slideResize.setValue(10)

	#Labels for additional sliders
        self.labelVelocity.setGeometry(QtCore.QRect(150, 210, 60, 20))
        self.labelTorque.setGeometry(QtCore.QRect(150, 250, 60, 20))
        self.labelStiffness.setGeometry(QtCore.QRect(150, 290, 60, 20))
        self.labelFAA.setGeometry(QtCore.QRect(150, 330, 60, 20))
	#Label for amp
        self.labelAmp.setGeometry(QtCore.QRect(150, 480, 60, 20))
	#Label for mPar
        self.labelMPar.setGeometry(QtCore.QRect(150, 520, 60, 20))
	#Label for resize
        self.labelResize.setGeometry(QtCore.QRect(150, 555, 60, 20))
	#Label for mode
        self.labelMode.setGeometry(QtCore.QRect(150, 355, 60, 50))
	#Teleop labels
        self.labelT1.setGeometry(QtCore.QRect(40, 55, 70, 20))
        self.labelT2.setGeometry(QtCore.QRect(280, 55, 70, 20))





    ################################
    #    Ui Reset Memory Method    #
    ################################
    def resetMemory(self):
	if(self.mode == 1):
	    self.proc.kill()
	    os.system('clear')
            self.labelMode.setText(_translate("Form", "   SAFE", None))
	
	#Setup ROS publishers
	self.pubTOut = rospy.Publisher('gui_theta_teleop', Float32, queue_size=10)
        self.pubHome = rospy.Publisher('gui_home', Float32, queue_size=10)
	self.pubVelSat = rospy.Publisher('gui_vel_sat', Float64MultiArray, queue_size=10)
	self.pubTauSat = rospy.Publisher('gui_tau_sat', Float64MultiArray, queue_size=10)
	self.pubStiffness = rospy.Publisher('gui_stiffness', Float64MultiArray, queue_size=10)
	self.pubFAA = rospy.Publisher('gui_faa', Float32, queue_size=10)
	self.pubGamma = rospy.Publisher('gamma_keep', Float64MultiArray, queue_size = 10)

	#Initialize ROS node
        rospy.init_node('gloveGUITeleop', anonymous=True)

	#Link ROS subscribers to callback functions
	rospy.Subscriber('daq_pos_ref', Float64MultiArray, self.posCallback)
	rospy.Subscriber('gamma_store', Float64MultiArray, self.gammaCallback)
	rospy.Subscriber('stimulate', Float32, self.stim)
	
	#Reset variables
	self.gamma = (0.0, 0.0)
	self.pos_ref = (0.0, 0.0)
	self.offset_ref = (0.0, 0.0)
	self.amp_ref = (0.0, 0.0)
	self.teleopTheta = (0.0, 0.0)
	self.amp_teleop = (0.0, 0.0)
	self.oState = (0.0, 0.0)
	self.state = (0.0, 0.0)
	self.offset = (0.0, 0.0)
	self.mode = 0
	self.startCnt = 0
	self.homeState = 0
	self.lastState = 0
	self.stateCnt = 0

	#Object resize variables + variable object
	self.resizeVal = 1.0
	self.Shape = Form

	os.system('clear')





    ###############################
    #    Text Generator Method    #
    ###############################
    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
	#Text main
        self.textMain.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:22pt;\">Teleop</span></p></body></html>", None))
	#Text theta teleop
        self.labelT1.setText(_translate("Form", "Theta One", None))
        self.labelT2.setText(_translate("Form", "Theta Two", None))
	#Text home resets
        self.pushHome1.setText(_translate("Form", "Reset Index", None))
        self.textH1.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Reset Index</p></body></html>", None))
        self.pushHome2.setText(_translate("Form", "Reset Wrist", None))
        self.textH2.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Reset Wrist</p></body></html>", None))
	#Additional texts
        self.labelVelocity.setText(_translate("Form", "Velocity", None))
        self.labelTorque.setText(_translate("Form", " Torque", None))
        self.labelStiffness.setText(_translate("Form", "Stiffness", None))
        self.labelFAA.setText(_translate("Form", "    FAA", None))
        self.textVelocity.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Max Velocity</p></body></html>", None))
        self.textTorque.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Max Torque</p></body></html>", None))
        self.textStiffness.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Stiffness</p></body></html>", None))
        self.textFAA.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">FAA</p></body></html>", None))
	#Mode font setup
        self.labelMode.setText(_translate("Form", "   SAFE", None))
        self.textMode.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Mode</p></body></html>", None))
        self.pushMode.setText(_translate("Form", "Change Mode", None))
	#Abort font setup
        self.pushAbort.setText(_translate("Form", "ABORT", None))
	#Amplify font setup
        self.labelAmp.setText(_translate("Form", "   Amp", None))
        self.textAmp.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Amp</p></body></html>", None))
	#mPar font setup
        self.labelMPar.setText(_translate("Form", "   mPar", None))
        self.textMPar.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">mPar</p></body></html>", None))
	#Resize font setup
        self.labelResize.setText(_translate("Form", "   Resize", None))
        self.textResize.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Resize</p></body></html>", None))
	#Reset buttons font setup
        self.pushResetBuild.setText(_translate("Form", "R Build", None))
        self.pushResetMemory.setText(_translate("Form", "R Memory", None))
	#Home setting font setup
        self.textSetHome.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Home Set</p></body></html>", None))
        self.pushSetHome.setText(_translate("Form", "Home Set", None))









#####################
#####################
#####    MAIN   #####
#####################
#####################
if __name__ == "__main__":
    try:
	#Open GUI widget
        import sys
        app = QtGui.QApplication(sys.argv)
        Form = QtGui.QWidget()
        ui = Ui_Form()
        ui.setupUi(Form)
        Form.show()
	ui.getFileName()

	#Close GUI widget
        sys.exit(app.exec_())
    #Check for control c
    except rospy.ROSInterruptException:
        pass
