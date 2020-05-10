from Working_with_file import read_file, write_file, make_folder
import math
from collections import defaultdict

folderInput = 'input'
fileInput = 'weather'
folderOutFile = 'outfile'
fileLog = 'log'
fileType = ['.txt']
splitType = [', ', ' ']

class TreeNode():
    def __init__(self, name:str, isLeaf: bool):
        self.name = name
        self.isLeaf = isLeaf
        self.childs = None # dict of treenode (k:value of Attribute, v:TreeNode)

class DTreeID3():
    def __init__(self, listInput: list, posClassAttr: int):
        self.root = None
        self.listData = listInput
        self.listAttrName = self.listData[0]
        self.listObject = self.listData[1:]
        self.indexClassifyAttr = posClassAttr
        
    def _calc_entropy(self, listObject: list) -> float:
        entropy = 0.0
        dictValueClassifyCount = self._count_object_each_value_of_attribute(listObject, self.indexClassifyAttr)
        
        totalObject = len(listObject)
        for (value, count) in dictValueClassifyCount.items():
            prob = count/totalObject # K can rang buoc vi kiem tra listData tu luc bat dau
            entropy -= prob*(math.log2(prob))

        return entropy

    def _count_object_each_value_of_attribute(self, listObject: list, indexAttr: int) -> dict:
        dictValueCount = dict()
        for row in listObject:
            value = row[indexAttr]
            if value not in dictValueCount:
                dictValueCount[value] = 1
            else:
                dictValueCount[value] += 1
        return dictValueCount

    def _extract_object_by_value_of_attribute(self, listObject: list, posAttr: int) -> list:
        listObjectEachValue = list()
        listValue = list()
        for row in listObject:
            value = row[posAttr]
            if value not in listValue:
                listValue.append(value)
                listObjectEachValue.append([row])
            else:
                indexValue = listValue.index(value)
                listObjectEachValue[indexValue].append(row)
        return (listObjectEachValue, listValue)



    def _run(self):
        entropyS = self._calc_entropy(self.listObject)
        dictEntropyAttr = defaultdict(dict)
        for posAttr in range(1, len(self.listAttrName)-1):
            (listObjectEachValue, listValue) = self._extract_object_by_value_of_attribute(self.listObject, posAttr)
            dictEntropyOfValue = dict()
            for listObjectByValue in listObjectEachValue:
                value = listValue[listObjectEachValue.index(listObjectByValue)]
                dictEntropyOfValue[value] = self._calc_entropy(listObjectByValue)
            attrName = self.listAttrName[posAttr]
            dictEntropyAttr[attrName] = dictEntropyOfValue
        print(dictEntropyAttr)


        return 1
    


    

def _read_file(inputFolder: str, inputFileName: str) -> list:
    inputList = read_file.read_csv_to_list_of_row(inputFolder, inputFileName)
    return inputList


def main():
    listData = _read_file(folderInput, fileInput)
    indexClassifyAttribute = -1
    id3 = DTreeID3(listData, indexClassifyAttribute)
    id3._run()

if __name__ == "__main__": main()