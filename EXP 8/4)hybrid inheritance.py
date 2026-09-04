class Student:
    def student_details(self):
        print("Name: prasad")
        print("Roll No: 66")


class Marks(Student):
    def marks(self):
        print("Marks: 85")


class Sports(Student):
    def sports(self):
        print("Sports: Cricket")


class Result(Marks, Sports):
    def result(self):
        print("Result: Pass")


# Create object
r = Result()

r.student_details()
r.marks()
r.sports()
r.result()
