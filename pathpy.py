class Path():
    def __init__(self):
        self.tab = ["uploads"]
    def __str__(self):
        temp = ""
        for i in self.tab:
            temp += i+"/"
        return temp
    def show(self):
        temp = ""
        for i in self.tab:
            temp += i+"/"
        return temp

    def add(self, folder):
        self.tab.append(folder)

    def up(self):
        if len(self.tab) != 1:
            self.tab.pop()

    def reset(self):
        self.tab = ["uploads"]
