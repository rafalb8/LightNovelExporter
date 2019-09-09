from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QInputDialog, QListWidgetItem, QAbstractItemView
import Utils
from gui.Window import Ui_MainWindow
from os import walk
from os.path import exists


class ViewType:
    BOOKVIEW = 0
    CHAPTERVIEW = 1


class Actions:
    def __init__(self, ui):
        if not isinstance(ui, Ui_MainWindow):
            raise

        self.ui = ui
        self.view = ViewType.BOOKVIEW
        self.settings = Utils.loadSettings()
        self.info = {}

    # Refresh book list
    def UpdateList(self):
        wdgList = self.ui.wdgList

        wdgList.clear()
        for root, books, files in walk(self.settings['BooksDirectory']):
            for book in books:
                wdgList.addItem(book)

    # Add novel to list
    def AddNovel(self):
        # Create Resized Input Dialog
        dlg = QInputDialog()
        dlg.setInputMode(QInputDialog.TextInput)
        dlg.setLabelText('Enter URL:')
        dlg.setWindowTitle('Add Novel')
        dlg.resize(500, 100)

        # If Cancelled
        if dlg.exec_() is 0:
            return

        # Get URL
        url = dlg.textValue()

        # Check URL
        if self.settings['MainURL'] not in url:
            print('{0} not in {1}'.format(self.settings['MainURL'], url))
            return

        # Dump Info
        try:
            info = Utils.dumpInfo(url, self.settings)
        except AttributeError:
            print('Incorrect URL')
            return

        # Dump Cover
        Utils.dumpCover(info, self.settings)

        self.UpdateList()

    # Show Book info
    def SelectedBook(self, item):
        if not isinstance(item, QListWidgetItem):
            return

        if self.view is ViewType.BOOKVIEW:
            # Get Info
            self.info = Utils.loadInfo(item.text(), self.settings)

            # Show Cover
            self.ui.imgCover.setPixmap(QPixmap.fromImage(self.settings['BooksDirectory'] + self.info['title'] + '/cover.jpg'))

            # Show Info
            self.ui.lblTitle.setText(self.info['title'])
            self.ui.lblType.setText(self.info['type'])
            self.ui.lblLanguage.setText(self.info['language'])
            self.ui.lblGenres.setText(', '.join(self.info['genres']))

    # Show Book Chapters
    def EnteredBook(self, item):
        if not isinstance(item, QListWidgetItem):
            return

        if self.view is ViewType.BOOKVIEW:
            self.view = ViewType.CHAPTERVIEW
            self.ui.menuNovel.setEnabled(True)

            # Insert Chapters
            wdgList = self.ui.wdgList
            wdgList.clear()

            for chapter in self.info['chapters']:
                name = chapter['volume'] + ' | ' + chapter['name']
                path = self.settings['BooksDirectory']+self.info['title']+'/'+chapter['name']+'.txt'
                if exists(path):
                    wdgList.addItem('[{0}]'.format(name))
                else:
                    wdgList.addItem(name)

            # Change Selection Mode
            self.ui.wdgList.setSelectionMode(QAbstractItemView.ExtendedSelection)

        elif self.view is ViewType.CHAPTERVIEW:
            pass

    # Download selected chapters
    def DownloadAction(self):
        wdgList = self.ui.wdgList

        # Get Selected List
        selected = [item.text().split(' | ')[1] for item in wdgList.selectedItems()]

        # Get indexes from Info dictionary
        chp = self.info['chapters']
        chapters = [i for i in range(len(chp)) for name in selected if name == chp[i]['name']]

        for i in range(len(chapters)):
            Utils.dumpChapterText(self.info, chapters[i], self.settings)
            wdgList.selectedItems()[i].setText('[{0}]'.format(wdgList.selectedItems()[i].text()))

