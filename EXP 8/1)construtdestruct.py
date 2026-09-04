class Student:

    def __init__(self, name):
        self.name = name
        print("Constructor called")
        print("Student name:", self.name)

    
    def __del__(self):
        print("Destructor called")



s1 = Student("Sandesh")


del s1
