## Example usage

```python
$ python3 -i CampusNet.py
>>> s = CampusNetSession("s***REMOVED***@student.dhbw-mannheim.de", "***REMOVED***")
>>> s.modules
[Module(num='T3_1000', name='Praxisprojekt I', credits=20.0, status='', semesters=['SoSe 2022'], id='381683598069776', grade=None), Module(num='T3INF1001', name='Mathematik I', credits=8.0, status='', semesters=['SoSe 2022', 'WiSe 2021/22'], id='380685560144022', grade=None), Module(num='T3INF1002', name='Theoretische Informatik I (MA-TINF21CS1)', credits=5.0, status='', semesters=['SoSe 2022'], id='382855008624547', grade=None), Module(num='T3INF1003', name='Theoretische Informatik II', credits=5.0, status='', semesters=['SoSe 2022'], id='382214102615788', grade=None), Module(num='T3INF1004', name='Programmieren', credits=9.0, status='', semesters=['SoSe 2022'], id='379974839816701', grade=None), Module(num='T3INF1005', name='Schlüsselqualifikationen', credits=5.0, status='', semesters=['SoSe 2022'], id='379974840574866', grade=None), Module(num='T3INF4102', name='Einführung in die Kryptologie', credits=5.0, status='', semesters=['SoSe 2022'], id='382214104541196', grade=None), Module(num='T3INF9000', name='Web and App Engineering', credits=5.0, status='', semesters=['SoSe 2022'], id='379974842066225', grade=None), Module(num='T3INF1006', name='Technische Informatik I', credits=5.0, status='bestanden', semesters=['WiSe 2021/22'], id='380703425164844', grade=1.2), Module(num='T3INF9001', name='Cyber Security Basics', credits=3.0, status='bestanden', semesters=['WiSe 2021/22'], id='379974841329087', grade=1.6)]
>>> s.get_exams_for_module(s.modules[9])
[Exam(semester='WiSe 2021/22', description='Hausarbeit (100%)', grade=1.6)]
```
