
import re
import os
from pathlib import Path
import math
import random
from datetime import datetime

class Collection:
    def __init__(self, name, location, creator):
        self.name = name
        self.location = location
        self.path = os.path.join(self.location, self.name)
        if not Path(self.path).is_dir():
            os.mkdir(self.path)
        self.creator = creator
        self.date_of_creation = datetime.today().strftime('%Y-%m-%d')
        self.date_of_last_mod = datetime.today().strftime('%Y-%m-%d')
        self.type = None
        self.ctr = 0
        self.size = 0
        self.list = []
        self.locked = False

    def lock(self):
        self.locked = True

    def __str__(self):
        return self.name + " " + self.creator + " " + self.date_of_creation + " " + \
               self.date_of_last_mod + " " + str(self.type) + " " + str(self.ctr) + " " + str(self.size)

    def overview(self):
        print(self)
        for elem in self.list:
            print("    ",end=" ")
            print(elem)
        print()

    def insert(self, elem):
        if self.locked == True:
            print("Collection is locked.")
            return
        if self.ctr == 0:
            self.type = elem.type
        elif elem.is_in_collection:
            print("File already belongs to a collection.")
            return
        elif elem.type != self.type:
            print("Types do not match.")
            return
        """
        flag = False
        counter = 1
        while(flag == False):
            flag = True
            for elem in self.list:
                if elem.name == elem.name:
                    pos = elem.name.rfind(".")
                    elem.name = elem.name[:pos] + "(" + str(counter) + ")" + ".txt"
                    flag = False
                    counter += 1
        """
        if not Path(self.path + "\\" + elem.name).is_file():
            os.rename(elem.path, self.path + "\\" + elem.name)
        elem.location = self.path
        elem.path = self.path + "\\" + elem.name
        self.list.append(elem)
        self.ctr += 1
        self.size = self.size + elem.size
        self.date_of_last_mod = datetime.today().strftime('%Y-%m-%d')
        elem.is_in_collection = True

    def update(self, father):
        self.location = father.path
        self.path = father.path + "\\" + self.name
        for i in range(len(self.list)):
            self.list[i].update(self)

    def remove(self, elem):
        if self.locked == True:
            print("Collection is locked.")
            return
        path = Path(self.path + "\\" + elem.name)
        if path.is_file():
            os.remove(path)
        for i in range(len(self.list)):
            if self.list[i].name == elem.name:
                self.size -= self.list[i].size
                self.ctr -= 1
                self.list.remove(self.list[i])
                self.date_of_last_mod = datetime.today().strftime('%Y-%m-%d')
                if self.ctr == 0:
                    self.type = None
                return
        print("Document does not exist.")
        return

    def union(self, col, creator=None):
        if self.type != col.type:
            print("Collections are of different type.")
            return
        if self.locked or col.locked:
            print("One of the collections is locked.")
            return
        union = Collection(self.name + " U " + col.name, self.location, creator)
        for file in col.list:
            file.is_in_collection = False
            union.insert(file)
            col.remove(file)
        for file in self.list:
            file.is_in_collection = False
            union.insert(file)
            self.remove(file)
        os.rmdir(col.path)
        os.rmdir(self.path)
        return union

    def divide_by_list(self, list):
        colf = Collection("firstHalf" + self.name, self.location, "Damir")
        cols = Collection("secondHalf" + self.name, self.location, "Damir")
        temp_list = self.list[:]
        for file in temp_list:
            if file.name in list:
                file.is_in_collection = False
                colf.insert(file)
                self.remove(file)
            else:
                file.is_in_collection = False
                cols.insert(file)
                self.remove(file)
        os.rmdir(self.path)
        return colf, cols

    def divide_by_size(self, size):
        size = int(size)
        num_of_col = math.ceil(len(self.list) / size)
        list_of_col = []
        list_for_rand = []
        for i in range(len(self.list)):
            list_for_rand.append(i)
        for i in range(num_of_col):
            list_of_col.append(Collection(self.name + " " + str(i), self.location, "Damir"))
        for col in list_of_col:
            for i in range(size):
                k = random.choice(list_for_rand)
                self.list[k].is_in_collection = False
                col.insert(self.list[k])
                self.remove(self.list[k])
                list_for_rand.pop()

        os.rmdir(self.path)
        return list_of_col

    def divide_by_regex(self, regex):
        colf = Collection("firstHalf" + self.name, self.location, "Damir")
        cols = Collection("secondHalf" + self.name, self.location, "Damir")
        temp_list = self.list[:]
        for file in temp_list:
            print("ima elemenata")
            if bool(re.match(regex, file.name)):
                file.is_in_collection = False
                colf.insert(file)
                self.remove(file)
            else:
                file.is_in_collection = False
                cols.insert(file)
                self.remove(file)
        #os.rmdir(self.path)
        return colf, cols

    def extract_sample(self):
        sample = Collection("sample" + self.name, self.location, "Damir")
        temp_list = self.list[:]
        for file in temp_list:
            print(file.size)
            if math.ceil(file.size) % 2 == 0:
                file.is_in_collection = False
                sample.insert(file)
                self.remove(file)
        return sample

    def export(self):
        pass
