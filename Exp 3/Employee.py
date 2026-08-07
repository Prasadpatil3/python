project_A = set(input("Enter employees for Project A (space-separated): ").split())
                
project_B = set(input("Enter employees for Project B (space-separated): ").split())

both_projects = project_A.intersection(project_B)

only_project_A = project_A.difference(project_B)

only_project_B = project_B.difference(project_A)

all_employees = project_A.union(project_B)

print("\nEmployees working on both projects:")
print(both_projects)

print("\nEmployees working only on Project A:")
print(project_A)

print("\nEmployees working only on Project B:")
print(project_B)

print("\nTotal unique employees across both projects:")
print(all_employees)
