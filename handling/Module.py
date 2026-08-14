import Filehandling

while True:
    print("\nfile handling module")
    print("1.Create and Write")
    print("2.Read")
    print("3.Append")
    print("4.Readline")
    print("5.Readlines")
    print("6.Tell")
    print("7.Seek")
    print("8.r+")
    print("9.w+")
    print("10.a+")
    print("11.Rename")
    print("12.Delete")
    print("13.Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
     Filehandling.create_file()

    elif choice == 2:
     Filehandling.read_file()

    elif choice == 3:
     Filehandling.append_file()

    elif choice == 4:
     Filehandling.read_line()

    elif choice == 5:
     Filehandling.read_lines()

    elif choice == 6:
     Filehandling.tell_position()

    elif choice == 7:
     Filehandling.seek_position()

    elif choice == 8:
     Filehandling.read_write()

    elif choice == 9:
     Filehandling.write_read()

    elif choice == 10:
     Filehandling.append_read()

    elif choice == 11:
     Filehandling.rename_file()

    elif choice == 12:
     Filehandling.delete_file()

    elif choice == 13:
     print("Program ended.")
     break

    else:
     print("Invalid choice!")
