import sys
from PySide2 import QtWidgets

import Utils
from gui.Window import Ui_MainWindow
from gui.Actions import Actions
from os.path import exists

# Create default settings file
if not exists('settings.json'):
    Utils.defaultSettings()

# Init Qt
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

# Connect actions to signals
act = Actions(ui)
ui.actAddNovel.triggered.connect(act.AddNovel)
ui.wdgList.currentItemChanged.connect(act.ListSelect)
ui.wdgList.itemActivated.connect(act.ListClick)
ui.wdgList.customContextMenuRequested.connect(act.ContextMenu)
ui.actDownload.triggered.connect(act.DownloadAction)
ui.actShowList.triggered.connect(act.BackToBookList)
ui.actGenerate.triggered.connect(act.GenerateBook)

# Update List
act.UpdateList()

# Start Qt
MainWindow.show()
sys.exit(app.exec_())











