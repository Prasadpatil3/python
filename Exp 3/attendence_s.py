attendance = {}

days = ["Mon", "Tue", "Wed", "Thu", "Fri"]

for day in days:
    attendance[day] = set(input(f"Enter students for {day} : ").split())

all_days = list(attendance.values())

print("Attended all classes:", set.intersection(*all_days))

all_students = set.union(*all_days)

one_class = {s for s in all_students if sum(s in d for d in all_days) == 1}
print("Attended only one class:", one_class)

print("Total unique students:", len(all_students))
