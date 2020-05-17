import csv
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
import DTID3_Class#, DataFrameModel 
from Working_with_file import make_folder
import pandas as pd
import pprint
import json

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('DTID3_GUI.ui', self)
        self.model = QtGui.QStandardItemModel(self)

        self._set_icon()

        self.btnImport.clicked.connect(self.on_Import_clicked)
        self.btnExport.clicked.connect(self.on_Export_clicked)
        self.btnSave.clicked.connect(self.on_Save_clicked)
        self.btnAdd.clicked.connect(self.on_Add_clicked)
        self.btnId3.clicked.connect(self.on_Id3_clicked)
        self.btnPredict.clicked.connect(self.on_Predict_clicked)
        self.lineEditPredict.textChanged.connect(self.on_textchanged)
        self.tableViewInput.setModel(self.model)

        self.lineEditPredict.setDisabled(True)
        self.btnExport.setDisabled(True)
        self.btnSave.setDisabled(True)
        self.btnAdd.setDisabled(True)
        self.btnId3.setDisabled(True)
        self.btnPredict.setDisabled(True)
        
        # self.tableViewInput.horizontalHeader().setStretchLastSection(True) #optional

        self.fileName = ''
        self.inputDir = './input/'
        self.listInput = []
        self.posClassify = -1
        self.tree = DTID3_Class.DTreeID3(self.posClassify)

    def _set_icon(self):
        imgDir = './GUI_image/'
        openIcon = QtGui.QIcon(imgDir + 'openIcon')
        saveIcon = QtGui.QIcon(imgDir + 'saveIcon')
        saveAsIcon = QtGui.QIcon(imgDir + 'saveAsIcon')
        runIcon = QtGui.QIcon(imgDir + 'runIcon')
        pixmapLogo = QtGui.QPixmap(imgDir + 'logoIconLarge')
        resIcon = QtGui.QIcon(imgDir + 'saveResIcon')
        addRowIcon = QtGui.QIcon(imgDir + 'addRowIcon')
        deleteRowIcon = QtGui.QIcon(imgDir + 'deleteRowIcon')
        predictIcon = QtGui.QIcon(imgDir + 'predictIcon')

        self.btnImport.setIcon(openIcon)
        self.btnExport.setIcon(saveAsIcon)
        self.btnSave.setIcon(saveIcon)
        self.btnId3.setIcon(runIcon)
        self.btnAdd.setIcon(addRowIcon)
        self.btnDelete.setIcon(deleteRowIcon)
        self.btnPredict.setIcon(predictIcon)        
        self.labelLogo.setPixmap(pixmapLogo)
        
    def on_textchanged(self):
        self.labelPredict.clear()

    def on_Add_clicked(self):
        self.model.appendRow([])

    def on_Export_clicked(self):
        (dataPath, _) = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File', self.inputDir, '*.csv')
        fileName = dataPath.split('/')[-1]
        if dataPath:
            self._export_file(fileName)

    def _export_file(self, fileName: str):
        with open(self.inputDir + fileName, 'w') as fileOutput:
            writer = csv.writer(fileOutput, lineterminator='\n')
            for rowNumber in range(self.model.rowCount()):
                fields = []
                for columnNumber in range(self.model.columnCount()):
                    fields.append(self.model.data(self.model.index(rowNumber, columnNumber), QtCore.Qt.DisplayRole))
                writer.writerow(fields)

    def on_Save_clicked(self):
        self._export_file(self.fileName)

    def _import_file(self, fileName):
        with open(self.inputDir + self.fileName, 'r', encoding = 'utf-8') as fileInput:
            rCount = 0
            for row in csv.reader(fileInput):    
                # if row[0] not in (None, ""):
                if row[0] != '':
                    items = []
                    cCount = 0
                    for field in row:
                        items.append(QtGui.QStandardItem(field))
                        cCount += 1
                    rCount += 1
                    self.model.appendRow(items)
        self.labelInputCount.setText('{}. {} dòng {} cột'.format(self.fileName, rCount, cCount))

    def _get_list_from_QStandardItemModel(self) -> list:
        listInput = []
        for rowNumber in range(self.model.rowCount()):
            row = []
            for columnNumber in range(self.model.columnCount()):
                cell = self.model.data(self.model.index(rowNumber, columnNumber), QtCore.Qt.DisplayRole)
                row.append(cell)
            listInput.append(row)
        return listInput
        

    def on_Import_clicked(self):
        self.labelInputCount.clear()
        self.labelInputName.setText('Dữ liệu')
        
        (dataPath, _) = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', self.inputDir, '*.csv')
        self.fileName = dataPath.split('/')[-1]
        if dataPath:
            self.model.clear()
            self._import_file(self.fileName)
            
            self.listInput = self._get_list_from_QStandardItemModel()

            self.plainTextDTree.clear()
            
            self.btnExport.setDisabled(False)
            self.btnAdd.setDisabled(False)
            self.btnId3.setDisabled(False)
            self.btnSave.setDisabled(False)
            

    def on_Id3_clicked(self):
        self.tree = DTID3_Class.DTreeID3(self.posClassify)
        self.tree._set_inputData(self.listInput)
        self.tree._run()
        self.tree._get_all_branch()
        strAllBranch = ''
        for branch in self.tree.listBranchStr:
            strAllBranch += branch + '\n' 
        self.plainTextDTree.insertPlainText(strAllBranch)
        # Hint ở ô dự đoán dữ liệu mới.
        strHint = 'Ví dụ:'
        for index in range(1, len(self.tree.listObject[0]) - 1):
            strHint += ' ' + self.tree.listObject[0][index]
        
        self.lineEditPredict.setPlaceholderText(strHint)
        self.lineEditPredict.setDisabled(False)
        self.btnPredict.setDisabled(False)


    def on_Predict_clicked(self):
        newValueStr = self.lineEditPredict.text()
        if newValueStr == '':
            self.labelPredict.setText('Chưa nhập giá trị.')
        else:
            res = self.tree._predict(newValueStr)
            self.labelPredict.setText('--> {}  '.format(res))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MyWindow()
    window.setWindowTitle('CÂY QUYẾT ĐỊNH ID3')
    window.show()
    sys.exit(app.exec_())
