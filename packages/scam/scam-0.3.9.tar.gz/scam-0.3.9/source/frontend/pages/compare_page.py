from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import os
from source.backend.interface import *
from source.backend.analyzer import remove_comments

#GUI actions for the Compare tab

class ComparePage(QWidget):

    def __init__(self, app):

        QWidget.__init__(self, parent=app)

        self.app = app
        self.mainWindow = app.window
        self.compMap = dict(dict())
        self.mapindex = 0
        self.fp_index = 0
        self.fp_total = 0

        self.create_widgets()

    def create_widgets(self):

        self.db = self.app.db

        #All Files list
        self.filesList = QListWidget(self)
        self.filesList.addItem(QListWidgetItem(self.db.getfileslist()))

        #Comparisons list
        self.compList = self.mainWindow.findChild(QListWidget, "filesListWidget")
        self.compList.setSelectionMode(QAbstractItemView.SingleSelection)

        #Comparison Buttons
        self.viewAll = self.mainWindow.findChild(QRadioButton, "radioButton")
        self.createReport = self.mainWindow.findChild(QPushButton, "pushButton")
        self.clearCompare = self.mainWindow.findChild(QPushButton, "pushButton_3")
        self.saveCompare = self.mainWindow.findChild(QPushButton, "saveButton")
        self.viewAll.toggled.connect(self.highlightFPs)
        self.clearCompare.clicked.connect(self.clearCompareFunc)

        #Fingerprint Buttons
        self.mainWindow.findChild(QPushButton, "prev_fingerprint").clicked.connect(self.prev_fp)
        self.mainWindow.findChild(QPushButton, "next_fingerprint").clicked.connect(self.next_fp)

        #File Comparison Displays
        self.A_display = self.mainWindow.findChild(QTextEdit, "compA_output")
        self.B_display = self.mainWindow.findChild(QTextEdit, "compB_output")
        self.A_title = self.mainWindow.findChild(QLabel, "FileA_Title")
        self.B_title = self.mainWindow.findChild(QLabel, "FileB_Title")

        self.compList.currentItemChanged.connect(self.displayFilesAB)

        #self.compList.currentItemChanged.connect(self.createCompareReport)
        self.createReport.clicked.connect(self.createCompareReport)

        self.clearing = False

        self.fp_label = self.mainWindow.findChild(QLabel, "label_32")

    def add_comparison(self, compareList):

        #{ mapindex : {'indexA': 'sample.py', 'IndexB': 'test.py', "comp2indexes": str(indexA , " compareTo ", indexB)}}
        #print("mapped: ", indexA, " comp2 ", indexB)
        strA = compareList[0]
        strB = compareList[1]

        comp2 = strA +  " compareTo " + strB

        self.compMap.update({  self.mapindex : { "indexA" : compareList[0],
                   "indexB" : compareList[1],
                   "display": comp2 } })

        commonPrefix = os.path.commonprefix([compareList[0], compareList[1]])

        comp2display = compareList[0][commonPrefix.rfind("/") + 1:]\
            + ' -- '\
            + "compared to"\
            + ' -- '\
            + compareList[1][commonPrefix.rfind("/") + 1:]\
            + "  -  Percent Match: " + compareList[2]

        self.compList.addItem(comp2display)
        self.mapindex += 1

        self.compList.setCurrentItem(self.compList.item(0))

        # for i in self.compMap:
        #     print(self.compMap[i]['display'])
        #     print(self.compList.item(i).text())

    def displayFilesAB(self):
        self.A_display.setReadOnly(False)
        self.B_display.setReadOnly(False)

        self.A_display.clear()
        self.B_display.clear()

        self.A_display.setReadOnly(True)
        self.B_display.setReadOnly(True)

        if not self.clearing:

            self.A_display.setReadOnly(False)
            self.B_display.setReadOnly(False)

            try:
                # print("indexA: ", self.compMap[self.compList.row(self.compList.currentItem())].get("indexA"))
                # print("indexB: ", self.compMap[self.compList.row(self.compList.currentItem())].get("indexB"))

                self.A_title.setText("File A Output: " + self.compMap[self.compList.row(self.compList.currentItem())].get("indexA"))
                self.B_title.setText("File B Output: " + self.compMap[self.compList.row(self.compList.currentItem())].get("indexB"))

                self.fileA = open(self.compMap[self.compList.row(self.compList.currentItem())].get("indexA"), 'r')
                self.fileB = open(self.compMap[self.compList.row(self.compList.currentItem())].get("indexB"), 'r')

                for lines in self.fileA.readlines():

                    if self.app.db.searchParams[1] < 3:
                        lines = remove_comments(lines)

                    self.A_display.moveCursor(QTextCursor.End)
                    self.A_display.insertPlainText(lines)

                for lines in self.fileB.readlines():

                    if self.app.db.searchParams[1] < 3:
                        lines = remove_comments(lines)

                    self.B_display.moveCursor(QTextCursor.End)
                    self.B_display.insertPlainText(lines)


                self.fileA.close()
                self.fileB.close()

            except FileNotFoundError:
                print("FNF: Try another selection")
            except KeyError:
                # print("KE: Try another selection")
                pass

            self.A_display.setReadOnly(True)
            self.B_display.setReadOnly(True)

            self.getFPs()



    def getFPs(self):

        boilerList = []

        for i in range(self.app.db.boilerDBList.count()):
            boilerList.append(self.app.db.boilerDBList.item(i).text())

        if self.app.db.searchParams[1] == 0:

            self.common_fp_obj = get_winnow_fps_c(self.compMap[self.compList.row(self.compList.currentItem())].get("indexA"),
                                             self.compMap[self.compList.row(self.compList.currentItem())].get("indexB"),
                                             self.app.db.searchParams[3],
                                             2,
                                             boilerList)



        elif self.app.db.searchParams[1] == 1:

            self.common_fp_obj = get_winnow_fps_cpp(self.compMap[self.compList.row(self.compList.currentItem())].get("indexA"),
                                             self.compMap[self.compList.row(self.compList.currentItem())].get("indexB"),
                                             self.app.db.searchParams[3],
                                             2,
                                             boilerList)

        elif self.app.db.searchParams[1] == 2:

            self.common_fp_obj = get_winnow_fps_java(self.compMap[self.compList.row(self.compList.currentItem())].get("indexA"),
                                             self.compMap[self.compList.row(self.compList.currentItem())].get("indexB"),
                                             self.app.db.searchParams[3],
                                             2,
                                             boilerList)

        else:

            self.common_fp_obj = get_winnow_fps_py(self.compMap[self.compList.row(self.compList.currentItem())].get("indexA"),
                                             self.compMap[self.compList.row(self.compList.currentItem())].get("indexB"),
                                             self.app.db.searchParams[3],
                                             2,
                                             boilerList)

        self.foundIndexes = []
        self.fp_total = 0
        self.fp_index = 0

        # Find and indicate safe found indexes
        for i in range(0, len(self.common_fp_obj.common)):

            goodA = False
            goodB = False

            substrArr1 = self.common_fp_obj.get_fps_substring(i, 0)
            for substr in substrArr1:
                found = self.highlightText(self.A_display, substr, 0)
                if found:
                    goodA = True

            substrArr2 = self.common_fp_obj.get_fps_substring(i, 1)
            for substr in substrArr2:
                found = self.highlightText(self.B_display, substr, 0)
                if found:
                    goodB = True

            if goodA and goodB:
                self.foundIndexes.append(i)
                self.fp_total += 1

        self.clearHighlights()

        self.highlightFPs()



    def highlightFPs(self):

        self.A_display.setReadOnly(False)
        self.B_display.setReadOnly(False)

        if self.viewAll.isChecked():

            self.fp_index = -1
            self.fp_label.setText("Fingerprint: 0/0")

            for i in range(0, self.fp_total):

                substrArr1 = self.common_fp_obj.get_fps_substring(self.foundIndexes[i], 0)
                for substr in substrArr1:

                    self.highlightText(self.A_display, substr, 0)

                substrArr2 = self.common_fp_obj.get_fps_substring(self.foundIndexes[i], 1)
                for substr in substrArr2:
                    self.highlightText(self.B_display, substr, 0)

            for bp_obj in self.app.db.boilerFPList:
                for i in range(len(bp_obj.common)):
                    substrArr = bp_obj.get_fps_substring(i, 0)
                    for substr in substrArr:
                        self.highlightText(self.A_display, substr, 1)
                        self.highlightText(self.B_display, substr, 1)

            self.A_display.moveCursor(QTextCursor.Start)
            self.A_display.ensureCursorVisible()

            self.B_display.moveCursor(QTextCursor.Start)
            self.B_display.ensureCursorVisible()

        else:
            self.clearHighlights()

            if self.fp_total > 0:
                if self.fp_index == -1:
                    self.fp_index = 0

                self.fp_label.setText("Fingerprint: " + str(self.fp_index + 1) + "/" + str(self.fp_total))

                substrArr1 = self.common_fp_obj.get_fps_substring(self.foundIndexes[self.fp_index], 0)
                for substr in substrArr1:
                    self.highlightText(self.A_display, substr, 0)

                substrArr2 = self.common_fp_obj.get_fps_substring(self.foundIndexes[self.fp_index], 1)
                for substr in substrArr2:
                    self.highlightText(self.B_display, substr, 0)

            for bp_obj in self.app.db.boilerFPList:
                for i in range(len(bp_obj.common)):
                    substrArr = bp_obj.get_fps_substring(i, 0)
                    for substr in substrArr:
                        self.highlightText(self.A_display, substr, 1)
                        self.highlightText(self.B_display, substr, 1)

        self.A_display.setReadOnly(True)
        self.B_display.setReadOnly(True)

    def prev_fp(self):

        if self.viewAll.isChecked() == False:
            self.fp_index -= 1
            if self.fp_index < 0:
                self.fp_index = self.fp_total - 1

            self.highlightFPs()

    def next_fp(self):

        if self.viewAll.isChecked() == False:
            self.fp_index += 1
            if self.fp_index >= self.fp_total:
                self.fp_index = 0

            self.highlightFPs()

    def clearHighlights(self):

        txtFormat = QTextCharFormat()
        txtFormat.setBackground(QBrush(QColor("white")))

        cursor_a = self.A_display.textCursor()
        cursor_b = self.B_display.textCursor()

        cursor_a.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor, 0)
        cursor_a.movePosition(QTextCursor.End, QTextCursor.KeepAnchor, 0)

        cursor_a.mergeCharFormat(txtFormat)

        cursor_b.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor, 0)
        cursor_b.movePosition(QTextCursor.End, QTextCursor.KeepAnchor, 0)

        cursor_b.mergeCharFormat(txtFormat)


    def highlightText(self, textBox, substring, bp):

        self.A_display.setReadOnly(False)
        self.B_display.setReadOnly(False)

        foundSomething = False

        txtFormat = QTextCharFormat()

        if bp == 0:
            txtFormat.setBackground(QBrush(QColor("yellow")))
        else:
            txtFormat.setBackground(QBrush(QColor(100, 200, 255)))

        index = textBox.toPlainText().find(substring)
        while index != -1:

            foundSomething = True

            cursor = textBox.textCursor()
            cursor.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor, 0)
            cursor.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor, index)
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(substring))
            cursor.mergeCharFormat(txtFormat)

            index = textBox.toPlainText().find(substring, index + len(substring), -1)

        self.A_display.setReadOnly(True)
        self.B_display.setReadOnly(True)

        return foundSomething

    def createCompareReport(self):

        self.reportA = os.path.basename(self.compMap[self.compList.row(self.compList.currentItem())].get("indexA"))
        self.reportB = os.path.basename(self.compMap[self.compList.row(self.compList.currentItem())].get("indexB"))

        self.A_name, _ = os.path.splitext(str(self.reportA))
        self.B_name, _ = os.path.splitext(str(self.reportB))

        self.compareFileName, _ = QFileDialog.getSaveFileName(self.mainWindow, "Save File", "FILE-"+str(self.A_name) + "-COMPARED_TO-" + str(
            self.B_name) + "-SCAM_REPORT.txt", "Text (*.txt)")
        if self.compareFileName:
            self.compareFile = open(self.compareFileName, 'w')

            self.compareFile.write('\n\n\t\t\tComparison SCAM report\n\n')

            self.compareFile.write(self.compList.currentItem().text() + "\n")
            self.compareFile.write(str(self.reportA) + " has " + str(round(self.similar()[0], 2)) + "% similarity when compared to " + str(self.reportB) + "\n")
            self.compareFile.write("\nTotal matched fingerprints = " + str(self.fp_total) + "\n")
            self.compareFile.write("K-gram equals " + str(self.app.db.searchParams[3]) +
                               "\nWindow size equals " + str(2) + "\n\n")

            self.compareFile.write("NOTE: The larger the k-gram value is, the more likely it is the fingerprint found was a\n "
                               "true copy, but making it smaller makes it better able to detect reordering/repositioning\n"
                               "of something copied and can find smaller matches. Window size determines the size of the\n"
                               "window used in the winnowing algorithm.\n")

            for i in range(0, self.fp_total):
                substrArr1 = self.common_fp_obj.get_fps_substring(self.foundIndexes[i], 0)

                self.compareFile.write("\n\n----- Fingerprint #" + str(i + 1) + " -----\n")
                for substr in substrArr1:
                    self.compareFile.write("\n*** " + str(self.reportA) + "'s matching fingerprint #" + str(i + 1) + ": ***\n" + str(substr) + "\n")

                self.compareFile.write("\n----------\n")
                substrArr2 = self.common_fp_obj.get_fps_substring(self.foundIndexes[i], 1)
                for substr in substrArr2:
                    self.compareFile.write("\n*** " + str(self.reportB) + "'s matching fingerprint #" + str(i + 1) + ": ***\n" + str(substr) + "\n")

            self.compareFile.close()


    def similar(self):

        self.simA = self.compMap[self.compList.row(self.compList.currentItem())].get("indexA")
        self.simB = self.compMap[self.compList.row(self.compList.currentItem())].get("indexB")

        # C
        if self.app.db.searchParams[1] == 0:
            boilerList = []
            for i in range(self.app.db.boilerDBList.count()):
                boilerList.append(self.app.db.boilerDBList.item(i).text())

            commonality = compare_files_c(self.simA, self.simB,
                                           self.app.db.searchParams[3], 2, boilerList)

        # C++
        elif self.app.db.searchParams[1] == 1:
            boilerList = []
            for i in range(self.app.db.boilerDBList.count()):
                boilerList.append(self.app.db.boilerDBList.item(i).text())

            commonality = compare_files_cpp(self.simA, self.simB,
                                         self.app.db.searchParams[3], 2, boilerList)

        # Java
        elif self.app.db.searchParams[1] == 2:
            boilerList = []
            for i in range(self.app.db.boilerDBList.count()):
                boilerList.append(self.app.db.boilerDBList.item(i).text())

            commonality = compare_files_java(self.simA, self.simB,
                                         self.app.db.searchParams[3], 2, boilerList)

        # Python
        else:
            boilerList = []
            for i in range(self.app.db.boilerDBList.count()):
                boilerList.append(self.app.db.boilerDBList.item(i).text())

            commonality = compare_files_py(self.simA, self.simB,
                                         self.app.db.searchParams[3], 2, boilerList)

        return commonality

    def clearCompareFunc(self):
        self.clearing = True
        self.compList.clear()
        self.mapindex = 0
        self.fp_index = 0
        self.fp_total = 0
        self.compMap.clear()
        self.compMap = dict(dict())
        self.A_title.setText("File A Output:")
        self.B_title.setText("File B Output")
        self.clearing = False

