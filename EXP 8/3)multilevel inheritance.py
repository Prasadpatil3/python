class Grandfather:
    def grandfather(self):
        print("I am Grandfather")


class Father(Grandfather):
    def father(self):
        print("I am Father")


class Son(Father):
    def son(self):
        print("I am Son")


# Create object of Son
s = Son()

s.grandfather()
s.father()
s.son()
