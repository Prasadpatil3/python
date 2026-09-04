class Father:
    def father_method(self):
        print("This is Father class")


class Mother:
    def mother_method(self):
        print("This is Mother class")


class Child(Father, Mother):
    def child_method(self):
        print("This is Child class")



c = Child()

c.father_method()
c.mother_method()
c.child_method()
