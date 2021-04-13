
from Document import Document
from Collection import Collection
from CompositeCollection import CompositeCollection
import pathlib
import shutil

def imp(folder_path):
    col = None
    pos = str(folder_path).rfind("\\")
    name = str(folder_path)
    location = name[:pos]
    name = name[pos + 1:]
    i = 1
    for path in pathlib.Path(folder_path).iterdir():
        print(path)
        if path.is_file():
            if i == 1 :
                col = Collection(name, location, "Unknown")
            pos = str(path).rfind("\\")
            name = str(path)
            name = name[pos + 1:]
            pos2 = name.find(".")
            tip = name[pos2+1:]
            tempdoc = Document(name,tip,folder_path)
            col.insert(tempdoc)
        if path.is_dir():
            if i == 1:
                col = CompositeCollection(name, location)
            col.insert(imp(path))
        i+=1
    return col

def export(col, dirPath):
    shutil.make_archive(dirPath + "\\" + col.name, 'zip', col.location + "\\" + col.name)

def test():
    col = imp("C:\\Users\\Damir Delijic\\Desktop\\composite")
    col.overview()
#test()
#kolekcija sa pet dokumenata, dvojica pocin ju sa a a ostala trojica sa b, izvuci sa a sa regexom.
dir = "C:\\Users\\Damir Delijic\\Desktop"
c1 = Collection("testKol",dir, "damir")
d1 = Document("ad1.txt", "txt", dir + "\\" + "testKol")
d2 = Document("ad2.txt", "txt", dir + "\\" + "testKol")
d3 = Document("bd3.txt", "txt", dir + "\\" + "testKol")
d4 = Document("bd4.txt", "txt", dir + "\\" + "testKol")
d5 = Document("bd5.txt", "txt", dir + "\\" + "testKol")
c1.insert(d1)
c1.insert(d2)
c1.insert(d3)
c1.insert(d4)
c1.insert(d5)
col1, col2 = c1.divide_by_regex(r'a')

