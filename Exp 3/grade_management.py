students = []
grades = []


def add_student(name, grade):
 students.append(name)
 grades.append(grade)
 print(f"{name} added successfully.")


def update_grade(name, new_grade):
 if name in students:
    index = students.index(name)
    grades[index] = new_grade
    print(f"{name}'s grade updated to {new_grade}.")
 else:
        print("Student not found.")


def remove_student(name):
 if name in students:
    index = students.index(name)
    students.pop(index)
    grades.pop(index)
    print(f"{name} removed successfully.")
 else:
        print("Student not found.")

def calculate_average():
 if len(grades) == 0:
    print("No grades available.")
 else:
    average = sum(grades) / len(grades)
    print(f"Average Grade: {average:.2f}")


def display_extremes():
    if len(grades) == 0:
        print("No grades available.")
    else:
        highest = max(grades)
        lowest = min(grades)

        highest_student = students[grades.index(highest)]
        lowest_student = students[grades.index(lowest)]

        print(f"Highest Grade: {highest} ({highest_student})")
        print(f"Lowest Grade: {lowest} ({lowest_student})")


def display_students():
    if len(students) == 0:
        print("No students in the list.")
    else:
        print("\nStudent List:")
        for i in range(len(students)):
            print(f"{students[i]} : {grades[i]}")


while True:
    print("\n--- Student Grade Management System ---")
    print("1. Add Student")
    print("2. Update Grade")
    print("3. Remove Student")
    print("4. Display Students")
    print("5. Calculate Average Grade")
    print("6. Display Highest and Lowest Grades")
    print("7. Exit")

    choice = input("Enter your choice (1-7): ")

    if choice == "1":
        name = input("Enter student name: ")
        grade = float(input("Enter student grade: "))
        add_student(name, grade)

    elif choice == "2":
        name = input("Enter student name to update: ")
        new_grade = float(input("Enter new grade: "))
        update_grade(name, new_grade)

    elif choice == "3":
        name = input("Enter student name to remove: ")
        remove_student(name)

    elif choice == "4":
        display_students()

    elif choice == "5":
        calculate_average()

    elif choice == "6":
        display_extremes()

    elif choice == "7":
        print("Exiting program...")
        break

    else:
        print("Invalid choice. Please try again.")
