#!/usr/bin/env python

from PyQt4 import QtCore, QtGui
import math
import rospy
from std_msgs.msg import Float32


#Launch GUI
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
    def hello(self):
	print "Hello is pressed"
	dataOut = 0
	pub.publish(dataOut)
    def hi(self):
	print "Hi is pressed"
	dataOut = 1
	pub.publish(dataOut)

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(547, 388)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(150, 250, 100, 25))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 250, 100, 25))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))

        self.retranslateUi(Form)
	QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.hello)
	QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.hi)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.pushButton.setText(_translate("Form", "Hello", None))
        self.pushButton_2.setText(_translate("Form", "Hi", None))


if __name__ == '__main__':
    try:
        import sys
        app = QtGui.QApplication(sys.argv)
        Form = QtGui.QWidget()
        ui = Ui_Form()
        ui.setupUi(Form)
        Form.show()

	pub = rospy.Publisher('chatter', Float32, queue_size=10)
        rospy.init_node('rosGui', anonymous=True)
        rate = rospy.Rate(10) # 10hz

        sys.exit(app.exec_())
    except rospy.ROSInterruptException:
        pass
