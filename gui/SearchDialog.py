from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QDialog

from gui import SearchUI


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Dialog UI
        self.ui = SearchUI.Ui_Dialog()
        self.ui.setupUi(self)

        # Connect action
        timer = QTimer()
        timer.setSingleShot(True)
        timer.setInterval(300)
        timer.timeout.connect(self.actSearch)
        self.ui.txtSearchBar.textChanged.connect(lambda: timer.start())

        # Return value
        self.url = ""

    # Show Dialog
    def show(self):
        if self.exec_() is 0:
            return False

        return True

    # Actions
    def actSearch(self):
        print(self.ui.txtSearchBar.text())



