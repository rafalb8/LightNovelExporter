import sys
from PySide2 import QtWidgets
from gui.Window import Ui_MainWindow
from gui.Actions import Actions

# Init Qt
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

# Connect actions to signals
act = Actions(ui)
ui.actAddNovel.triggered.connect(act.AddNovel)
ui.wdgList.currentItemChanged.connect(act.SelectedBook)
ui.wdgList.itemActivated.connect(act.EnteredBook)

# Update List
act.UpdateList()

# Start Qt
MainWindow.show()
sys.exit(app.exec_())











