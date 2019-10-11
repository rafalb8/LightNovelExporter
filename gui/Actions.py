from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QInputDialog, QListWidgetItem, QAbstractItemView, QFileDialog, QProgressDialog
import Utils
from gui.SearchDialog import SearchDialog
from gui.Window import Ui_MainWindow
from os import walk, path
from shutil import rmtree

class ViewType:
    BOOKVIEW = 0
    CHAPTERVIEW = 1


class Actions:
    def __init__(self, app, ui):
        if not isinstance(ui, Ui_MainWindow):
            raise

        self.app = app
        self.ui = ui
        self.view = ViewType.BOOKVIEW
        self.settings = Utils.loadSettings()
        self.info = {}

    # Refresh book list
    def UpdateList(self):
        wdgList = self.ui.wdgList
        wdgList.clear()

        if self.view is ViewType.BOOKVIEW:
            # Change Selection Mode
            self.ui.wdgList.setSelectionMode(QAbstractItemView.SingleSelection)

            # Enable/ Disable menus
            self.ui.menuNovel.setEnabled(False)
            self.ui.btnShowList.setEnabled(False)
            self.ui.menuBooks.setEnabled(True)

            # Add books to the list
            for root, books, files in walk(self.settings['BooksDirectory']):
                for book in books:
                    wdgList.addItem(book)

        elif self.view is ViewType.CHAPTERVIEW:
            # Change Selection Mode
            self.ui.wdgList.setSelectionMode(QAbstractItemView.ExtendedSelection)

            # Enable/ Disable menus
            self.ui.menuNovel.setEnabled(True)
            self.ui.btnShowList.setEnabled(True)
            self.ui.menuBooks.setEnabled(False)

            # Add chapters to the list
            for chapter in self.info['chapters']:
                name = '{0} | {1}'.format(chapter['volume'], chapter['name'])
                file = path.join(self.settings['BooksDirectory'], self.info['title'], '{0}.{1}.html'.format(chapter['volume'], chapter['name']))
                if path.exists(file):
                    wdgList.addItem('[{0}]'.format(name))
                else:
                    wdgList.addItem(name)

    def BackToBookList(self):
        self.view = ViewType.BOOKVIEW
        self.UpdateList()

    # Add novel to list
    def AddBook(self):
        dlg = SearchDialog()
        dlg.show()

    # Add novel to list from URL
    def AddBookFromURL(self):
        # Create Resized Input Dialog
        dlg = QInputDialog()
        dlg.setInputMode(QInputDialog.TextInput)
        dlg.setLabelText('Enter URL:')
        dlg.setTextValue('https://www.readlightnovel.org/only-i-level-up')
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

    # Remove novel
    def RemoveBook(self):
        # Get Selected item
        if len(self.ui.wdgList.selectedItems()) <= 0:
            return

        selected = self.ui.wdgList.selectedItems()[0].text()
        book = path.join(self.settings['BooksDirectory'], selected)

        rmtree(book, ignore_errors=True)
        self.UpdateList()

    # List item selection event
    def ListSelect(self, item):
        if not isinstance(item, QListWidgetItem):
            return

        # Show Book info
        if self.view is ViewType.BOOKVIEW:
            # Get Info
            self.info = Utils.loadInfo(item.text(), self.settings)

            # Show Cover
            img = path.join(self.settings['BooksDirectory'], self.info['title'], 'cover.jpg')
            self.ui.imgCover.setPixmap(QPixmap.fromImage(img))

            # Show Info
            self.ui.lblTitle.setText(self.info['title'])
            self.ui.lblType.setText(self.info['type'])
            self.ui.lblLanguage.setText(self.info['language'])
            self.ui.lblGenres.setText(', '.join(self.info['genres']))

    # List click event
    def ListClick(self, item):
        if not isinstance(item, QListWidgetItem):
            return

        if self.view is ViewType.BOOKVIEW:
            self.view = ViewType.CHAPTERVIEW

        # Insert Chapters
        self.UpdateList()

    # Right click menu for list
    def ContextMenu(self, point):
        if self.view is ViewType.BOOKVIEW:
            self.ui.menuBooks.exec_(self.ui.wdgList.mapToGlobal(point))
        elif self.view is ViewType.CHAPTERVIEW:
            self.ui.menuNovel.exec_(self.ui.wdgList.mapToGlobal(point))

    # Find and download chapters
    def downloadChapters(self, chapters):
        chp = self.info['chapters']

        # Get indexes from Info dictionary
        idx = [i for i in range(len(chp)) for volume, name in chapters if name == chp[i]['name'] and volume == chp[i]['volume']]

        # Create Progress Dialog
        progress = QProgressDialog('Downloading Chapters', 'Cancel', 0, len(idx))

        # Show Dialog
        progress.show()
        self.app.processEvents()

        # Dump chapters
        for i in range(len(idx)):
            if progress.wasCanceled():
                return False

            Utils.dumpChapterText(self.info, idx[i], self.settings)
            progress.setValue(i)
            self.app.processEvents()

        # Return status
        return True

    # Download selected chapters
    def DownloadAction(self):
        wdgList = self.ui.wdgList

        # Get Selected List
        selected = [item.text().split(' | ') for item in wdgList.selectedItems() if item.text().split(' | ')[1][-1] is not ']']

        # Download chapters
        self.downloadChapters(selected)

        # Refresh list
        self.UpdateList()

    # Generate ePUB from selected chapters
    def GenerateBook(self):
        wdgList = self.ui.wdgList

        # Get Selected List
        selected = [item.text().split(' | ') for item in wdgList.selectedItems()]

        if len(selected) <= 0:
            return

        # Dump not downloaded chapters
        notDumped = [x for x in selected if x[1][-1] != ']']

        # Download chapters
        if not self.downloadChapters(notDumped):
            self.UpdateList()
            # If canceled stop epub generation
            return

        self.UpdateList()

        # Update selected list
        selected = [[x[0][1:], x[1][:-1]] for x in selected if x[1][-1] == ']']
        selected += notDumped

        # Get dicts from Info dictionary
        chapters = [chp for chp in self.info['chapters'] for volume, name in selected if name == chp['name'] and volume == chp['volume']]

        # Generate Title for book
        volume = chapters[0]['volume']
        for chapter in chapters:
            if chapter['volume'] != volume or 'chapters' in volume.lower():
                volume = 'Chapters:'

        title = self.info['title'] + ' ' + volume

        try:
            # If chapters are not from the same volume
            if volume == 'Chapters:':
                numbers = [int(float(''.join(s for s in name if s.isdigit() or s == '.' or s == '-'))) for name in selected]
                numbers = list(set(numbers))

                # Generate ranges for number list
                ranges = Utils.ranges(numbers)

                for r in ranges:
                    if r[0] == r[1]:
                        title += ' {0},'.format(r[0])
                    else:
                        title += ' {0} - {1},'.format(r[0], r[1])

                if title[-1] == ',':
                    title = title[:-1]
        except ValueError:
            pass

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
        ans = QFileDialog.getSaveFileName(caption='Save ePUB', filter='ePUB (*.epub)', dir=title+'.epub')
        filename = ans[0]

        # Add file format if not present
        if filename[-5:] != '.epub':
            filename += '.epub'

        # Generate ePUB file
        Utils.generateEPUB(filename, title, self.info, chapters, self.settings)

