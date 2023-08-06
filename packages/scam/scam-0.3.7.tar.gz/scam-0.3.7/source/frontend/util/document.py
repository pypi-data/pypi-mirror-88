from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtUiTools import QUiLoader
from functools import partial
from math import floor
import os
import networkx as nx
from grave import plot_network
from grave.style import use_attributes

class Document:

    @property
    def widget(self):
        return self._widget

    @widget.setter
    def widget(self, new_widget):
        self._widget = new_widget


    @property
    def documentName(self):
        return self._documentName

    @documentName.setter
    def documentName(self, new_name):
        self._documentName = new_name


    @property
    def percentMatch(self):
        return self._percentMatch

    @percentMatch.setter
    def percentMatch(self, new_percent):
        self._percentMatch = new_percent


    @property
    def matchCount(self):
        return self._matchCount

    @matchCount.setter
    def matchCount(self, new_match):
        self._matchCount = new_match
    

    @property
    def matchList(self):
        return self._matchList

    @matchList.setter
    def matchList(self, new_list):
        self._matchList = new_list

    def __init__(self, app, docName, pMatch, numMatch, matchNames, matchPercent, graph):

        self.app = app

        ui_file = QFile("frontend/gui/doc_obj.ui")
        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        self.widget = loader.load(ui_file, self.app).findChild(QWidget, "docObject")

        ui_file.close()

        self.documentName = docName
        self.percentMatch = pMatch
        self.matchCount = numMatch
        self.matchList = matchNames
        self.matchPercentAndFP = matchPercent
        self.graph = graph

        self.create_widget()

    def create_widget(self):

        self.widgetDocName = self.widget.findChild(QLabel, "docNameLabel")
        self.widgetDocName.setText(self.documentName)

        self.widgetDocProgress = self.widget.findChild(QProgressBar, "progressBar")
        self.widgetDocProgress.setValue(self.percentMatch)

        self.widgetDocInfo = self.widget.findChild(QLabel, "docInfoLabel")
        self.widgetDocInfo.setText("   " + str(self.percentMatch) + "% Matching Content | " + str(self.matchCount) + " Documents Matched   ")

        self.docInfoButton = self.widget.findChild(QPushButton, "pushButton")
        self.docInfoButton.clicked.connect(self.viewDocInfo)

        self.app.scrollContentLayout.addWidget(self.widget)

    def viewDocInfo(self):

        self.plotGraph()

        for i in range(len(self.app.matchWidgets)):
            self.app.matchWidgets[-1].deleteLater()
            self.app.matchWidgets.pop()

        self.app.mainWindow.findChild(QLabel, "label_5").setText("Document Name: " + self._documentName)
        self.app.mainWindow.findChild(QLabel, "label_5").setWordWrap(True)
        self.app.mainWindow.findChild(QLabel, "label_27").setText("Percentage Matched: " + str(self.percentMatch) + "%")
        self.app.mainWindow.findChild(QLabel, "label_31").setText("Documents Matched: " + str(self.matchCount))

        totalFP = 0
        for i in range(len(self._matchList)):
            totalFP += self.matchPercentAndFP[i][1]

        self.app.mainWindow.findChild(QLabel, "label_4").setText("Total Fingerprints Found: " + str(totalFP))

        ui_file = QFile("frontend/gui/match_obj.ui")

        for i in range(len(self._matchList)):
            ui_file.open(QFile.ReadOnly)
            loader = QUiLoader()
            self.app.matchWidgets.append(loader.load(ui_file, self.app).findChild(QWidget, "docObject"))

            commonPrefix = os.path.commonprefix([self._matchList[i], self._documentName])
            self.app.matchWidgets[i].findChild(QLabel, "docNameLabel").setText(self._matchList[i][commonPrefix.rfind("/") + 1:])

            self.app.matchWidgets[i].findChild(QProgressBar, "progressBar").setValue(self.matchPercentAndFP[i][0])
            self.app.matchWidgets[i].findChild(QLabel, "docInfoLabel").setText("   " + str(floor(self.matchPercentAndFP[i][0] * 100) / 100) + "% Similar | " + str(self.matchPercentAndFP[i][1]) + " Fingerprints   ")
            self.app.matchWidgets[i].findChild(QPushButton, "pushButton").clicked.connect(partial(self.sendCompare, self._matchList[i]))
            self.app.matchScrollContentLayout.addWidget(self.app.matchWidgets[i])

            ui_file.close()

    def sendCompare(self, other_file):
        pMatchString = str(floor(self.matchPercentAndFP[self.matchList.index(other_file)][0] * 100) / 100) + "%"
        self.app.app.send_compare.emit([self._documentName, other_file, pMatchString])

    def plotGraph(self):

        G = self.graph[0]
        largest_node = self.graph[1]
        G.add_edge(largest_node, largest_node)

        for node in G.nodes:
            G.nodes[node]["size"] = 200
            G.nodes[node]["color"] = 'C0'

        G.nodes[largest_node]["size"] = 400
        G.nodes[largest_node]["color"] = "red"
        self.app.axes.clear()
        self.app.selectedDocument.setText("")

        graph = plot_network(G, layout="spring", ax=self.app.axes, node_style=use_attributes(), edge_style=use_attributes())
        graph.set_picker(10)
        self.app.canvas.mpl_connect('pick_event', self.app.selectNode)

        self.app.update_graph.emit()


