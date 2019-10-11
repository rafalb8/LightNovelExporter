# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui',
# licensing of 'MainWindow.ui' applies.
#
# Created: Fri Oct 11 11:33:56 2019
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(930, 728)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.wdgList = QtWidgets.QListWidget(self.centralwidget)
        self.wdgList.setGeometry(QtCore.QRect(10, 10, 651, 691))
        self.wdgList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.wdgList.setObjectName("wdgList")
        self.lblTitle = QtWidgets.QLabel(self.centralwidget)
        self.lblTitle.setGeometry(QtCore.QRect(670, 370, 251, 71))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lblTitle.setFont(font)
        self.lblTitle.setText("")
        self.lblTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.lblTitle.setWordWrap(True)
        self.lblTitle.setObjectName("lblTitle")
        self.lblType = QtWidgets.QLabel(self.centralwidget)
        self.lblType.setGeometry(QtCore.QRect(670, 450, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lblType.setFont(font)
        self.lblType.setText("")
        self.lblType.setAlignment(QtCore.Qt.AlignCenter)
        self.lblType.setObjectName("lblType")
        self.lblLanguage = QtWidgets.QLabel(self.centralwidget)
        self.lblLanguage.setGeometry(QtCore.QRect(670, 500, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lblLanguage.setFont(font)
        self.lblLanguage.setText("")
        self.lblLanguage.setAlignment(QtCore.Qt.AlignCenter)
        self.lblLanguage.setObjectName("lblLanguage")
        self.lblGenres = QtWidgets.QLabel(self.centralwidget)
        self.lblGenres.setGeometry(QtCore.QRect(670, 550, 251, 111))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lblGenres.setFont(font)
        self.lblGenres.setText("")
        self.lblGenres.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.lblGenres.setWordWrap(True)
        self.lblGenres.setObjectName("lblGenres")
        self.imgCover = QtWidgets.QLabel(self.centralwidget)
        self.imgCover.setGeometry(QtCore.QRect(670, 10, 251, 331))
        self.imgCover.setAutoFillBackground(True)
        self.imgCover.setText("")
        self.imgCover.setScaledContents(True)
        self.imgCover.setMargin(0)
        self.imgCover.setObjectName("imgCover")
        self.btnShowList = QtWidgets.QPushButton(self.centralwidget)
        self.btnShowList.setEnabled(False)
        self.btnShowList.setGeometry(QtCore.QRect(760, 670, 80, 23))
        self.btnShowList.setObjectName("btnShowList")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 930, 30))
        self.menubar.setObjectName("menubar")
        self.menuBooks = QtWidgets.QMenu(self.menubar)
        self.menuBooks.setObjectName("menuBooks")
        self.menuNovel = QtWidgets.QMenu(self.menubar)
        self.menuNovel.setEnabled(False)
        self.menuNovel.setObjectName("menuNovel")
        MainWindow.setMenuBar(self.menubar)
        self.actAddBookURL = QtWidgets.QAction(MainWindow)
        self.actAddBookURL.setObjectName("actAddBookURL")
        self.actDownload = QtWidgets.QAction(MainWindow)
        self.actDownload.setEnabled(True)
        self.actDownload.setObjectName("actDownload")
        self.actGenerate = QtWidgets.QAction(MainWindow)
        self.actGenerate.setObjectName("actGenerate")
        self.actRemoveBook = QtWidgets.QAction(MainWindow)
        self.actRemoveBook.setEnabled(True)
        self.actRemoveBook.setObjectName("actRemoveBook")
        self.actAddBook = QtWidgets.QAction(MainWindow)
        self.actAddBook.setObjectName("actAddBook")
        self.menuBooks.addAction(self.actAddBook)
        self.menuBooks.addAction(self.actAddBookURL)
        self.menuBooks.addAction(self.actRemoveBook)
        self.menuNovel.addAction(self.actDownload)
        self.menuNovel.addAction(self.actGenerate)
        self.menubar.addAction(self.menuBooks.menuAction())
        self.menubar.addAction(self.menuNovel.menuAction())

        self.retranslateUi(MainWindow)
        self.wdgList.setCurrentRow(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Light Novel Exporter", None, -1))
        self.btnShowList.setText(QtWidgets.QApplication.translate("MainWindow", "Back", None, -1))
        self.menuBooks.setTitle(QtWidgets.QApplication.translate("MainWindow", "Novel List", None, -1))
        self.menuNovel.setTitle(QtWidgets.QApplication.translate("MainWindow", "Novel", None, -1))
        self.actAddBookURL.setText(QtWidgets.QApplication.translate("MainWindow", "Add from URL", None, -1))
        self.actDownload.setText(QtWidgets.QApplication.translate("MainWindow", "Download Chapter/s", None, -1))
        self.actGenerate.setText(QtWidgets.QApplication.translate("MainWindow", "Generate ePUB", None, -1))
        self.actRemoveBook.setText(QtWidgets.QApplication.translate("MainWindow", "Remove Book", None, -1))
        self.actAddBook.setText(QtWidgets.QApplication.translate("MainWindow", "Add Book", None, -1))

