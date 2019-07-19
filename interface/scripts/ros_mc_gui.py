#!/usr/bin/env python


#import
from PyQt4 import QtCore, QtGui
import math
import rospy
from std_msgs.msg import Float32


resetVal = 0


#check inports
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


#widget
class Ui_Form(object):

    #widget actions
    def sin(self):
	print "Producing Sine function"
	signalOut = 001
	#pub.publish(signalOut)
    def cos(self):
	print "Producing Cosine function"
	signalOut = 010
	#pub.publish(signalOut)
    def funcReset(self):
	global resetVal
	print "Resetting function"
	if(resetVal == 0):
	    resetVal = 1
	else:
	    resetVal = 0
	print(resetVal)
	pubReset.publish(resetVal)
    def slideVal(self):
	print "New slider value is: " + str(self.horizontalSlider.value())
	dataOut = self.horizontalSlider.value()
	pubAmp.publish(dataOut)

    #widget setup
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(400, 300)
        self.horizontalSlider = QtGui.QSlider(Form)
        self.horizontalSlider.setGeometry(QtCore.QRect(100, 200, 200, 100))
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(10)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.plainTextEdit = QtGui.QPlainTextEdit(Form)
        self.plainTextEdit.setGeometry(QtCore.QRect(100, 200, 200, 30))
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.textEdit = QtGui.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(100, 10, 200, 51))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(40, 80, 100, 25))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(160, 80, 100, 25))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(280, 80, 100, 25))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(200, 250, 75, 50))
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(Form)
	QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.sin)
	QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.cos)
	QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL(_fromUtf8("clicked()")), self.funcReset)
        QtCore.QObject.connect(self.horizontalSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.label.setNum)
	QtCore.QObject.connect(self.horizontalSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.slideVal)
        QtCore.QMetaObject.connectSlotsByName(Form)


    #widget action to function call
    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.plainTextEdit.setPlainText(_translate("Form", "        Amplitude Magnifier", None))
        self.textEdit.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:26pt; vertical-align:super;\">   SIGNAL TYPE</span></p></body></html>", None))
        self.pushButton.setText(_translate("Form", "SIN", None))
        self.pushButton_2.setText(_translate("Form", "COS", None))
        self.pushButton_3.setText(_translate("Form", "RESET", None))
        self.label.setText(_translate("Form", "1", None))


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
	pubReset = rospy.Publisher('daqFuncReset', Float32, queue_size=10)
	pubAmp = rospy.Publisher('daqFuncAmp', Float32, queue_size=10)
        rospy.init_node('daqGUI', anonymous=True)
        rate = rospy.Rate(10) # 10hz

	#close GUI widget
        sys.exit(app.exec_())

    #check for control c
    except rospy.ROSInterruptException:
        pass
