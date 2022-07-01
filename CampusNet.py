import sys
from typing import Union
from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup


class LoginError(ValueError):
    pass


@dataclass
class Module:
    num: str
    name: str
    credits: float
    status: str
    semester: str
    id: str
    grade: Union[float, None] = None

@dataclass
class Exam:
    semester: str
    description: str
    grade: Union[float, None] = None

class CampusNetSession:
    def __init__(self, username: str = None, password: str = None, base_url="https://dualis.dhbw.de/"):
        """
        Initialize a new CampusNetSession.
        :param username: The username of the user.
        :param password: The password of the user.
        :raises:
            ValueError: If the username or password is empty.
            LoginError: If the login failed.
        """
        self.username = username
        self.password = password
        self.base_url = base_url
        self._semesters = None
        self._modules = None
        if self.username is None:
            raise ValueError("Username is empty.")
        if self.password is None:
            raise ValueError("Password is empty.")
        self.session = requests.Session()
        self._login()

    @property
    def mgrqispi(self):
        if self.base_url.endswith("/"):
            return self.base_url + "scripts/mgrqispi.dll"
        else:
            return self.base_url + "/scripts/mgrqispi.dll"

    """
    ```javascript
    >>> reloadpage.createUrlAndReload.toString()
    function(dispatcher, applicationName, programName, sessionNo, menuId,args){
        [...]
		window.location.href = dispatcher + \"?APPNAME=\" + applicationName + \"&PRGNAME=\" + programName + \"&ARGUMENTS=-N\" + sessionNo + \",-N\" + menuId  + temp_args;
	}
    ```
    """

    def create_url(self, program_name, args="", application_name="CampusNet"):
        # Note: MenuID is purely visual, so it doesn't matter. Always pass the HOME menu id.
        return f"{self.mgrqispi}?APPNAME={application_name}&PRGNAME={program_name}&ARGUMENTS=-N{self.session_number},-N00019{args}"

    def _login(self):
        """
        Login to the CampusNet.
        :raises:
            LoginError: If the login failed.
        """
        response = self.session.post(self.mgrqispi, data={
            'usrname': self.username,
            'pass': self.password,
            'APPNAME': 'CampusNet',
            'PRGNAME': 'LOGINCHECK',
            'ARGUMENTS': 'clino,usrname,pass,menuno,menu_type,browser,platform',
            'clino': '000000000000001',
            'menuno': '000324',
            'menu_type': 'classic',
            'browser': '',
            'platform': '',
        })
        if len(response.cookies) == 0:  # We didn't get a session token in response
            raise LoginError('Login failed.')

        # The header looks like this
        # 0; URL=/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=STARTPAGE_DISPATCH&ARGUMENTS=-N954433323189667,-N000019,-N000000000000000
        # url will be "/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=STARTPAGE_DISPATCH&ARGUMENTS=-N954433323189667,-N000019,-N000000000000000"
        # and arguments will be "-N954433323189667,-N000019,-N000000000000000"
        # 954433323189667 is the session id, 000019 is the menu id and -N000000000000000 are temporary arguments
        url = "=".join(response.headers["Refresh"].split(";")[
                       1].strip().split("=")[1:])
        arguments = url.split("ARGUMENTS=")[1]
        self.session_number = arguments.split(",")[0][2:]

    def _get_semesters(self):
        """
        Get the semesters from the CampusNet.
        :return: A list of semesters.
        """
        response = self.session.get(self.create_url('COURSERESULTS'))
        soup = BeautifulSoup(response.text, 'html.parser')
        semesters = {}
        for semester in soup.find_all('option'):
            semesters[semester.text] = semester.get('value')
        return semesters

    @property
    def semesters(self):
        """
        Lazily loads the semesters.
        :return: A dictionary of all semesters.
        """
        if not self._semesters:
            self._semesters = self._get_semesters()
        return self._semesters

    def _get_modules(self):
        """
        Get the modules from the CampusNet.
        :return: A list of modules.
        """
        modules = []
        for semester in self.semesters:
            response = self.session.post(self.mgrqispi, data={
                'APPNAME': 'CampusNet',
                'semester': self.semesters[semester],
                'Refresh': 'Aktualisieren',
                'PRGNAME': 'COURSERESULTS',
                'ARGUMENTS': 'sessionno,menuno,semester',
                'sessionno': self.session_number,
                'menuno': '000307'
            })

            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', {'class': 'nb list'})
            for row in table.find_all('tr')[1:]:
                cells = row.find_all('td')
                if len(cells) == 7:
                    try:
                        grade = float(cells[2].text.strip().replace(",", "."))
                    except ValueError:
                        grade = None
                    # getting id for this module
                    exams_button = cells[5]
                    # FIXME: This is a hack, looking for a specific substring in JavaScript code.
                    exams_script = exams_button.find('script').text
                    exams_id = exams_script.split('","Resultdetails"')[0].split(",-N")[-1]
                    modules.append(Module(
                        num=cells[0].text.strip(),
                        name=cells[1].text.strip(),
                        credits=float(cells[3].text.strip().replace(',', '.')),
                        status=cells[4].text.strip(),
                        semester=semester,
                        id=exams_id,
                        grade=grade
                    ))
                elif len(cells) != 0:
                    # FIXME: proper logging
                    print("Unexpected number of cells:",
                          len(cells), file=sys.stderr)
        return modules

    @property
    def modules(self):
        """
        Lazily loads the modules.
        :return: A list of all modules.
        """
        if not self._modules:
            self._modules = self._get_modules()
        return self._modules

    def get_exams_for_module(self, module: Module):
        """
        Get the exams for a module.
        :param module: The module.
        :return: A list of exams.
        """
        response = self.session.get(self.create_url('RESULTDETAILS', f",-N{module.id}"))
        soup = BeautifulSoup(response.text, 'html.parser')
        exam_table = soup.find('table', {'class': 'tb'})
        exams = []
        for row in exam_table.find_all("tr"):
            cells = row.find_all('td')
            if len(cells) == 6 and all("tbdata" in cell["class"] for cell in cells):
                try:
                    grade = float(cells[3].text.strip().replace(",", "."))
                except ValueError:
                    grade = None
                exams.append(Exam(
                    semester=module.semester,
                    description=cells[1].text.strip(),
                    grade=grade,
                ))
        return exams