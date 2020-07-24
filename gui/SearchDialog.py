from PySide2.QtCore import QTimer
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QDialog
from faster_than_requests import get2str

from Utils import search
from gui import SearchUI


class SearchDialog(QDialog):
    def __init__(self, settings):
        super().__init__()

        # Dialog UI
        self.ui = SearchUI.Ui_SearchUI()
        self.ui.setupUi(self)

        # Dialog Variables
        self.settings = settings
        self.results = []

        # Connect actions

        # Search Bar
        timer = QTimer()
        timer.setSingleShot(True)
        timer.setInterval(300)
        timer.timeout.connect(self.actSearch)
        self.ui.txtSearchBar.textChanged.connect(lambda: timer.start())

        # List
        self.ui.listResults.currentItemChanged.connect(self.actListSelect)
        self.ui.listResults.itemActivated.connect(self.actListClick)

    # Show Dialog
    def show(self):
        if self.exec_() == 0:
            return ''

        # Return URL
        item = self.ui.listResults.selectedItems()[0]

        url = [b['url'] for b in self.results if b['title'] == item.text()][0]
        return url

    # Actions
    def actSearch(self):
        # Clear list
        self.ui.listResults.clear()

        # Get Search Results
        title = self.ui.txtSearchBar.text()

        if len(title) < 3:
            return

        self.results = search(title, self.settings)

        # Display results
        for book in self.results:
            self.ui.listResults.addItem(book['title'])

    def actListSelect(self, item):
        # Get Image
        url = [b['img'] for b in self.results if b['title'] == item.text()][0]

        img = QPixmap()
        img.loadFromData(get2str(url))

        w = self.ui.imgCover.width()
        h = self.ui.imgCover.height()

        # Show Image
        self.ui.imgCover.setPixmap(img.scaled(w, h))

    def actListClick(self):
        self.accept()



