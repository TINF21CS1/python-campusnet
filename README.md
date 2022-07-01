# CampusNet Python

## Installation

```
pip install git+https://github.com/TINF21CS1/python-campusnet@dev
```

## Usage Examples

### Getting all exams and grades

The module can be used directly to get information about all exams

```
$ python -m campusnet -h
usage: python -m campusnet [-h] [-b BASE_URL] [-o {table,json,csv}] username [password]

Get exams from CampusNet instance.

positional arguments:
  username              Username (including domain)
  password              Password (will be read from stdin if not supplied)

optional arguments:
  -h, --help            show this help message and exit
  -b BASE_URL, --base-url BASE_URL
                        Base URL of the CampusNet instance (default: https://dualis.dhbw.de/)
  -o {table,json,csv}, --output {table,json,csv}
                        Output format of the data (default: table)
```

```
$ python -m campusnet s*******@student.dhbw-mannheim.de -b https://dualis.dhbw.de
Password: 
Module     Name                                      Exam                                                    Semester      Description                                     Grade
---------  ----------------------------------------  ------------------------------------------------------  ------------  --------------------------------------------  -------
T3_1000    Praxisprojekt I                           T3_1000.1 Projektarbeit 1 (MA-TINF21CS1)                SoSe 2022     Projektarbeit (1%)
T3_1000    Praxisprojekt I                           T3_1000.2 Wissenschaftliches Arbeiten 1 (MA-TINF21CS1)  SoSe 2022     Ablauf- und Reflexionsbericht (1%)
T3INF1001  Mathematik I                              T3INF1001.1 Lineare Algebra (MA-TINF21CS1)              WiSe 2021/22  Klausurarbeit (50%)                               *.*
T3INF1001  Mathematik I                              T3INF1001.2 Analysis (MA-TINF21CS1)                     SoSe 2022     Klausurarbeit (50%)                               *.*
T3INF1002  Theoretische Informatik I (MA-TINF21CS1)  Modulabschlussleistungen                                SoSe 2022     Klausurarbeit (100%)
T3INF1003  Theoretische Informatik II                Modulabschlussleistungen                                SoSe 2022     Klausurarbeit (100%)
T3INF1004  Programmieren                             Modulabschlussleistungen                                SoSe 2022     Programmentwurf (100%)
T3INF1005  Schlüsselqualifikationen                  Modulabschlussleistungen                                SoSe 2022     Klausurarbeit (< 50 %) (100%)
T3INF4102  Einführung in die Kryptologie             Modulabschlussleistungen                                SoSe 2022     Klausur 75 % und Laborarbeit 25 % (100%)
T3INF9000  Web and App Engineering                   Modulabschlussleistungen                                SoSe 2022     Klausur 50 % und Programmentwurf 50 % (100%)
T3INF1006  Technische Informatik I                   Modulabschlussleistungen                                WiSe 2021/22  Klausurarbeit (100%)                              *.*
T3INF9001  Cyber Security Basics                     Modulabschlussleistungen                                WiSe 2021/22  Hausarbeit (100%)                                 *.*
```---------------------------------------  ---
```

### Python Package

You can also use `campusnet` as a package to interact with CampusNet from Python.

```python
$ python
>>> from campusnet import CampusNetSession
>>> s = CampusNetSession("s***REMOVED***@student.dhbw-mannheim.de", "***REMOVED***")
>>> s.modules
[Module(num='T3_1000', name='Praxisprojekt I', credits=20.0, status='', semesters=['SoSe 2022'], id='381683598069776', grade=None), Module(num='T3INF1001', name='Mathematik I', credits=8.0, status='', semesters=['SoSe 2022', 'WiSe 2021/22'], id='380685560144022', grade=None), Module(num='T3INF1002', name='Theoretische Informatik I (MA-TINF21CS1)', credits=5.0, status='', semesters=['SoSe 2022'], id='382855008624547', grade=None), Module(num='T3INF1003', name='Theoretische Informatik II', credits=5.0, status='', semesters=['SoSe 2022'], id='382214102615788', grade=None), Module(num='T3INF1004', name='Programmieren', credits=9.0, status='', semesters=['SoSe 2022'], id='379974839816701', grade=None), Module(num='T3INF1005', name='Schlüsselqualifikationen', credits=5.0, status='', semesters=['SoSe 2022'], id='379974840574866', grade=None), Module(num='T3INF4102', name='Einführung in die Kryptologie', credits=5.0, status='', semesters=['SoSe 2022'], id='382214104541196', grade=None), Module(num='T3INF9000', name='Web and App Engineering', credits=5.0, status='', semesters=['SoSe 2022'], id='379974842066225', grade=None), Module(num='T3INF1006', name='Technische Informatik I', credits=5.0, status='bestanden', semesters=['WiSe 2021/22'], id='380703425164844', grade=1.2), Module(num='T3INF9001', name='Cyber Security Basics', credits=3.0, status='bestanden', semesters=['WiSe 2021/22'], id='379974841329087', grade=1.6)]
>>> s.get_exams_for_module(s.modules[9])
[Exam(semester='WiSe 2021/22', description='Hausarbeit (100%)', grade=1.6)]
```

## Contribution

This package is still work in progress. If you need data from CampusNet, that is currently not retrieved by it, please feel free to open an Issue or even PR for it.

We are studying at DHBW Mannheim, so this package is tested with [https://dualis.dhbw.de](https://dualis.dhbw.de). But it should also be compatible with other CampusNet instances from other universities. If you have acess to another CampusNet instance and use our script, let us know how it goes :).
