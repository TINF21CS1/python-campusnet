import campusnet
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="python -m campusnet", description="Get exams from CampusNet instance."
    )
    parser.add_argument("username", help="Username (including domain)")
    parser.add_argument(
        "password",
        help="Password (will be read from stdin if not supplied)",
        nargs="?",
        default=None,
    )
    parser.add_argument(
        "-b",
        "--base-url",
        help="Base URL of the CampusNet instance (default: https://dualis.dhbw.de/)",
        default="https://dualis.dhbw.de/",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output format of the data (default: table)",
        default="table",
        choices=["table", "json", "csv"],
    )

    args = parser.parse_args()
    if not args.password:
        from getpass import getpass

        password = getpass()
    else:
        password = args.password

    while True:
        try:
            s = campusnet.CampusNetSession(args.username, password, args.base_url)
            break
        except campusnet.LoginError as e:
            print("Invalid username or password.")
            if not args["password"]:
                password = getpass()
            else:
                exit(1)

    if args.output == "table":
        from tabulate import tabulate

        table = []
        for module in s.modules:
            for exam in s.get_exams_for_module(module):
                table.append(
                    [
                        module.num,
                        module.name,
                        exam.name,
                        exam.semester,
                        exam.description,
                        exam.grade,
                    ]
                )

        print(
            tabulate(
                table,
                headers=["Module", "Name", "Exam", "Semester", "Description", "Grade"],
            )
        )
    elif args.output == "json":
        import json

        out = []
        for module in s.modules:
            for exam in s.get_exams_for_module(module):
                out.append(
                    {
                        "module": module.num,
                        "name": module.name,
                        "exam": exam.name,
                        "semester": exam.semester,
                        "description": exam.description,
                        "grade": exam.grade,
                    }
                )
        print(json.dumps(out, indent=4))
    elif args.output == "csv":
        import csv
        import sys

        out = [["Module", "Name", "Exam", "Semester", "Description", "Grade"]]
        for module in s.modules:
            for exam in s.get_exams_for_module(module):
                out.append(
                    [
                        module.num,
                        module.name,
                        exam.name,
                        exam.semester,
                        exam.description,
                        exam.grade,
                    ]
                )
        writer = csv.writer(sys.stdout)
        writer.writerows(out)
