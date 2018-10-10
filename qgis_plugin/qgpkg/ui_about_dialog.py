# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_about_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_qgpkgDlg(object):
    def setupUi(self, qgpkgDlg):
        qgpkgDlg.setObjectName("qgpkgDlg")
        qgpkgDlg.resize(456, 358)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/plugins/QgisGeopackage/about.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        qgpkgDlg.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(qgpkgDlg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtWidgets.QTextEdit(qgpkgDlg)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.button_box = QtWidgets.QDialogButtonBox(qgpkgDlg)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.button_box.setObjectName("button_box")
        self.verticalLayout.addWidget(self.button_box)

        self.retranslateUi(qgpkgDlg)
        self.button_box.accepted.connect(qgpkgDlg.accept)
        self.button_box.rejected.connect(qgpkgDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(qgpkgDlg)

    def retranslateUi(self, qgpkgDlg):
        _translate = QtCore.QCoreApplication.translate
        qgpkgDlg.setWindowTitle(_translate("qgpkgDlg", "QGIS map project GeoPackage extension"))
        self.textEdit.setHtml(_translate("qgpkgDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:9pt; font-weight:600;\">ABOUT</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:9pt;\">This plugin reads and writes QGIS map projects, including data, style and related resources from/into a geopackage file.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:9pt;\">It supports the </span><a href=\"https://github.com/pka/qgpkg/blob/master/qgis_geopackage_extension.md\"><span style=\" text-decoration: underline; color:#2980b9;\">qgis</span></a><span style=\" font-family:\'Ubuntu\'; font-size:9pt;\"> and </span><a href=\"https://github.com/pka/qgpkg/blob/master/ows_geopackage_extension.md\"><span style=\" text-decoration: underline; color:#2980b9;\">ows</span></a><span style=\" font-family:\'Ubuntu\'; font-size:9pt;\"> geopackage extensions. The </span><span style=\" font-family:\'Ubuntu\'; font-size:9pt; font-weight:600;\">qgis geopackage extension</span><span style=\" font-family:\'Ubuntu\'; font-size:9pt;\"> was created with the goal of enabling QGIS users to share their projects, while the </span><span style=\" font-family:\'Ubuntu\'; font-size:9pt; font-weight:600;\">ows geopackage extension</span><span style=\" font-family:\'Ubuntu\'; font-size:9pt;\"> was designed for interoperability, enabling porting map projects between different mapping frameworks; on the former  the approach is to store a QGIS project file in an sqlite table, while on the latter the project is encoded using OGC OWS context standard, on a different sqlite table</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:9pt;\">Currently, writing is only supported using the qgis geopackage extension.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Ubuntu\'; font-size:9pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:9pt;\">Authors: Cedric Christen, Pirmin Kalberer (pka@sourcepole.ch), Joana Simoes (joana.simoes@geocat.net), Paul van Genuchten</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:9pt;\">from SourcePole and GeoCat</span></p></body></html>"))

