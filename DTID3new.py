from Working_with_file import read_file, write_file
import math

inputFolder = 'input'
inputFileName = 'weather'
outFileFolder = 'outfile'
fileLogName = 'log'
fileType = ['.txt']
splitType = [', ', ' ']

def count_each_value_of_attribute(objectList: list(list()), attributePos: int) -> dict:
    attrNameDict = dict()
    for objectIndex in range(0, len(objectList)):
        if objectList[objectIndex][attributePos] not in attrNameDict:
            attrNameDict[objectList[objectIndex][attributePos]] = 1
        else:
            attrNameDict[objectList[objectIndex][attributePos]] += 1
    #co nen dem thu xem cac attrName bang nhau ve so luong, giam tai viec tinh entropy (vi se = 1).
    return attrNameDict


'''
De tinh entropy, input la bang cac doi tuong va vi tri thuoc tinh phan lop,
tra ve gia tri float
'''
def entropy(objectList: list(list()), classifyPos: int) -> float:
    if len(objectList) <= 1:
        return -1.0
    entropy = 0.0
    classifyNameDict = count_each_value_of_attribute(objectList, classifyPos)
    objectCount = len(objectList)
    if len(classifyNameDict) <= 1:
        return 0
    for (classifyName, classifyCount) in classifyNameDict.items():
        entropy -= (classifyCount/objectCount)*math.log2(classifyCount/objectCount)
    return entropy


'''
Entropy of attribute A after deciding on a particular attribute B.
- Lay danh sach cac gia tri cua thuoc tinh.
- Rut trich cac bang con theo cac gia tri do.
- Tinh entropy cho tung gia tri cua thuoc tinh.
- Tinh Entropy toan bo gia tri cua thuoc tinh.
'''
def entropy_by_attribute(objectList: list(list()), attrPos: int, classifyPos: int) -> float:
    entropyList = list()
    avgEntropy = 0.0
    valueCountOfAttrDict = count_each_value_of_attribute(objectList, attrPos)
    
    objectListByEachValueOfAttr = extract_objectList_by_value_of_attribute(objectList, attrPos)
    
    for objectListAtValue in objectListByEachValueOfAttr:
        entropyList.append(entropy(objectListAtValue, classifyPos))
    
    entropyAtEachValue = dict()
    for index in range(len(entropyList)):
        entropyAtEachValue[list(valueCountOfAttrDict.keys())[index]] = entropyList[index]

    entropyIndex = 0
    for (valueName, count) in valueCountOfAttrDict.items():
        avgEntropy += (count/len(objectList))*entropyList[entropyIndex]
        entropyIndex += 1

    return avgEntropy, entropyAtEachValue#list(valueCountOfAttrDict.keys())


'''
Information Gain.
'''
def information_gain(entropyOverall: float, entropyAttr: float) -> float:
    return (entropyOverall - entropyAttr)


'''
Rut trich tu bang ban dau, theo gia tri cua thuoc tinh.
'''
def extract_objectList_by_value_of_attribute(objectList: list(list()), attributePos: int):
    attrNameDict = count_each_value_of_attribute(objectList, attributePos)
    objectListByEachValueOfAttr = list(list(list()))
    for (attrName, count) in attrNameDict.items():
        valueOfAttrList = list()
        for objIndex in range(0, len(objectList)):
            if objectList[objIndex][attributePos] == attrName:
                valueOfAttrList.append(objectList[objIndex])
        objectListByEachValueOfAttr.append(valueOfAttrList)
    
    return objectListByEachValueOfAttr

def run(inputList: list, attrVisitedList: list):
    classifyPos = -1
    # inputList = read_file.read_csv_to_list_of_row(inputFolder, inputFileName)
    objectList = inputList[1:]
    attrNameList = inputList[0]
    entropyOverall = entropy(objectList, classifyPos)
    
    write_file.list_to_txt_continuos(['Entropy(S):', str(entropyOverall)], outFileFolder, fileLogName, fileType[0], splitType[1])
    
    IGList = list()
    attrCount = len(objectList[0]) - 2 # Tru cot stt va cot phan lop.
    for attrIndex in range(1, attrCount + 1):
        if attrIndex not in attrVisitedList:
            entropyByAttr = entropy_by_attribute(objectList, attrIndex, -1)
            entropybyValueList = entropyByAttr[1]
            entropyAttr = entropyByAttr[0]
            iGAttr = information_gain(entropyOverall, entropyAttr)
            IGList.append(iGAttr)
            write_file.list_to_txt_continuos(['IG({0}):{1}. Entropy({0}):{2}'.format(attrNameList[attrIndex], iGAttr, entropyAttr), entropybyValueList], outFileFolder, fileLogName, fileType[0], splitType[1])

    write_file.list_to_txt_continuos(['Max IG({0}):'.format(attrNameList[IGList.index(max(IGList)) + 1]), max(IGList)], outFileFolder, fileLogName, fileType[0], splitType[1])
    
    return (attrNameList[IGList.index(max(IGList)) + 1], max(IGList))
        


def main():
    attrVisitedList = [0]
    attrPos = 1
    inputList = read_file.read_csv_to_list_of_row(inputFolder, inputFileName)
    # print(run(inputList))
    inputList2 = extract_objectList_by_value_of_attribute(inputList, attrPos)
    attrNameList = inputList2[0]
    print(run(attrNameList + inputList2[1], attrVisitedList))

    
if __name__ == "__main__": main()