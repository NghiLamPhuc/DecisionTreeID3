from Working_with_file import read_file, write_file, make_folder
import math
from collections import defaultdict

folderInput = 'input'
fileInput = ['weather', 'Bai2', 'BuyComputer', 'BHK']
folderOutFile = 'outfile'
fileLog = 'log'
fileType = ['.txt']
splitType = [', ', ' ']

class TreeNode():
    def __init__(self, name: str, sizeListFlag: int):
        self.name = name
        self.isLeaf = False
        self.childs = dict() # dict of treenode (k:value of Attribute, v:TreeNode)
        self.listObject = None
        self.listAttrFlag = list()
        for i in range(sizeListFlag):
            self.listAttrFlag.append(0)
        self.listAttrFlag[0] = -1
        self.listAttrFlag[-1] = -1
        self.entropy = 0.0
        self.infoGain = 0.0
    
    def _display_childs(self):
        for (value, child) in self.childs.items():
            print('-{0}-> {1}'.format(value, child.name))
        
class DTreeID3():
    def __init__(self, listInput: list, posClassAttr: int):
        self.root = None
        self.listData = listInput
        self.listAttrName = self.listData[0]
        self.listObject = self.listData[1:]
        self.indexClassifyAttr = posClassAttr
        self.totalAttr = len(self.listAttrName)
        self.totalObject = len(self.listData) - 1
        self.countObjectClassified = 0

        self.listBranchStr = list()
        
    def _calc_entropy(self, listObject: list) -> float:
        entropy = 0.0
        dictValueClassifyCount = self._count_object_each_value_of_attribute(listObject, self.listAttrName[self.indexClassifyAttr])
        
        totalObject = len(listObject)
        for (value, count) in dictValueClassifyCount.items():
            if count == totalObject:
                return 0.0
            prob = count/totalObject # K can rang buoc vi kiem tra listData tu luc bat dau
            entropy -= prob*(math.log2(prob))

        return entropy

    def _count_object_each_value_of_attribute(self, listObject: list, nameAttr: str) -> dict:
        dictValueCount = dict()
        indexAttr = self.listAttrName.index(nameAttr)
        for row in listObject:
            value = row[indexAttr]
            if value not in dictValueCount:
                dictValueCount[value] = 1
            else:
                dictValueCount[value] += 1
        return dictValueCount

    def _extract_object_by_value_of_attribute(self, listObject: list, nameAttr: str) -> list:
        listObjectEachValue = list()
        listValue = list()
        indexAttr = self.listAttrName.index(nameAttr)
        for row in listObject:
            value = row[indexAttr]
            if value not in listValue:
                listValue.append(value)
                listObjectEachValue.append([row])
            else:
                indexValue = listValue.index(value)
                listObjectEachValue[indexValue].append(row)
        return (listObjectEachValue, listValue)

    def _calc_entropy_attribute(self, listObject: list, nameAttr: str):
        dictEntropyOfValue = dict()
        entropyAttr = 0.0
        (listObjectEachValue, listValue) = self._extract_object_by_value_of_attribute(listObject, nameAttr)
        for listObjectByValue in listObjectEachValue:
            indexVal = listObjectEachValue.index(listObjectByValue)
            value = listValue[indexVal]
            entropyVal = self._calc_entropy(listObjectByValue)
            dictEntropyOfValue[value] = entropyVal
            
            probAppearance = len(listObjectByValue)/self.totalObject
            entropyAttr += probAppearance*entropyVal
        print('Entropy({0}) : {1}'.format(nameAttr, entropyAttr))
        print(dictEntropyOfValue)
        return (entropyAttr, dictEntropyOfValue)

    def _set_root(self):
        entropyS = self._calc_entropy(self.listObject)
        print('Entropy(S): {0}'.format(entropyS))
        dictInfoGainAttr = dict()
        listAttrName = self.listAttrName[1:self.totalAttr-1]
        for nameAttr in listAttrName:
            (entropyAttr, dictEntropyOfValue) = self._calc_entropy_attribute(self.listObject, nameAttr)
            infoGain = entropyS - entropyAttr
            dictInfoGainAttr[nameAttr] = infoGain
            print('Information Gain({0}): {1}\n'.format(nameAttr, infoGain))
        (attr, ig) = _get_max_of_dict(dictInfoGainAttr)
        print('============    MAX(ig): {0}: {1}    ============\n'.format(attr, ig))

        self.root = TreeNode(attr, self.totalAttr)
        self.root.isLeaf = False
        self.root.entropy = entropyS
        self.root.infoGain = ig
        self.root.listObject = self.listObject
        self.root.listAttrFlag[self.listAttrName.index(attr)] = 1

    def _find_separate_node(self, listObject: list, prevNode: TreeNode):
        namePrevAttr = prevNode.name
        valueOfAttr = listObject[0][self.listAttrName.index(namePrevAttr)]

        entropyS = self._calc_entropy(listObject)
        print('Entropy({0}={1}): {2}'.format(namePrevAttr, valueOfAttr, entropyS))

        if entropyS == 0:
            classifyValueName = listObject[0][-1]
            child = TreeNode(classifyValueName, self.totalAttr)
            child.listAttrFlag = prevNode.listAttrFlag.copy()
            child.listAttrFlag[self.listAttrName.index(namePrevAttr)] = 1
            child.listObject = listObject
            child.isLeaf = True
            
            prevNode.childs[valueOfAttr] = child
            
            self.countObjectClassified += len(listObject)
            print('============    Leaf: {0}    ============\n'.format(child.name))

        else:
            dictInfoGainAttr = dict()
            dictEntropyAttr = dict()
            listAttrFlag = prevNode.listAttrFlag
            for nameAttr in self.listAttrName:
                if listAttrFlag[self.listAttrName.index(nameAttr)] == 0:
                    (entropyAttr, dictEntropyOfValue) = self._calc_entropy_attribute(listObject, nameAttr)
                    infoGain = entropyS - entropyAttr
                    dictEntropyAttr[nameAttr] = entropyAttr
                    dictInfoGainAttr[nameAttr] = infoGain
                    print('Information Gain({0}): {1}\n'.format(nameAttr, infoGain))
            (attr, ig) = _get_max_of_dict(dictInfoGainAttr)
            print('============    MAX(ig): {0}: {1}    ============\n'.format(attr, ig))

            child = TreeNode(attr, self.totalAttr)
            child.listAttrFlag = prevNode.listAttrFlag.copy()
            child.listAttrFlag[self.listAttrName.index(namePrevAttr)] = 1
            child.listObject = listObject
            child.entropy = dictEntropyAttr[attr]
            child.infoGain = ig
            
            prevNode.childs[valueOfAttr] = child
        
        return child
        
    def _find_list_separate_node(self, curNode: TreeNode):
        nameCurAttr = curNode.name
        listSepNode = list()
        (listObjectEachValue, listValue) = self._extract_object_by_value_of_attribute(curNode.listObject, nameCurAttr)
        for listObjectByValue in listObjectEachValue:
            sepNode = self._find_separate_node(listObjectByValue, curNode)
            if sepNode.isLeaf == False:
                listSepNode.append(sepNode)
        return listSepNode

    def _run(self):
        self._set_root()
        queueSepNode = self._find_list_separate_node(self.root)
        while queueSepNode:
            sepNode = queueSepNode.pop(0)
            queueSepNode.extend(self._find_list_separate_node(sepNode))

    def _display_tree(self):
        self._set_root_branch()
        for (value, rootChild) in self.root.childs.items():
            curStr = self.listBranchStr.pop(0)
            if rootChild.isLeaf:
                self.listBranchStr.append(curStr)
                continue
            listCopyCurStr = list()
            for i in range(len(rootChild.childs)):
                listCopyCurStr.append(curStr)
            self._display_separate_node(rootChild, listCopyCurStr)

    def _set_root_branch(self):
        for (value, child) in self.root.childs.items():
            if child.isLeaf:
                branchStr = '{0}: {1}: {2}.'.format(self.root.name, value, child.name)
            else:
                branchStr = '{0}: {1}: {2}: '.format(self.root.name, value, child.name)
            self.listBranchStr.append(branchStr)

    def _display_separate_node(self, node: TreeNode, listCurStr: list):
        i = 0
        for (value, childNode) in node.childs.items():
            listCurStr[i] += '{0}: {1}.'.format(value, childNode.name)
            i += 1
        self.listBranchStr.extend(listCurStr)
        
    def _predict(self):
        pass

def _get_max_of_dict(d: dict):
    max = 0
    key = -1
    for (k,v) in d.items():
        if v > max:
            max = v
            key = k
    return (key, max)

def _get_min_of_dict(d: dict):
    min = 0
    key = -1
    for (k,v) in d.items():
        if v < min:
            min = v
            key = k
    return (key, min)
    

def _read_file(inputFolder: str, inputFileName: str) -> list:
    inputList = read_file.read_csv_to_list_of_row(inputFolder, inputFileName)
    return inputList

def main():
    listData = _read_file(folderInput, fileInput[0])
    indexClassifyAttribute = -1
    id3 = DTreeID3(listData, indexClassifyAttribute)
    id3._run()
    id3._display_tree()
    print(*id3.listBranchStr, sep='\n')
    

if __name__ == "__main__": main()
