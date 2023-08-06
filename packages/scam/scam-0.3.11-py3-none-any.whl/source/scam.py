import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from source.frontend.pages.search_page import *
from source.frontend.pages.results_page import *
from source.frontend.pages.compare_page import *

#SCAM Frontend
#Some structure/design inspired from Mistletoe: https://github.com/cacticouncil/mistletoe

class ScamApp(QMainWindow):

    @property
    def window(self):
        return self._window

    update_results = Signal()
    update_compare = Signal()
    send_compare = Signal(object)
    update_output = Signal()

    def __init__(self, filename):

            QMainWindow.__init__(self, parent=None)

            self.db = sharedDB()
            self.h = None

            #Load UI File
            ui_file = QFile(filename)
            ui_file.open(QFile.ReadOnly)
            loader = QUiLoader()
            ui_file.seek(0)
            self._window = loader.load(ui_file, self)

            ui_file.close()

            icon = QIcon("frontend/SCAM.png")
            self.setWindowIcon(icon)


            # self.button = QPushButton("Push for Window")
            # self.button.clicked.connect(self.show_new_window)
            # self.setCentralWidget(self.button)

            self.create_widgets()


    def create_widgets(self):

    #Search
        self.searchPage = SearchPage(self)
        #self.update_output.connect()

    #Results
        self.resultsPage = ResultsPage(self)
        self.update_compare.connect(self.resultsPage.add_documents)

    #Compare
        self.comparePage = ComparePage(self)

        self.send_compare.connect(self.comparePage.add_comparison)

        self.findChild(QAction, 'actionManual').triggered.connect(self.show_new_window)

    def show_new_window(self, checked):
        if self.h is None:
            self.h = HelpManu()
        self.h.show()

class HelpManu(QDialog):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        QDialog.__init__(self, parent=None)

        # Load UI File
        ui_file = QFile("frontend/gui/help_manual.ui")
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        ui_file.seek(0)
        self._window = loader.load(ui_file, self)
        ui_file.close()

        icon = QIcon("frontend/SCAM.png")
        self.setWindowIcon(icon)

    def closeEvent(self, event):
        event.ignore()
        self.hide()


class sharedDB:

    @property
    def searchParams(self):
        return self._searchParams

    @searchParams.setter
    def searchParams(self, new_params):
        self._searchParams = new_params

    @property
    def boilerDBList(self):
        return self._boilerDBList

    @boilerDBList.setter
    def boilerDBList(self, new_list):
        self._boilerDBList = new_list

    @property
    def boilerFPList(self):
        return self._boilerFPList

    @boilerFPList.setter
    def boilerFPList(self, new_list):
        self._boilerFPList = new_list

    def __init__(self):
        self._fileList = QListWidget()
        self._boilerDBList = QListWidget()
        self._searchParams = []
        self._boilerFPList = []

    def getfileslistNum(self):
        val = self._fileList.count()
        return val

    def getfileslist(self):
        return self._fileList

    def setfileslist(self, ex_fileList):
        self._fileList = ex_fileList

def main():

    app = QApplication(sys.argv)
    gui = ScamApp("frontend/gui/scam_gui.ui")
    gui.window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()