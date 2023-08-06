from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtUiTools import QUiLoader
import copy
from source.frontend.util.document import Document
from source.backend.interface import *
from math import floor
from copy import deepcopy
from threading import Thread

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#GUI actions for the Results tab

class ClickCanvas(FigureCanvas):

    def __init__(self, fig, window):
        FigureCanvas.__init__(self,fig)
        self.window = window

class ResultsPage(QWidget):

    update_graph = Signal()

    def __init__(self, app):

        QWidget.__init__(self, parent=None)

        self.update_graph.connect(self.updateGraph)

        self.app = app
        self.mainWindow = app.window

        self.documents = []
        self.matchWidgets = []
        self.noDocs = False

        self.create_widgets()

    def create_widgets(self):

        self.docScrollArea = self.mainWindow.findChild(QScrollArea, "scrollArea")

        self.scrollContent = QWidget()
        self.scrollContent.setStyleSheet("background-color: rgb(220,220,220)")

        self.docScrollArea.setWidget(self.scrollContent)
        self.scrollContentLayout = QVBoxLayout(self.scrollContent)

        self.sortType = self.mainWindow.findChild(QComboBox, "comboBox")
        self.sortType.currentIndexChanged.connect(self.resort)

        self.matchScrollContent = QWidget()
        self.matchScrollContent.setStyleSheet("background-color: rgb(180,180,180)")

        self.mainWindow.findChild(QScrollArea, "scrollArea_4").setWidget(self.matchScrollContent)
        self.matchScrollContentLayout = QVBoxLayout(self.matchScrollContent)

        self.selectedDocument = self.mainWindow.findChild(QLabel, "label_7")
        self.viewSelectedInfo = self.mainWindow.findChild(QPushButton, "pushButton_4")

        self.sendNum = self.mainWindow.findChild(QSpinBox, "spinBox")
        self.sendCurrentButton = self.mainWindow.findChild(QPushButton, "pushButton_2")
        self.sendAllButton = self.mainWindow.findChild(QPushButton, "pushButton_6")

        self.sendCurrentButton.clicked.connect(self.sendCurrentDoc)
        self.sendAllButton.clicked.connect(self.sendAllDocs)

        self.graph = self.mainWindow.findChild(QFrame, "frame_4")
        self.graphLayout = QVBoxLayout(self.graph)

        self.figure, self.axes = plt.subplots(1, figsize=(1, 1))
        self.axes.set_axis_off()
        self.axes.set_position([0, 0, 1, 1])
        self.canvas = FigureCanvas(self.figure)
        self.graphLayout.addWidget(self.canvas)


        self.add_documents()

        #for i in range(10):
            #self.add_document(i)

        #self.resort()
        #self.documents[0].viewDocInfo()

    def add_documents(self):

        # Clear Existing Results

        self.viewSelectedInfo.clicked.connect(self.doNothing)

        for i in range(len(self.documents)):
            self.remove_doc()

        for i in range(len(self.matchWidgets)):
            self.matchWidgets[-1].deleteLater()
            self.matchWidgets.pop()

        self.axes.clear()
        self.updateGraph()
        self.selectedDocument.setText("")

        self.mainWindow.findChild(QLabel, "label_5").setText("Document Name: ")
        self.mainWindow.findChild(QLabel, "label_5").setWordWrap(True)
        self.mainWindow.findChild(QLabel, "label_27").setText("Percentage Matched: ")
        self.mainWindow.findChild(QLabel, "label_31").setText("Documents Matched: ")
        self.mainWindow.findChild(QLabel, "label_4").setText("Total Fingerprints Found: ")

        # Add New Results
        if self.app.db.getfileslist().count() > 0:

            if self.noDocs == True:
                self.noDocLabel.deleteLater()
                self.noDocs = False

            # C
            if self.app.db.searchParams[1] == 0:

                fileList = []
                boilerList = []
                for i in range(self.app.db.getfileslist().count()):
                    fileList.append(self.app.db.getfileslist().item(i).text())
                for i in range(self.app.db.boilerDBList.count()):
                    boilerList.append(self.app.db.boilerDBList.item(i).text())

                filetofp_obj = compare_multiple_files_c(fileList, self.app.db.searchParams[3],
                                                          self.app.db.searchParams[4], boilerList,
                                                          self.app.db.searchParams[2])

                self.app.db.boilerFPList = []
                tempList = []

                for boilerItem in boilerList:
                    tempList.append(get_winnow_fps_c(boilerItem, boilerItem, self.app.db.searchParams[3],
                                                      self.app.db.searchParams[4], []))

                self.app.db.boilerFPList = deepcopy(tempList)

                for f2fp_main in filetofp_obj:

                    docName = f2fp_main.filename
                    docPlagarized = floor(f2fp_main.similarity * 100) / 100
                    docMatchCount = 0
                    docMatchNames = []
                    docMatchPercent = []

                    for f2fp_other in filetofp_obj:
                        if f2fp_other in f2fp_main.similarto:
                            docMatchNames.append(f2fp_other.filename)
                            docMatchPercent.append(
                                compare_files_c(f2fp_main.filename, f2fp_other.filename, self.app.db.searchParams[3],
                                                  self.app.db.searchParams[4], boilerList))

                    docMatchCount = len(docMatchNames)
                    tempDoc = Document(self, docName, docPlagarized, docMatchCount, docMatchNames, docMatchPercent, f2fp_main.graph)
                    self.documents.append(tempDoc)

            # C++
            elif self.app.db.searchParams[1] == 1:

                fileList = []
                boilerList = []
                for i in range(self.app.db.getfileslist().count()):
                    fileList.append(self.app.db.getfileslist().item(i).text())
                for i in range(self.app.db.boilerDBList.count()):
                    boilerList.append(self.app.db.boilerDBList.item(i).text())

                filetofp_obj = compare_multiple_files_cpp(fileList, self.app.db.searchParams[3], self.app.db.searchParams[4], boilerList, self.app.db.searchParams[2])

                self.app.db.boilerFPList = []
                tempList = []

                for boilerItem in boilerList:
                    tempList.append(get_winnow_fps_cpp(boilerItem, boilerItem, self.app.db.searchParams[3],
                                                      self.app.db.searchParams[4], []))

                self.app.db.boilerFPList = deepcopy(tempList)

                for f2fp_main in filetofp_obj:

                    docName = f2fp_main.filename
                    docPlagarized = floor(f2fp_main.similarity * 100) / 100
                    docMatchCount = 0
                    docMatchNames = []
                    docMatchPercent = []

                    for f2fp_other in filetofp_obj:
                        if f2fp_other in f2fp_main.similarto:
                            docMatchNames.append(f2fp_other.filename)
                            docMatchPercent.append(compare_files_cpp(f2fp_main.filename, f2fp_other.filename, self.app.db.searchParams[3], self.app.db.searchParams[4], boilerList))

                    docMatchCount = len(docMatchNames)
                    tempDoc = Document(self, docName, docPlagarized, docMatchCount, docMatchNames, docMatchPercent, f2fp_main.graph)
                    self.documents.append(tempDoc)

            # Java
            elif self.app.db.searchParams[1] == 2:

                fileList = []
                boilerList = []
                for i in range(self.app.db.getfileslist().count()):
                    fileList.append(self.app.db.getfileslist().item(i).text())
                for i in range(self.app.db.boilerDBList.count()):
                    boilerList.append(self.app.db.boilerDBList.item(i).text())

                filetofp_obj = compare_multiple_files_java(fileList, self.app.db.searchParams[3], self.app.db.searchParams[4], boilerList, self.app.db.searchParams[2])

                self.app.db.boilerFPList = []
                tempList = []

                for boilerItem in boilerList:
                    tempList.append(get_winnow_fps_java(boilerItem, boilerItem, self.app.db.searchParams[3],
                                                      self.app.db.searchParams[4], []))

                self.app.db.boilerFPList = deepcopy(tempList)

                for f2fp_main in filetofp_obj:

                    docName = f2fp_main.filename
                    docPlagarized = floor(f2fp_main.similarity * 100) / 100
                    docMatchCount = 0
                    docMatchNames = []
                    docMatchPercent = []

                    for f2fp_other in filetofp_obj:
                        if f2fp_other in f2fp_main.similarto:
                            docMatchNames.append(f2fp_other.filename)
                            docMatchPercent.append(compare_files_java(f2fp_main.filename, f2fp_other.filename, self.app.db.searchParams[3], self.app.db.searchParams[4], boilerList))

                    docMatchCount = len(docMatchNames)
                    tempDoc = Document(self, docName, docPlagarized, docMatchCount, docMatchNames, docMatchPercent, f2fp_main.graph)
                    self.documents.append(tempDoc)

            # Python
            else:

                fileList = []
                boilerList = []
                for i in range(self.app.db.getfileslist().count()):
                    fileList.append(self.app.db.getfileslist().item(i).text())
                for i in range(self.app.db.boilerDBList.count()):
                    boilerList.append(self.app.db.boilerDBList.item(i).text())

                filetofp_obj = compare_multiple_files_py(fileList, self.app.db.searchParams[3], self.app.db.searchParams[4], boilerList, self.app.db.searchParams[2])

                self.app.db.boilerFPList = []
                tempList = []

                for boilerItem in boilerList:
                    tempList.append(get_winnow_fps_py(boilerItem, boilerItem, self.app.db.searchParams[3], self.app.db.searchParams[4], []))

                self.app.db.boilerFPList = deepcopy(tempList)

                for f2fp_main in filetofp_obj:

                    docName = f2fp_main.filename
                    docPlagarized = floor(f2fp_main.similarity * 100) / 100
                    docMatchCount = 0
                    docMatchNames = []
                    docMatchPercent = []

                    for f2fp_other in filetofp_obj:
                        if f2fp_other in f2fp_main.similarto:
                            docMatchNames.append(f2fp_other.filename)
                            docMatchPercent.append(compare_files_py(f2fp_main.filename, f2fp_other.filename, self.app.db.searchParams[3], self.app.db.searchParams[4], boilerList))

                    docMatchCount = len(docMatchNames)
                    tempDoc = Document(self, docName, docPlagarized, docMatchCount, docMatchNames, docMatchPercent, f2fp_main.graph)
                    self.documents.append(tempDoc)

            self.resort()

        else:
            if self.noDocs == False:
                self.noDocLabel = QLabel()
                self.noDocLabel.setText("Please complete a search to view results here...")
                self.scrollContentLayout.addWidget(self.noDocLabel)
                self.noDocs = True

    def remove_doc(self):
        self.documents[-1].widget.deleteLater()
        self.documents.pop()

    def resort(self):
        if self.sortType.currentIndex() == 0:
            self.documents.sort(reverse=True, key=self.percentSort)
        else:
            self.documents.sort(reverse=True, key=self.countSort)

        for doc in self.documents:
            self.scrollContentLayout.removeWidget(doc.widget)

        for i in range(len(self.documents)):
            self.scrollContentLayout.addWidget(self.documents[i].widget)

        
    def percentSort(self, doc):
        return doc.percentMatch

    def countSort(self, doc):
        return doc.matchCount

    def updateGraph(self):
        self.canvas.draw()
        self.viewSelectedInfo.clicked.connect(self.doNothing)

