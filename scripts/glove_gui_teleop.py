#!/usr/bin/env python

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'glove_gui_teleop.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import math
import rospy
from std_msgs.msg import Float32



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



class Ui_Form(object):


    #widget actions
    def theta1(self):
	dataOut = self.slideT1.value()
	print('Theta one has been changed to: '+ str(dataOut))
	pubTOut.publish(dataOut)
    def theta2(self):
	dataOut = self.slideT2.value()
	print('Theta two has been changed to: ' + str(dataOut))
	pubTOut.publish(dataOut)

    def maxVelocity(self):
	dataOut = self.slideVelocity.value()
	print('Maximum velocity has been changed to: ' + str(dataOut))
	pubVTS.publish(dataOut)
    def maxTorque(self):
	dataOut = self.slideTorque.value()
	print('Maximum torque has been changed to: ' + str(dataOut))
	pubVTS.publish(dataOut)
    def stiffness(self):
	dataOut = self.slideStiffness.value()
	print('Stiffness has been changed to: ' + str(dataOut))
	pubVTS.publish(dataOut)
    def homeTheta1(self):
	print 'New home value for theta one has been reset'
	signalOut = 111
	pubHome.publish(signalOut)
    def homeTheta2(self):
	print "New home value for theta two has been reset"
	signalOut = 222
	pubHome.publish(signalOut)





    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(400, 305)
        self.textMain = QtGui.QTextEdit(Form)
        self.textMain.setGeometry(QtCore.QRect(130, 0, 130, 50))
        self.textMain.setObjectName(_fromUtf8("textEdit"))
        self.slideT1 = QtGui.QSlider(Form)
        self.slideT1.setGeometry(QtCore.QRect(20, 60, 160, 30))
        self.slideT1.setMaximum(360)
        self.slideT1.setOrientation(QtCore.Qt.Horizontal)
        self.slideT1.setObjectName(_fromUtf8("horizontalSlider"))
        self.slideT2 = QtGui.QSlider(Form)
        self.slideT2.setGeometry(QtCore.QRect(210, 60, 160, 30))
        self.slideT2.setMaximum(360)
        self.slideT2.setOrientation(QtCore.Qt.Horizontal)
        self.slideT2.setObjectName(_fromUtf8("horizontalSlider_2"))
        self.labelT1 = QtGui.QLabel(Form)
        self.labelT1.setGeometry(QtCore.QRect(40, 40, 70, 20))
        self.labelT1.setObjectName(_fromUtf8("label"))
        self.pushHome1 = QtGui.QPushButton(Form)
        self.pushHome1.setGeometry(QtCore.QRect(50, 150, 100, 27))
        self.pushHome1.setObjectName(_fromUtf8("pushButton"))
        self.textH1 = QtGui.QTextEdit(Form)
        self.textH1.setGeometry(QtCore.QRect(50, 100, 100, 40))
        self.textH1.setObjectName(_fromUtf8("textEdit_2"))
        self.textH2 = QtGui.QTextEdit(Form)
        self.textH2.setGeometry(QtCore.QRect(240, 100, 100, 40))
        self.textH2.setObjectName(_fromUtf8("textEdit_3"))
        self.pushHome2 = QtGui.QPushButton(Form)
        self.pushHome2.setGeometry(QtCore.QRect(240, 150, 100, 27))
        self.pushHome2.setObjectName(_fromUtf8("pushButton_2"))
        self.slideVelocity = QtGui.QSlider(Form)
        self.slideVelocity.setGeometry(QtCore.QRect(220, 190, 160, 30))
        self.slideVelocity.setOrientation(QtCore.Qt.Horizontal)
        self.slideVelocity.setObjectName(_fromUtf8("horizontalSlider_3"))
        self.slideTorque = QtGui.QSlider(Form)
        self.slideTorque.setGeometry(QtCore.QRect(220, 230, 160, 30))
        self.slideTorque.setOrientation(QtCore.Qt.Horizontal)
        self.slideTorque.setObjectName(_fromUtf8("horizontalSlider_4"))
        self.slideStiffness = QtGui.QSlider(Form)
        self.slideStiffness.setGeometry(QtCore.QRect(220, 270, 160, 30))
        self.slideStiffness.setOrientation(QtCore.Qt.Horizontal)
        self.slideStiffness.setObjectName(_fromUtf8("horizontalSlider_5"))
        self.labelVelocity = QtGui.QLabel(Form)
        self.labelVelocity.setGeometry(QtCore.QRect(150, 190, 60, 20))
        self.labelVelocity.setObjectName(_fromUtf8("label_3"))
        self.labelTorque = QtGui.QLabel(Form)
        self.labelTorque.setGeometry(QtCore.QRect(150, 230, 60, 20))
        self.labelTorque.setObjectName(_fromUtf8("label_4"))
        self.labelStiffness = QtGui.QLabel(Form)
        self.labelStiffness.setGeometry(QtCore.QRect(150, 270, 60, 20))
        self.labelStiffness.setObjectName(_fromUtf8("label_5"))
        self.textVelocity = QtGui.QTextEdit(Form)
        self.textVelocity.setGeometry(QtCore.QRect(10, 190, 120, 30))
        self.textVelocity.setObjectName(_fromUtf8("textEdit_4"))
        self.textTorque = QtGui.QTextEdit(Form)
        self.textTorque.setGeometry(QtCore.QRect(10, 230, 121, 31))
        self.textTorque.setObjectName(_fromUtf8("textEdit_5"))
        self.textStiffness = QtGui.QTextEdit(Form)
        self.textStiffness.setGeometry(QtCore.QRect(10, 270, 120, 30))
        self.textStiffness.setObjectName(_fromUtf8("textEdit_6"))
        self.labelT2 = QtGui.QLabel(Form)
        self.labelT2.setGeometry(QtCore.QRect(280, 40, 70, 20))
        self.labelT2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.slideT1, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.labelT1.setNum)
	QtCore.QObject.connect(self.slideT1, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.theta1)
        QtCore.QObject.connect(self.slideT2, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.labelT2.setNum)
	QtCore.QObject.connect(self.slideT2, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.theta2)
        QtCore.QObject.connect(self.slideVelocity, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.labelVelocity.setNum)
        QtCore.QObject.connect(self.slideVelocity, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.maxVelocity)
        QtCore.QObject.connect(self.slideTorque, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.labelTorque.setNum)
        QtCore.QObject.connect(self.slideTorque, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.maxTorque)
        QtCore.QObject.connect(self.slideStiffness, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.labelStiffness.setNum)
        QtCore.QObject.connect(self.slideStiffness, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.stiffness)
	QtCore.QObject.connect(self.pushHome1, QtCore.SIGNAL(_fromUtf8("clicked()")), self.homeTheta1)
	QtCore.QObject.connect(self.pushHome2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.homeTheta2)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.textMain.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:22pt;\">Teleop</span></p></body></html>", None))
        self.labelT1.setText(_translate("Form", "Theta One", None))
        self.pushHome1.setText(_translate("Form", "Reset One", None))
        self.textH1.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Home One</p></body></html>", None))
        self.textH2.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Home Two</p></body></html>", None))
        self.pushHome2.setText(_translate("Form", "Reset Two", None))
        self.labelVelocity.setText(_translate("Form", "Velocity", None))
        self.labelTorque.setText(_translate("Form", " Torque", None))
        self.labelStiffness.setText(_translate("Form", "Stiffness", None))
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
        self.labelT2.setText(_translate("Form", "Theta Two", None))


#main
if __name__ == "__main__":
    try:
	#open GUI widget
        import sys
        app = QtGui.QApplication(sys.argv)
        Form = QtGui.QWidget()
        ui = Ui_Form()
        ui.setupUi(Form)
        Form.show()

	#create publishing node
	pubVTS = rospy.Publisher('gloveVTS', Float32, queue_size=10)
	pubTOut = rospy.Publisher('gloveThetaTeleop', Float32, queue_size=10)
        pubHome = rospy.Publisher('gloveHome', Float32, queue_size=10)
        rospy.init_node('gloveGUITeleop', anonymous=True)
        rate = rospy.Rate(10) # 10hz

	#close GUI widget
        sys.exit(app.exec_())

    #check for control c
    except rospy.ROSInterruptException:
        pass
