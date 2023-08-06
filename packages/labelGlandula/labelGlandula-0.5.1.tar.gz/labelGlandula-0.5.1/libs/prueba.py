# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogo.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QDialog,QWidget, QPushButton, QDialog, QApplication
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPainter, QPen
from PyQt5.Qt import Qt
from libs.linea import DibujarLineaApp

class Ui_Dialog(object):
    genera = False

    def setupUi(self, Ui_Dialog):
        Ui_Dialog.setObjectName("Dialog")
        #Ui_Dialog.resize(498, 488)
        Ui_Dialog.resize(450, 188)
        self.dialog = Ui_Dialog
        self.buttonBox = QtWidgets.QDialogButtonBox(Ui_Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(250, 140, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.label = QtWidgets.QLabel(Ui_Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 431, 17))
        self.label.setObjectName("label")

        self.escala = QtWidgets.QLineEdit(Ui_Dialog)
        self.escala.setGeometry(QtCore.QRect(20, 70, 113, 25))
        self.escala.setObjectName("lineEdit")

        self.pixel = QtWidgets.QLineEdit(Ui_Dialog)
        self.pixel.setGeometry(QtCore.QRect(20, 110, 113, 25))
        self.pixel.setObjectName("lineEdit")

        self.label1 = QtWidgets.QLabel(Ui_Dialog)
        self.label1.setGeometry(QtCore.QRect(150, 110, 51, 25))
        self.label1.setObjectName("label")

        self.medidas = QtWidgets.QComboBox(Ui_Dialog)
        self.medidas.setGeometry(QtCore.QRect(150, 70, 51, 25))
        self.medidas.setObjectName("comboBox")
        self.medidas.addItem("")
        self.medidas.addItem("")
        self.medidas.addItem("")


        self.label_3 = QtWidgets.QLabel(Ui_Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 140, 391, 17))
        self.label_3.setObjectName("label_3")


        self.buttonBox.accepted.connect(self.actualizar)
        self.retranslateUi(Ui_Dialog)
        QtCore.QMetaObject.connectSlotsByName(Ui_Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Enter the scale and the corresponding unit:"))
        self.label1.setText(_translate("Dialog", "px"))
        self.medidas.setItemText(0, _translate("Dialog", "cm"))
        self.medidas.setItemText(1, _translate("Dialog", "mm"))
        self.medidas.setItemText(2, _translate("Dialog", "µm"))
        #self.label_2.setText(_translate("Dialog", "px"))




    def actualizar(self):
        self.genera = True
        # Se lee el valor de la caja de texto
        escalas = float(self.escala.text())
        #pixeles = int(self.pixel.text())
        unidad = self.medidas.currentText()
        pixels = float(self.pixel.text())
        #ch2 = self.checkBox_2.isChecked()
        #ch3 = self.checkBox_3.isChecked()
        #ch4 = self.checkBox_4.isChecked()
        #ch5 = self.checkBox_5.isChecked()
        #ch6 = self.checkBox_6.isChecked()
        #ch7 = self.checkBox_7.isChecked()
        #ch8 = self.checkBox_8.isChecked()
        #ch9 = self.checkBox_9.isChecked()
        #ch10 = self.checkBox_10.isChecked()
        # if self.escalas.setValidator(QtGui.QDoubleValidator()):
        self.esca = escalas
        self.pixe = pixels
        # else:
        #     QtGui.QMessageBox.about(self, "The scale must be a number")
        # if self.pixeles.setValidator(QtGui.QDoubleValidator()):
        #self.pix = pixeles
        # else:
        #     QtGui.QMessageBox.about(self, "The pixels must be a number")
        self.uni = unidad

        # close dialog
        self.dialog.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
