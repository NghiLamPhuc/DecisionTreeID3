#'lamphucnghi@gmail.com'
from collections import defaultdict
# import file_dir_init
import csv

TYPE_OF_RESULT_LIST_IS_TEXT = 0
TYPE_OF_RESULT_LIST_IS_INT = 1
TYPE_OF_RESULT_LIST_IS_FLOAT = 2
TYPE_OF_RESULT_LIST_IS_SENTENCE = 3

TYPE_OF_CONVERT_STR = 10
TYPE_OF_CONVERT_INT = 11
TYPE_OF_CONVERT_FLOAT = 12

HAS_KEY = True
HAS_NO_KEY = False

def read_line_as_dict(folderName: str, fileName: str, fileType: str, splitType: str, hasKey: bool, keyType: int, valueType: int) -> dict:
    '''
    reading a file with dict type:
    key1 : value1, value2, value3, ...
    key2 : value1, value2, ....
    '''
    try:
        f = open('./{}/{}{}'.format(folderName, fileName, fileType), 'r', encoding = 'utf-8')
        inpDict = defaultdict(dict)
        splitKey = ' : ' if hasKey == True else splitType
        i = 0
        for line in f:
            if line != '\n':
                lineSplited = line.split('\n')[0].split(splitKey)
                curKey = ''
                curValues = ''
                curValuesSplited = None
                if hasKey == False:
                    curKey = str(i)
                    curValues = lineSplited
                    curValuesSplited = curValues
                else:
                    curKey = lineSplited[0]
                    curValues = lineSplited[1]
                    curValuesSplited = curValues.rstrip().split(splitType)

                if keyType == TYPE_OF_CONVERT_STR:
                    curKey = lineSplited[0]
                elif keyType == TYPE_OF_CONVERT_INT:
                    curKey = int(lineSplited[0])
                elif keyType == TYPE_OF_CONVERT_FLOAT:
                    curKey = float(lineSplited[0])

                if valueType == TYPE_OF_CONVERT_STR:
                    curValues = lineSplited[1]
                    inpDict[curKey] = sorted(curValuesSplited)
                elif valueType == TYPE_OF_CONVERT_INT:
                    curValuesChanged = [int(value) for value in curValuesSplited]
                    inpDict[curKey] = sorted(curValuesChanged)
                elif valueType == TYPE_OF_CONVERT_FLOAT:
                    curValuesChanged = [float(value) for value in curValuesSplited]
                    inpDict[curKey] = sorted(curValuesChanged)
                i += 1
        f.close()
        return inpDict
    except:
        print('No such file or dir!!')

def read_lineSplited_to_list(folderName: str, fileName: str, fileType: str, splitType: str, outListType: int) -> list:
    '''
    Reading a file like:
    [*0.1 0.2 0.3....
    0.4 0.5 0.6]*
    each row stored in a [l]ist of [L]ist
    '''
    try:
        f = open('./{}/{}{}'.format(folderName, fileName, fileType), 'r', encoding = 'utf-8')
        List = list()
        for line in f:
            if line != '\n':
                if outListType == TYPE_OF_RESULT_LIST_IS_SENTENCE:
                    List.append(line.rstrip())
                else:
                    lineToStrList = line.rstrip().split(splitType)
                    if lineToStrList[0][0] == '[':
                        lineToStrList[0] = lineToStrList[0][1:]
                        lineToStrList[-1] = lineToStrList[-1][:-1]
                    if outListType == TYPE_OF_RESULT_LIST_IS_TEXT:
                        List.append(lineToStrList)
                    elif outListType == TYPE_OF_RESULT_LIST_IS_INT:
                        List.append([int(x) for x in lineToStrList])
                    elif outListType == TYPE_OF_RESULT_LIST_IS_FLOAT:
                        List.append([float(x) for x in lineToStrList])
                
        f.close()
        if len(List) == 1:
            return sum(List, [])
        return List
    except:
        print('No such file or dir!!')

def convert_twoHierachyList_to_oneList(inpList: list(list())) -> list:
    '''
    We have a [L]ist with each item is a [l]ist.
    We want to merge all item of all [l]ist to [L]ist.
    [[0, 1, 2], [1, 2, 3]] --> [0, 1, 2, 1, 2, 3]
    '''
    return list(sum(inpList, []))

def read_csv_to_list_of_row(fileDir: str, fileName: str) -> list(list()):
    '''
    Reading a CSV file. A line in CSV is an object. Storing CSV in a list, where an item of list is a row of CSV.
    '''
    rowList = list()
    with open("./" + fileDir + "/" + fileName + '.csv', 'r') as inpCSVFile:
        reader = csv.reader(inpCSVFile)
        for row in reader:
            rowList.append(row)
    return rowList

def test():
    folderName = 'test_write'
    fileName = ['a1', 'an', 'b', 'c', 'd', 'e']
    fileType = '.txt'
    a1 = read_lineSplited_to_list(folderName, fileName[0], fileType, ', ', 1)
    print(a1)
    an = read_lineSplited_to_list(folderName, fileName[1], fileType, ', ', 1)
    print(an)
    b1 = read_line_as_dict(folderName, fileName[1], fileType, ', ', HAS_NO_KEY, TYPE_OF_CONVERT_STR, TYPE_OF_CONVERT_FLOAT)
    print(b1)
    bn = read_line_as_dict(folderName, fileName[2], fileType, ', ', HAS_NO_KEY, TYPE_OF_CONVERT_STR, TYPE_OF_CONVERT_FLOAT)
    print(bn)
    c = read_line_as_dict(folderName, fileName[3], fileType, ', ', HAS_KEY, TYPE_OF_CONVERT_STR, TYPE_OF_CONVERT_FLOAT)
    print(c)
    d = read_line_as_dict(folderName, fileName[4], fileType, ', ', HAS_KEY, TYPE_OF_CONVERT_STR, TYPE_OF_CONVERT_FLOAT)
    print(d)
    e = read_line_as_dict(folderName, fileName[4], fileType, ', ', HAS_KEY, TYPE_OF_CONVERT_STR, TYPE_OF_CONVERT_STR)
    print(e)


def main():
    print('readfile')
    # print(read_csv_to_list_of_row(file_dir_init.input_dir, 'weather')[1])
    

if __name__ == "__main__": main()