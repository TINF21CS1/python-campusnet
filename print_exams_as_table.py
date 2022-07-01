import CampusNet
from tabulate import tabulate

username = input("Username (mit @!): ")
password = input("Password: ")

s = CampusNet.CampusNetSession(username, password)

table = list()

for module in s.modules:
    for exam in s.get_exams_for_module(module):
        table.append([module.num, module.name, exam.semester, exam.description, exam.grade])

print(tabulate(table))
