'lamphucnghi@gmail.com'
# from FUNC_working_with_file import make_folder
import make_folder

INDEX_ROW_NO = 0
INDEX_ROW_YES = 1

'''
writing a list to txt.
'''
def list_to_txt(List: list, folderName: str, fileName: str, fileType: str, splitType: str) -> int:
    make_folder.create_folder(folderName)
    if not List:
        print('Empty list! ' + fileName)
        return 0
    
    with open('./{0}/{1}{2}'.format(folderName, fileName, fileType), 'w', encoding = 'utf-8') as fout:
        for curr in range(len(List) - 1):
            fout.write('{0}{1}'.format(List[curr], splitType))
        fout.write('{0}'.format(List[-1]))
    return 1

'''
Writing a [L]ist of [l]ist to file, with split type,
if [l]ist only has one value:
    each [l]ist is seperated by split type.
    [[1], [2], [3], [4]]
    1,2,3,4
if [l]ist has n values:
    each [l]ist is seperated by '\n'.
    each item in [l]ist is seperated by split type.
    [[0,1,2], [1,2,3]]
    0,1,2
    1,2,3
'''
def list_2hierachy_to_txt(List: list, folderName: str, fileName: str, fileType: str, splitType: str) -> int:
    make_folder.create_folder(folderName)
    if not List:
        print('Empty list! ' + fileName)
        return 0
    
    with open('./{0}/{1}{2}'.format(folderName, fileName, fileType), 'w', encoding = 'utf-8') as fout:
        if len(List[0]) > 1:
            for subList in List:
                for curr in range(len(subList) - 1):
                    fout.write('{0}{1}'.format(subList[curr], splitType))
                fout.write('{0}\n'.format(subList[-1]))
        elif len(List[0]) == 1:
            for curr in range(len(List) - 1):
                for item in List[curr]:
                    fout.write('{0}{1}'.format(item, splitType))
            fout.write('{0}'.format(str(List[-1])[1:-1]))
    return 1

'''
dict to txt.
Each key each row
Values is a list with splitType
'''        
def dict_valueList_to_txt(Dict: dict, folderName: str, fileName: str, fileType: str, splitType: str) -> int:
    make_folder.create_folder(folderName)
    if not Dict:
        print('Empty dict!' + fileName)
        return 0
    with open('./{0}/{1}{2}'.format(folderName, fileName, fileType), 'w', encoding = 'utf-8') as fout:
        for (key, values) in Dict.items():
            fout.write('{0} : '.format(key))
            for indexItem in range(len(values) - 1):
                fout.write('{0}{1}'.format(values[indexItem], splitType) )
            fout.write('{0}\n'.format(values[-1]) )
            fout.write('\n')
    return 1

'''
dict to txt
key : value
'''
def dict_to_txt(Dict: dict, folderName: str, fileName: str, fileType: str) -> int:
    make_folder.create_folder(folderName)
    if not Dict:
        print('Empty dict!' + fileName)
        return 0
    with open('./{0}/{1}{2}'.format(folderName, fileName, fileType), 'w', encoding = 'utf-8') as fout:
        for (key, value) in Dict.items():
            row = '{0} : {1}\n'.format(key, value)
            fout.write(row)
    return 1

'''
write list to one txt file. a+
'''
def list_to_txt_continuos(List: list, folderName: str, fileName: str, fileType: str, splitType: str) -> 0:
    make_folder.create_folder(folderName)
    if not List:
        print('Empty list! ' + fileName)
        return 0
    with open('./{0}/{1}{2}'.format(folderName, fileName, fileType), 'a+', encoding = 'utf-8') as fout:
        for index in range(len(List) - 1):
            fout.write(('{0}' + splitType).format(List[index]))
        fout.write('{0}'.format(List[-1]))
        fout.write('\n')
    return 1

def test():
    folderName = 'test_write'
    fileType = '.txt'
    a1 = [[0], [1], [2], [3], [4], [5]]
    list_2hierachy_to_txt(a1, folderName, 'a1', fileType, ', ')

    an = [[0,1,2], [2,3], [4,5,6]]
    list_2hierachy_to_txt(an, folderName, 'an', fileType, ', ')

    b = [0,1,2,3,4,5]
    list_to_txt(b, folderName, 'b', fileType, ', ')

    c = {'0':[0,1,2],'a':[1,2,3],'b':[8,9,1]}
    dict_valueList_to_txt(c, folderName, 'c', fileType, ', ')

    d = {'a':1,'b':2,'c':3}
    if dict_to_txt(d, folderName, 'd', fileType) == 1:
        print('dict wrote!')

    e = [1,2,3,4,5]
    for _ in range(10):
        list_to_txt_continuos(e, folderName, 'e', fileType, ', ')

def main():
    print('test')
    


if __name__ == "__main__": main()