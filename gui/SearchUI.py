# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Search.ui',
# licensing of 'Search.ui' applies.
#
# Created: Fri Jul 24 11:00:26 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_SearchUI(object):
    def setupUi(self, SearchUI):
        SearchUI.setObjectName("SearchUI")
        SearchUI.resize(859, 595)
        self.verticalLayoutWidget = QtWidgets.QWidget(SearchUI)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 851, 591))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.txtSearchBar = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.txtSearchBar.setObjectName("txtSearchBar")
        self.verticalLayout_2.addWidget(self.txtSearchBar)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listResults = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.listResults.setObjectName("listResults")
        self.horizontalLayout.addWidget(self.listResults)
        self.imgCover = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.imgCover.setMinimumSize(QtCore.QSize(359, 479))
        self.imgCover.setObjectName("imgCover")
        self.horizontalLayout.addWidget(self.imgCover)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(SearchUI)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), SearchUI.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), SearchUI.accept)
        QtCore.QMetaObject.connectSlotsByName(SearchUI)

    def retranslateUi(self, SearchUI):
        SearchUI.setWindowTitle(QtWidgets.QApplication.translate("SearchUI", "Dialog", None, -1))
        self.imgCover.setText(QtWidgets.QApplication.translate("SearchUI", "Cover", None, -1))

