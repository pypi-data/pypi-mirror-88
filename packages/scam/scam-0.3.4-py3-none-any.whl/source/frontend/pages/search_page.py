import os
import time
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import os

from source.backend.interface import *


#GUI actions for the Search tab

class SearchPage(QWidget):

    def __init__(self, app):

        QWidget.__init__(self, parent=app)

        self.app = app
        self.mainWindow = app.window

        self.db = self.app.db

        self.searchMap = dict()

        self.create_widgets()

    def create_widgets(self):

        #File Addition/Removal
        self.mainWindow.findChild(QPushButton, "addBoilerplate").clicked.connect(self.addBoilerplate)
        self.mainWindow.findChild(QPushButton, "addStudent").clicked.connect(self.addStudent)
        self.mainWindow.findChild(QPushButton, "clearBoilerplate").clicked.connect(self.clearBoilerplate)
        self.mainWindow.findChild(QPushButton, "clearStudent").clicked.connect(self.clearStudent)

        self.studentFileList = self.mainWindow.findChild(QListWidget, "studentFileListWidget")
        self.boilerplateFileList = self.mainWindow.findChild(QListWidget, "boilerplateFileListWidget")
        self.fileList = QListWidget(self) #self.mainWindow.findChild(QListWidget, "filesListWidget")

        #Basic Search Parameters
        self.autoSearch = self.mainWindow.findChild(QComboBox, "searchSettingsBox") # 1 for Manual, 0 for Automatic

        self.searchLang = self.mainWindow.findChild(QComboBox, "langBox") # 0 for C/C++, 1 for Java, 2 for Python, 3 for Text
        self.ignoreCount = self.mainWindow.findChild(QSpinBox, "ignoreBox")
        self.ignoreCount.setValue(1)

        #Advanced Search Parameters
        self.kGrams = self.mainWindow.findChild(QSpinBox, "kGramsSpinbox")
        self.kGrams.setValue(10)
        self.windowSize = self.mainWindow.findChild(QSpinBox, "windowSizeSpinbox")

        self.kGrams.setValue(10)
        self.windowSize.setValue(5)
        self.windowSize.setValue(5)

        #Output
        self.outputDisplay = self.mainWindow.findChild(QTextEdit, "outputText")
        self.outputDisplay.setReadOnly(True)

        #Run/Clear/Save Search
        self.mainWindow.findChild(QPushButton, "compareButton").clicked.connect(self.compare)
        self.mainWindow.findChild(QPushButton, "clearButton").clicked.connect(self.clearOutput)
        self.mainWindow.findChild(QPushButton, "defaultButton").clicked.connect(self.defaultSettings)

        self.mainWindow.findChild(QPushButton, "saveButton").clicked.connect(self.genReport)

        self.boilerfilenames = []
        self.studentfilenames = []

    #File Addition/Removal

    def addBoilerplate(self):

        if self.searchLang.currentIndex() == 0:
            self.boilerfilenames,_ = QFileDialog.getOpenFileNames(self.mainWindow, "Open Boilerplate Files", os.getcwd() + "./", "C/C++ Files (*.c *.cpp *.h *.hpp);; Java Files (*.class *.java);; Python Files (*.py);; All Files (*.*)")
        elif self.searchLang.currentIndex() == 1:
            self.boilerfilenames, _ = QFileDialog.getOpenFileNames(self.mainWindow, "Open Boilerplate Files", os.getcwd() + "./", "C/C++ Files (*.c *.cpp *.h *.hpp);; Java Files (*.class *.java);; Python Files (*.py);; All Files (*.*)")
        elif self.searchLang.currentIndex() == 2:
            self.boilerfilenames,_ = QFileDialog.getOpenFileNames(self.mainWindow, "Open Boilerplate Files", os.getcwd() + "./", "Java Files (*.class *.java);; C/C++ Files (*.c *.cpp *.h *.hpp);; Python Files (*.py);; All Files (*.*)")
        else:
            self.boilerfilenames, _ = QFileDialog.getOpenFileNames(self.mainWindow, "Open Boilerplate Files", os.getcwd() + "./", "Python Files (*.py);; C/C++ Files (*.c *.cpp *.h *.hpp);; Java Files (*.class *.java);; All Files (*.*)")

        if len(self.boilerfilenames):
            for names in range(0,len(self.boilerfilenames)):
                self.boilerplateFileList.addItem(QListWidgetItem(self.boilerfilenames[names]))
        else:
            self.outputDisplay.append("There were no boilerplate files have been added by user. Unnecessary for source code analysis")



    def addStudent(self):

        if self.searchLang.currentIndex() == 0:
            self.studentfilenames,_ = QFileDialog.getOpenFileNames(self.mainWindow, "Open Student Files", os.getcwd() + "./", "C/C++ Files (*.c *.cpp *.h *.hpp);; Java Files (*.class *.java);; Python Files (*.py);; All Files (*.*)")
        elif self.searchLang.currentIndex() == 1:
            self.studentfilenames, _ = QFileDialog.getOpenFileNames(self.mainWindow, "Open Student Files", os.getcwd() + "./", "C/C++ Files (*.c *.cpp *.h *.hpp);; Java Files (*.class *.java);; Python Files (*.py);; All Files (*.*)")
        elif self.searchLang.currentIndex() == 2:
            self.studentfilenames,_ = QFileDialog.getOpenFileNames(self.mainWindow, "Open Student Files", os.getcwd() + "./", "Java Files (*.class *.java);; C/C++ Files (*.c *.cpp *.h *.hpp);; Python Files (*.py);; All Files (*.*)")
        else:
            self.studentfilenames, _ = QFileDialog.getOpenFileNames(self.mainWindow, "Open Student Files", os.getcwd() + "./", "Python Files (*.py);; C/C++ Files (*.c *.cpp *.h *.hpp);; Java Files (*.class *.java);; All Files (*.*)")

        if len(self.studentfilenames) > 0:
            for names in range(0,len(self.studentfilenames)):
                self.studentFileList.addItem(QListWidgetItem(self.studentfilenames[names]))
            #self.studentFileList.addItem(QListWidgetItem("Test Item #%i" % (self.studentFileList.count() + 1)))
        else:
            self.outputDisplay.append("There were no Student files have been added by user. Necessary for source code analysis.")

    def clearBoilerplate(self):
        self.boilerplateFileList.clear()

    def clearStudent(self):
        self.studentFileList.clear()

    #Basic Search Parameters

    def setSearchType(self):
        if self.sender().isChecked() == True:
            self.searchType = 1
        else:
            self.searchType = 0

    def compare(self):

        self.clearOutput()

        self.db.setfileslist(self.studentFileList)
        self.db.boilerDBList = self.boilerplateFileList
        self.db.boilerFPList = []

        if self.autoSearch.currentIndex() == 1:
            self.db.searchParams = [self.autoSearch.currentIndex(),
                                    self.searchLang.currentIndex(), self.ignoreCount.value(),
                                    self.kGrams.value(), self.windowSize.value()]
        else:

            tempFiles = []
            for i in range(self.studentFileList.count()):
                tempFiles.append(self.studentFileList.item(i).text())
            for i in range(self.boilerplateFileList.count()):
                tempFiles.append(self.boilerplateFileList.item(i).text())

            if self.searchLang.currentIndex() == 0:
                tempK, tempW = set_params(tempFiles, -1, -1, "c")
            elif self.searchLang.currentIndex() == 1:
                tempK, tempW = set_params(tempFiles, -1, -1, "cpp")
            elif self.searchLang.currentIndex() == 2:
                tempK, tempW = set_params(tempFiles, -1, -1, "java")
            elif self.searchLang.currentIndex() == 3:
                tempK, tempW = set_params(tempFiles, -1, -1, "python")

            print(str(tempK) + " - " + str(tempW))

            self.db.searchParams = [self.autoSearch.currentIndex(),
                                    self.searchLang.currentIndex(), self.ignoreCount.value(),
                                    tempK, tempW]

        self.similar()

        self.outputDisplay.clear()

        for i in reversed(sorted(self.searchMap.keys())):
            # print(self.searchMap[i])
            self.outputDisplay.append(self.searchMap[i])

        self.app.update_compare.emit()

        self.toResultsTab()

    def toResultsTab(self):
        self.app.findChild(QTabWidget, "tabWidget").setCurrentWidget(self.app.findChild(QWidget, "Results"))

    def clearOutput(self):
        self.outputDisplay.clear()
        self.db.searchParams = []
        self.fileList.clear()

    def defaultSettings(self):
        self.autoSearch.setCurrentIndex(0)
        self.ignoreCount.setValue(1)
        self.kGrams.setValue(10)
        self.windowSize.setValue(5)

    def genReport(self):

        current_time = time.strftime("%Y-%m-%d_%H-%M-%S")

        self.genFileName, _ = QFileDialog.getSaveFileName(self.mainWindow, "Save File", "SCAM_REPORT_"
                                                          + str(current_time) + ".txt", "Text (*.txt)")

        if self.genFileName:
            self.outputDisplay.clear()
            self.outputDisplay.append("SCAM report gernerated at:\n\t"+self.genFileName)
            self.genFile = open(self.genFileName, 'w')

            self.genFile.write('\n\t\tSCAM General report\n\n')

            self.genFile.write("\nKgrams currently set to:"+ str(self.kGrams.value()))
            self.outputDisplay.append("Kgrams currently set to:"+ str(self.kGrams.value()))
            self.genFile.write("\nWindow currently set to: "+ str(self.windowSize.value()))
            self.outputDisplay.append("Window currently set to:"+ str(self.windowSize.value()))

            self.genFile.write("\n\nNOTE: The larger the k-gram value is, the more likely it is the fingerprint found was a\n "
                               "true copy, but making it smaller makes it better able to detect reordering/repositioning\n"
                               "of something copied and can find smaller matches. Window size determines the size of the\n"
                               "window used in the winnowing algorithm.\n")

            self.similar()

            self.genFile.write("\n")

            for i in reversed(sorted(self.searchMap.keys())):
                #print(self.searchMap[i])
                self.outputDisplay.append(self.searchMap[i])
                self.genFile.write("\n" + self.searchMap[i])

            self.genFile.close()


    def similar(self):

        boilerList = []
        for i in range(self.boilerplateFileList.count()):
            boilerList.append(self.boilerplateFileList.item(i).text())

        totalStuds = self.studentFileList.count()
        for studA in range(0,totalStuds):
            for studB in range(0,totalStuds):
                if studA == studB or studA > studB:
                    continue

                self.studFileA = self.studentFileList.item(studA).text()
                self.studFileB = self.studentFileList.item(studB).text()

                self.studFileNameA = os.path.basename(self.studFileA)
                self.studFileNameB = os.path.basename(self.studFileB)

                # C
                if self.searchLang.currentIndex() == 0:
                    commonality = compare_files_c(self.studFileA, self.studFileB,
                                                   self.kGrams.value(), self.windowSize.value(), boilerList)

                # C++
                elif self.searchLang.currentIndex() == 1:
                    commonality = compare_files_cpp(self.studFileA, self.studFileB,
                                                 self.kGrams.value(), self.windowSize.value(), boilerList)

                # Java
                elif self.searchLang.currentIndex() == 2:
                    commonality = compare_files_java(self.studFileA, self.studFileB,
                                                 self.kGrams.value(), self.windowSize.value(), boilerList)

                # Python
                else:
                    commonality = compare_files_py(self.studFileA, self.studFileB,
                                                 self.kGrams.value(), self.windowSize.value(), boilerList)
                self.studStr = str("\n"+ self.studFileNameA + " has " + str(
                    round(commonality[0], 2)) + "% similarity when \ncompared to " + self.studFileNameB + " and " + str(commonality[1]) + " fingerprints in common.")
                self.searchMap.update({ round(commonality[0],2) : self.studStr})


