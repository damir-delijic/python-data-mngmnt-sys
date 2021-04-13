
import os
from pathlib import Path
from Collection import Collection
import re
import math

class CompositeCollection(Collection):
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.path = os.path.join(self.location, self.name)
        temp_path = Path(self.path)
        if not temp_path.is_dir():
            os.mkdir(self.path)
        self.ctr = 0
        self.size = 0
        self.list = []
        self.locked = False

    def lock(self):
        for col in self.list:
            col.lock()
            self.locked = True

    def __str__(self):
        return self.name + " " + str(self.ctr) + " " + str(self.size)

    def overview(self):
        print(self)
        for dir in self.list:
            print("    ", end=" ")
            print(dir)
        print()

    def insert(self, elem):
        if self.locked == True:
            print("Slozena kolekcija je zakljucana.")
            return
        temp_path = Path(self.path + "\\" + elem.name)
        if not temp_path.is_dir():
            os.rename(elem.path, self.path + "\\" + elem.name)
        elem.location = self.path
        elem.path = self.path + "\\" + elem.name
        for i in range(len(elem.list)):
            elem.list[i].update(elem)
        self.ctr += 1
        self.size += elem.size
        self.list.append(elem)


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
            os.rmdir(path)
        for i in range(len(self.list)):
            if self.list[i].name == elem.name:
                self.size -= self.list[i].size
                self.ctr -= 1
                self.list.remove(self.list[i])
                return
        print("Collection does not exist.")
        return

    def union(self, comp_col, creator=None):
        if self.locked or comp_col.locked:
            print("One of the collections is locked.")
            return

        union = CompositeCollection(self.name + " U " + comp_col.name, self.location)
        for col in comp_col.list:
            union.insert(col)
            comp_col.remove(col)
        for col in self.list:
            union.insert(col)
            self.remove(col)
        os.rmdir(col.path)
        os.rmdir(self.path)
        return union

    def divide_by_list(self, list):
        colf = Collection("firstHalf" + self.name, self.location)
        cols = Collection("secondHalf" + self.name, self.location)
        temp_list = self.list[:]
        for col in temp_list:
            if col.name in list:
                colf.insert(col)
                self.remove(col)
            else:
                cols.insert(col)
                self.remove(col)
        os.rmdir(self.path)
        return colf, cols

    def divide_by_regex(self, regex):
        colf = Collection("firstHalf" + self.name, self.location)
        cols = Collection("secondHalf" + self.name, self.location)
        temp_list = self.list[:]
        for col in temp_list:
            if bool(re.match(regex, col.name)):
                colf.insert(col)
                self.remove(col)
            else:
                cols.insert(col)
                self.remove(col)
        os.rmdir(self.path)
        return colf, cols

    def extract_sample(self):
        sample = Collection("sample" + self.name, self.location)
        temp_list = self.list[:]
        for col in temp_list:
            if math.ceil(col.size) % 2 == 0:
                sample.insert(col)
                self.remove(col)
        return sample

    def export(self):
        pass
