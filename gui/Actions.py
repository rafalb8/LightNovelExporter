from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QInputDialog, QListWidgetItem, QAbstractItemView
import Utils
from gui.Window import Ui_MainWindow
from os import walk


class ViewType:
    BOOKVIEW = 0
    CHAPTERVIEW = 1


class Actions:
    def __init__(self, ui):
        if isinstance(ui, Ui_MainWindow):
            self.ui = ui
            self.view = ViewType.BOOKVIEW

    # Refresh book list
    def UpdateList(self):
        wdgList = self.ui.wdgList
        settings = Utils.loadSettings()

        wdgList.clear()
        for root, books, files in walk(settings['BooksDirectory']):
            for book in books:
                wdgList.addItem(book)

    # Show Book info
    def SelectedBook(self, item):
        if not isinstance(item, QListWidgetItem):
            return

        if self.view is ViewType.BOOKVIEW:
            settings = Utils.loadSettings()
            # Get Info
            info = Utils.loadInfo(item.text(), settings)

            # Show Cover
            self.ui.imgCover.setPixmap(QPixmap.fromImage(settings['BooksDirectory'] + info['title'] + '/cover.jpg'))

            # Show Info
            self.ui.lblTitle.setText(info['title'])
            self.ui.lblType.setText(info['type'])
            self.ui.lblLanguage.setText(info['language'])
            self.ui.lblGenres.setText(', '.join(info['genres']))

    # Show Book Chapters
    def EnteredBook(self, item):
        if not isinstance(item, QListWidgetItem):
            return
        # Load Settings
        settings = Utils.loadSettings()

        if self.view is ViewType.BOOKVIEW:
            self.view = ViewType.CHAPTERVIEW
            self.ui.menuNovel.setEnabled(True)

            # Get Info
            info = Utils.loadInfo(item.text(), settings)

            # Insert Chapters
            wdgList = self.ui.wdgList
            wdgList.clear()

            for chapter in info['chapters']:
                wdgList.addItem(chapter['name'])

            # Change Selection Mode
            self.ui.wdgList.setSelectionMode(QAbstractItemView.ExtendedSelection)

        elif self.view is ViewType.CHAPTERVIEW:
            pass

    # Add novel to list
    def AddNovel(self):
        # Create Resized Input Dialog
        dlg = QInputDialog()
        dlg.setInputMode(QInputDialog.TextInput)
        dlg.setLabelText('Enter URL:')
        dlg.setWindowTitle('Add Novel')
        dlg.resize(500, 100)
        ans = (dlg.textValue(), dlg.exec_())

        # If Cancelled
        if ans[1] is 0:
            return

        # Get URL
        settings = Utils.loadSettings()
        url = ans[0]

        # Check URL
        if settings['MainURL'] not in url:
            print('Incorrect URL')
            return

        # Dump Info
        try:
            info = Utils.dumpInfo(url, settings)
        except AttributeError:
            print('Incorrect URL')
            return

        # Dump Cover
        Utils.dumpCover(info, settings)

        self.UpdateList()
