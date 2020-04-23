from Working_with_file import read_file
import math


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
Average Entropy Information of attribute
- Lay danh sach cac gia tri cua thuoc tinh.
- Rut trich cac bang con theo cac gia tri do.
- Tinh entropy cho tung bang con.
- Tinh Entropy trung binh.
'''
def average_entropy_of_attribute(objectList: list(list()), attrPos: int, classifyPos: int) -> float:
    entropyList = list()
    avgEntropy = 0.0
    valueCountOfAttrDict = count_each_value_of_attribute(objectList, attrPos)
    
    objectListByEachValueOfAttr = extract_objectList_by_value_of_attribute(objectList, attrPos)
    
    for objectListAtValue in objectListByEachValueOfAttr:
        entropyList.append(entropy(objectListAtValue, classifyPos))
    
    entropyIndex = 0
    for (valueName, count) in valueCountOfAttrDict.items():
        avgEntropy += (count/len(objectList))*entropyList[entropyIndex]
        entropyIndex += 1

    return avgEntropy


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


def main():
    print('DTID3new')
    objectList = read_file.read_csv_to_list_of_row('./input/', 'weather')[1:]
    attrCount = len(objectList[0]) - 1
    # print(entropy(objectList, -1))
    # print(extract_objectList_by_value_of_attribute(objectList, 1)[1])
    average_entropy_of_attribute(objectList, 1, -1)

    
if __name__ == "__main__": main()