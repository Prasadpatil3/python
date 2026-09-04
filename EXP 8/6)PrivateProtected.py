class Grandfather:
    def __init__(self):
        self.__money = 50000       # Private
        self._house = "Big House"  # Protected

    def show(self):
        print("Private Money:", self.__money)


class Father(Grandfather):
    def display_father(self):
        print("Protected House:", self._house)


class Son(Father):
    def display_son(self):
        print("Son can access House:", self._house)


s = Son()

s.show()
s.display_father()
s.display_son()
