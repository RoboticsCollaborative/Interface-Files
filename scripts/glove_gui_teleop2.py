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



from PyQt4 import QtCore, QtGui
import math
import rospy
from std_msgs.msg import Float32
from std_msgs.msg import Float64MultiArray

from rdda_interface.msg import JointCommands



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


    joint_pub = rospy.Publisher("rdd/joint_cmds", JointCommands, queue_size=10)




    #########################
    #    Callback Methods   #
    #########################

    #Teleop theta call
    def theta(self):
	theta1 = self.slideT1.value()
	theta2 = self.slideT2.value()
	theta = Float64MultiArray()
	theta.data = [theta1, theta2]
	print('Theta one has been changed to: '+ str(theta1))
	print('Theta two has been changed to: '+ str(theta2))
	self.pubTOut.publish(theta)

    #Home reset calls
    def homeTheta1(self):
	print 'New home value for theta one has been reset'
	signalOut = 111
	self.pubHome.publish(signalOut)
    def homeTheta2(self):
	print "New home value for theta two has been reset"
	signalOut = 222
	self.pubHome.publish(signalOut)

    #Additional calls
    def maxVelocity(self):
	vel = self.slideVelocity.value()
	velSat = Float64MultiArray()
	velSat.data = [vel]
	print('Maximum velocity has been changed to: ' + str(vel))
	self.pubVelSat.publish(velSat)
	self.vel_sat = (vel, vel)
	self.joint_pub.publish(self.pos_ref, self.vel_sat, self.tau_sat, self.stiff_val, 20)
    def maxTorque(self):
	tau = self.slideTorque.value()
	tauSat = Float64MultiArray()
	tauSat.data = [tau]
	print('Maximum torque has been changed to: ' + str(tau))
	self.pubTauSat.publish(tauSat)
	self.tau_sat = (tau, tau)
	self.joint_pub.publish(self.pos_ref, self.vel_sat, self.tau_sat, self.stiff_val, 20)
    def stiffness(self):
	stiffVal = self.slideStiffness.value()
	stiffness = Float64MultiArray()
	stiffness.data = [stiffVal]
	print('Stiffness has been changed to: ' + str(stiffVal))
	self.pubStiffness.publish(stiffness)
	self.stiff_val = (stiffVal, stiffVal)
	self.joint_pub.publish(self.pos_ref, self.vel_sat, self.tau_sat, self.stiff_val, 20)
    def faa(self):
	faaVal = self.slideFAA.value()
	print('Frequency anti alias value has been changed to: ' + str(faaVal))
	self.pubFAA.publish(faaVal)
	self.faa_val = faaVal
	self.joint_pub.publish(self.pos_ref, self.vel_sat, self.tau_sat, self.stiff_val, 20)

    def posCallback(self, data):
	self.pos_ref = (data.data[0], data.data[1])
	print(self.pos_ref)
	self.joint_pub.publish(self.pos_ref, self.vel_sat, self.tau_sat, self.stiff_val, 20)





    #########################
    #    Ui Setup Method    #
    #########################
    def setupUi(self, Form):
	self.pubTOut = rospy.Publisher('gui_theta_teleop', Float64MultiArray, queue_size=10)
        self.pubHome = rospy.Publisher('gui_home', Float32, queue_size=10)
	self.pubVelSat = rospy.Publisher('gui_vel_sat', Float64MultiArray, queue_size=10)
	self.pubTauSat = rospy.Publisher('gui_tau_sat', Float64MultiArray, queue_size=10)
	self.pubStiffness = rospy.Publisher('gui_stiffness', Float64MultiArray, queue_size=10)
	self.pubFAA = rospy.Publisher('gui_faa', Float32, queue_size=10)

        rospy.init_node('gloveGUITeleop', anonymous=True)
	rospy.Subscriber('daq_pos_ref', Float64MultiArray, self.posCallback)
        self.joint_pub = rospy.Publisher("rdd/joint_cmds", JointCommands, queue_size=1)
	self.pos_ref = (0.0, 0.0)
	self.vel_sat = (0.0, 0.0)
	self.tau_sat = (0.0, 0.0)
	self.stiff_val = (0.0, 0.0)
	self.faa_val = 20
	#Define widget dimmensions
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(400, 370)
	#Main text
        self.textMain = QtGui.QTextEdit(Form)
        self.textMain.setGeometry(QtCore.QRect(130, 15, 130, 50))
        self.textMain.setObjectName(_fromUtf8("textEdit"))
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
	#Teleop labels
        self.labelT1 = QtGui.QLabel(Form)
        self.labelT1.setGeometry(QtCore.QRect(40, 55, 70, 20))
        self.labelT1.setObjectName(_fromUtf8("label"))
        self.labelT2 = QtGui.QLabel(Form)
        self.labelT2.setGeometry(QtCore.QRect(280, 55, 70, 20))
        self.labelT2.setObjectName(_fromUtf8("label_2"))
	#Home pushbuttons
        self.pushHome1 = QtGui.QPushButton(Form)
        self.pushHome1.setGeometry(QtCore.QRect(50, 165, 100, 27))
        self.pushHome1.setObjectName(_fromUtf8("pushButton"))
        self.pushHome2 = QtGui.QPushButton(Form)
        self.pushHome2.setGeometry(QtCore.QRect(240, 165, 100, 27))
        self.pushHome2.setObjectName(_fromUtf8("pushButton_2"))
	#Home text
        self.textH1 = QtGui.QTextEdit(Form)
        self.textH1.setGeometry(QtCore.QRect(50, 115, 100, 40))
        self.textH1.setObjectName(_fromUtf8("textEdit_2"))
        self.textH2 = QtGui.QTextEdit(Form)
        self.textH2.setGeometry(QtCore.QRect(240, 115, 100, 40))
        self.textH2.setObjectName(_fromUtf8("textEdit_3"))
	#Additional sliders
        self.slideVelocity = QtGui.QSlider(Form)
        self.slideVelocity.setGeometry(QtCore.QRect(220, 205, 160, 30))
        self.slideVelocity.setOrientation(QtCore.Qt.Horizontal)
        self.slideVelocity.setObjectName(_fromUtf8("horizontalSlider_3"))
	self.slideVelocity.setMinimum(1)
	self.slideVelocity.setMaximum(100)

        self.slideTorque = QtGui.QSlider(Form)
        self.slideTorque.setGeometry(QtCore.QRect(220, 245, 160, 30))
        self.slideTorque.setOrientation(QtCore.Qt.Horizontal)
        self.slideTorque.setObjectName(_fromUtf8("horizontalSlider_4"))

        self.slideStiffness = QtGui.QSlider(Form)
        self.slideStiffness.setGeometry(QtCore.QRect(220, 285, 160, 30))
        self.slideStiffness.setOrientation(QtCore.Qt.Horizontal)
        self.slideStiffness.setObjectName(_fromUtf8("horizontalSlider_5"))

        self.slideFAA = QtGui.QSlider(Form)
        self.slideFAA.setGeometry(QtCore.QRect(220, 325, 160, 30))
        self.slideFAA.setOrientation(QtCore.Qt.Horizontal)
        self.slideFAA.setObjectName(_fromUtf8("horizontalSlider_6"))
	#Labels for additional sliders
        self.labelVelocity = QtGui.QLabel(Form)
        self.labelVelocity.setGeometry(QtCore.QRect(150, 205, 60, 20))
        self.labelVelocity.setObjectName(_fromUtf8("label_3"))
        self.labelTorque = QtGui.QLabel(Form)
        self.labelTorque.setGeometry(QtCore.QRect(150, 245, 60, 20))
        self.labelTorque.setObjectName(_fromUtf8("label_4"))
        self.labelStiffness = QtGui.QLabel(Form)
        self.labelStiffness.setGeometry(QtCore.QRect(150, 285, 60, 20))
        self.labelStiffness.setObjectName(_fromUtf8("label_5"))
        self.labelFAA = QtGui.QLabel(Form)
        self.labelFAA.setGeometry(QtCore.QRect(150, 325, 60, 20))
        self.labelFAA.setObjectName(_fromUtf8("label_6"))
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
        QtCore.QObject.connect(self.slideVelocity, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.labelVelocity.setNum)
        QtCore.QObject.connect(self.slideVelocity, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.maxVelocity)
        QtCore.QObject.connect(self.slideTorque, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.labelTorque.setNum)
        QtCore.QObject.connect(self.slideTorque, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.maxTorque)
        QtCore.QObject.connect(self.slideStiffness, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.labelStiffness.setNum)
        QtCore.QObject.connect(self.slideStiffness, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.stiffness)
        QtCore.QObject.connect(self.slideFAA, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.labelFAA.setNum)
        QtCore.QObject.connect(self.slideFAA, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.faa)







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
        self.pushHome1.setText(_translate("Form", "Reset One", None))
        self.textH1.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Home One</p></body></html>", None))
        self.pushHome2.setText(_translate("Form", "Reset Two", None))
        self.textH2.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Home Two</p></body></html>", None))
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


	#Close GUI widget
        sys.exit(app.exec_())
    #Check for control c
    except rospy.ROSInterruptException:
        pass
