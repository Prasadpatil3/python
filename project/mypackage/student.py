def get_student():
    name = input("Enter student name: ")
    roll = input("Enter roll number: ")
    return name, roll

def display_student(name, roll):
    print("Name:", name)
    print("Roll No:", roll)
