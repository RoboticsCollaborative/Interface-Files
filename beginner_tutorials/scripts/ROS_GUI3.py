# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ROS_GUI3.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(400, 300)
        self.horizontalSlider = QtGui.QSlider(Form)
        self.horizontalSlider.setGeometry(QtCore.QRect(120, 240, 160, 29))
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(10)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.plainTextEdit = QtGui.QPlainTextEdit(Form)
        self.plainTextEdit.setGeometry(QtCore.QRect(110, 200, 181, 31))
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.textEdit = QtGui.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(120, 10, 181, 51))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(40, 80, 99, 27))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(160, 80, 99, 27))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(280, 80, 99, 27))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(200, 270, 68, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.checkBox = QtGui.QCheckBox(Form)
        self.checkBox.setGeometry(QtCore.QRect(140, 150, 131, 22))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.horizontalSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.label.setNum)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.plainTextEdit.setPlainText(_translate("Form", "  Amplitude Magnifier", None))
        self.textEdit.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:26pt; vertical-align:super;\">   SIGNAL TYPE</span></p></body></html>", None))
        self.pushButton.setText(_translate("Form", "SIN", None))
        self.pushButton_2.setText(_translate("Form", "COS", None))
        self.pushButton_3.setText(_translate("Form", "TAN", None))
        self.label.setText(_translate("Form", "1", None))
        self.checkBox.setText(_translate("Form", "Function OFF", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

