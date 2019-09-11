from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QInputDialog, QListWidgetItem, QAbstractItemView, QFileDialog
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

        if self.view is ViewType.BOOKVIEW:
            for root, books, files in walk(self.settings['BooksDirectory']):
                for book in books:
                    wdgList.addItem(book)
        elif self.view is ViewType.CHAPTERVIEW:
            for chapter in self.info['chapters']:
                name = '{0} | {1}'.format(chapter['volume'], chapter['name'])
                path = self.settings['BooksDirectory']+self.info['title']+'/'+chapter['name']+'.txt'
                if exists(path):
                    wdgList.addItem('[{0}]'.format(name))
                else:
                    wdgList.addItem(name)

    def BackToBookList(self):
        if self.view is not ViewType.BOOKVIEW:
            self.view = ViewType.BOOKVIEW
            self.ui.menuNovel.setEnabled(False)
            self.UpdateList()

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
            self.ui.actShowList.setEnabled(True)

            # Insert Chapters
            self.UpdateList()

            # Change Selection Mode
            self.ui.wdgList.setSelectionMode(QAbstractItemView.ExtendedSelection)

        elif self.view is ViewType.CHAPTERVIEW:
            pass

    # Find and download chapters
    def downloadChapters(self, chapters):
        chp = self.info['chapters']

        # Get indexes from Info dictionary
        idx = [i for i in range(len(chp)) for name in chapters if name == chp[i]['name']]

        # Dump chapters
        for i in idx:
            Utils.dumpChapterText(self.info, i, self.settings)

    # Download selected chapters
    def DownloadAction(self):
        wdgList = self.ui.wdgList

        # Get Selected List
        selected = [item.text().split(' | ')[1] for item in wdgList.selectedItems() if item.text().split(' | ')[1][-1] is not ']']

        # Download chapters
        self.downloadChapters(selected)

        # Refresh list
        self.UpdateList()

    # Generate ePUB from selected chapters
    def GenerateBook(self):
        wdgList = self.ui.wdgList

        # Get Selected List
        selected = [item.text().split(' | ')[1] for item in wdgList.selectedItems()]

        # Dump not downloaded chapters
        notDumped = [x for x in selected if x[-1] != ']']
        self.downloadChapters(notDumped)
        self.UpdateList()

        # Update selected list
        selected = [x[:-1] for x in selected if x[-1] == ']']
        selected += notDumped

        # Get dicts from Info dictionary
        chapters = [chp for chp in self.info['chapters'] for name in selected if name == chp['name']]

        # Generate Title for book
        volume = chapters[0]['volume']
        for chapter in chapters:
            if chapter['volume'] != volume or 'chapters' in volume.lower():
                volume = 'Chapters:'

        title = self.info['title'] + ' ' + volume

        # If chapters are not from the same volume
        if volume == 'Chapters:':
            numbers = [int(float(''.join(s for s in name if s.isdigit() or s == '.'))) for name in selected]
            numbers = list(set(numbers))
            numbers.sort()

            # Generate ranges for number list
            ranges = Utils.ranges(numbers)

            for r in ranges:
                if r[0] == r[1]:
                    title += ' {0},'.format(r[0])
                else:
                    title += ' {0}-{1},'.format(r[0], r[1])

            if title[-1] == ',':
                title = title[:-1]

        # Show Title Input Dialog
        dlg = QInputDialog()
        dlg.setInputMode(QInputDialog.TextInput)
        dlg.setLabelText('Enter Title:')
        dlg.setWindowTitle('Select Book Title')
        dlg.setTextValue(title)
        dlg.resize(500, 100)

        # If Cancelled
        if dlg.exec_() is 0:
            return

        # Get URL
        title = dlg.textValue()

        # Show File Dialog
        ans = QFileDialog.getSaveFileName(caption='Save ePUB', filter='ePUB (*.epub)')
        filename = ans[0]

        # Add file format if not present
        if filename[-5:] != '.epub':
            filename += '.epub'

        # Generate ePUB file
        Utils.generateEPUB(filename, title, self.info, chapters, self.settings)

