

class testobj:
    def __init__(self, name):
        self.name = name

    def getName(self):
        print(self.name)

list = ["lind", "pind", "find"]
for i in list:
    obj = testobj(i)
    

obj.getName()