# Method of highlighting from NetworkX extension library Grave:
# https://networkx.org/grave/latest/gallery/node_picking.html#

    def selectNode(self, event):

        print("SELECTING NODE")
        self.viewSelectedInfo.clicked.connect(self.doNothing)

        if not hasattr(event, 'nodes') or not event.nodes:
            return

        print("NOT RETURNING")

        graph = event.artist.graph

        for node, attributes in graph.nodes.data():
            if attributes["size"] == 200:
                attributes.pop("color", None)
            elif attributes["size"] == 400:
                attributes["color"] = 'r'

        for node in event.nodes:
            graph.nodes[node]['color'] = 'y'

        for node in event.nodes:
            print(node)

            for doc in self.documents:
                if doc.documentName == node:
                    self.selectedDocument.setText(doc.documentName)
                    self.viewSelectedInfo.clicked.connect(doc.viewDocInfo)


        event.artist.stale = True
        event.artist.figure.canvas.draw_idle()

        self.canvas.draw()

    def doNothing(self):
        pass

    def sendByThreshold(self, doc, percentNum):
        for i in range(len(doc.matchList)):
            if doc.matchPercentAndFP[i][0] >= percentNum:
                doc.sendCompare(doc.matchList[i])

    def sendCurrentDoc(self):
        docName = self.mainWindow.findChild(QLabel, "label_5").text()[15:]

        for doc in self.documents:
            if doc.documentName == docName:
                self.sendByThreshold(doc, self.sendNum.value())
                return

    def sendAllDocs(self):
        for doc in self.documents:
            self.sendByThreshold(doc, self.sendNum.value())

        self.app.findChild(QTabWidget, "tabWidget").setCurrentWidget(
            self.app.findChild(QWidget, "Compare"))

