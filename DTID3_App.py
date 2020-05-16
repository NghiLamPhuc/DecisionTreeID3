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

        self.btnImport.clicked.connect(self.on_Import_clicked)
        self.btnId3.clicked.connect(self.on_Id3_clicked)
        self.btnPredict.clicked.connect(self.on_Predict_clicked)
        self.lineEditPredict.setDisabled(True)
        self.lineEditPredict.textChanged.connect(self.on_textchanged)
        
        self.df = pd.DataFrame()
        self.attributes = list()
        self.tree = dict()

    def on_textchanged(self):
        self.labelPredict.clear()

    def on_Import_clicked(self):
        self.labelInputCount.clear()
        self.labelInputName.setText('Dữ liệu')
        
        inputDir = './input/'
        (dataPath, _) = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', inputDir, '*.csv')
        fileName = dataPath.split('/')[-1]
        if dataPath:
            dataFrame = ID3.import_data(inputDir, fileName)

            self.attributes = list(dataFrame.columns.values)[: len(list(dataFrame.columns.values)) - 1]
            
            model = DataFrameModel.DataFrameModel(dataFrame)
            self.tableViewInput.setModel(model)
            
            self.labelInputCount.setText('{} dòng. {} cột.'.format(model._dataframe.shape[0], model._dataframe.shape[1]) )
            self.labelInputName.setText(dataPath.split('/')[-1])
             
            self.df = model._dataframe
            
            # Hint bang placeholdertext cho o lineEditText.
            firstValueRow = list(dataFrame.iloc[0])[:len(list(dataFrame.iloc[0])) - 1]
            firstRowStr = 'Ví dụ : '
            for value in range(len(firstValueRow) - 1):
                firstRowStr += str(firstValueRow[value]) + ','
            firstRowStr += str(firstValueRow[-1])
            firstRowStr = firstRowStr.rstrip()
            self.lineEditPredict.setPlaceholderText(firstRowStr)
            # set enabled lineeditPredict
            self.lineEditPredict.setDisabled(False)

    def on_Id3_clicked(self):
        self.tree = ID3.buildTree(self.df)
        pprint.pprint(self.tree)
        # self.plainTextDTree.toPlainText(tree_str)
        
    def on_Predict_clicked(self):
        instanceDict = dict()
        instanceStr = self.lineEditPredict.text()
        if not instanceStr:
            self.labelPredict.setText('Chưa nhập giá trị.')
        if not self.tree:
            self.labelPredict.setText('Chưa có cây quyết định.')
        if instanceStr:
            instanceList = instanceStr.split(',')
            for index in range(len(self.attributes)):
                instanceDict[self.attributes[index]] = instanceList[index]

            instanceDict = pd.Series(instanceDict)
            predictInstance = ID3.predict(instanceDict, self.tree)
            self.labelPredict.setText('-->{}   '.format(predictInstance))
            make_folder.create_folder('./Output/')
            predictNameFile = 'predict ' + self.labelInputName.text() + '.txt'
            with open('./Output/' + predictNameFile, 'a', encoding = 'utf-8') as f:
                f.write(instanceStr + '-->{}\n'.format(predictInstance))
                


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MyWindow()
    window.setWindowTitle('CÂY QUYẾT ĐỊNH ID3')
    window.show()
    sys.exit(app.exec_())
