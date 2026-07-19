from MainCode.Main import *
from PyQt6.QtWidgets import QApplication

app=QApplication(sys.argv)
window=MainWindow(mode="offline")
window.show()
app.exec()
