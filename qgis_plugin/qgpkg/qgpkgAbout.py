# -*- coding: utf-8 -*-

from qgis.PyQt import QtCore, QtWidgets
from .ui_about_dialog import Ui_qgpkgDlg


class qgpkgAbout(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, None)
        self.setWindowFlags(
            self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        # Todo: add support for translation
        self._initGui(parent)

    def _initGui(self, parent):
        self.ui = Ui_qgpkgDlg()
        self.ui.setupUi(self)
