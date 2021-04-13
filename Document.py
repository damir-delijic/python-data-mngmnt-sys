
import os

class Document:
    def __init__(self, name, type, location):
        self.name = name
        self.type = type
        self.location = location
        self.path = os.path.join(self.location, self.name)
        self.size = os.stat(self.path).st_size/1024
        self.is_in_collection = False

    def __str__(self):
        return "Path: " + self.path + " In a collection: " + str(self.is_in_collection) + " Size: " + str(self.size)

    def update(self, father):
        self.location = father.path
        self.path = father.path + "\\" + self.name