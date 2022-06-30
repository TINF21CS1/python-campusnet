# Julian Lemmerich
# 30.06.2022
# Interacting with Campus net
# more specifically DHBW's Campusnet at dualis.dhbw.de

import requests
import re

## Login

email = 's212689%40student.dhbw-mannheim.de' #urlencoded! @ = %40
password = input('Password: ')

headers = {
    'Host': 'dualis.dhbw.de',
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = f'usrname={email}&pass={password}&APPNAME=CampusNet&PRGNAME=LOGINCHECK&ARGUMENTS=clino%2Cusrname%2Cpass%2Cmenuno%2Cmenu_type%2Cbrowser%2Cplatform'

response = requests.post('https://dualis.dhbw.de/scripts/mgrqispi.dll', headers=headers, data=data)

cnsc = response.headers['Set-cookie'][0:38].replace(" ", "") #cookie in format "csnc =FA27B61020C03AA5A83046B13D6CC38D; HttpOnly; secure" broken down to "csnc=FA27B61020C03AA5A83046B13D6CC38D"
# TODO: something is borken with that cnsc. It looks identical to a valid one, but only gives access denied.
cnsc = 'cnsc=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# TODO get -N Arguments from response redirect?

## Get all Semesters

# Prüfungsergebnisse Tab: https://dualis.dhbw.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=COURSERESULTS&ARGUMENTS=-N422875220398735,-N000307,
# die arguments sind wohl dynamisch...
# Semesterlist: <select id="semester" .*> </select>
# then get value from option, display name

headers = {
    'Host': 'dualis.dhbw.de',
    'Cookie': cnsc,
}

response = requests.get('https://dualis.dhbw.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=COURSERESULTS&ARGUMENTS=-N518587923698845,-N000019', data="", headers=headers)

semester = {}

for match in re.findall('<option value=".*</option>', response.text):
    semester[match.split('>')[1].split('<')[0]]=match[15:30] #key=name, value=id

## Get all Prüfungen in Semester

print("Getting Modules")

overview=list() # table is cross semester, so initialized outside

for semestername in semester:
    print(semestername)
    headers = {
        'Host': 'dualis.dhbw.de',
        'Cookie': cnsc,
    }
    response = requests.get(f'https://dualis.dhbw.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=COURSERESULTS&ARGUMENTS=-N518587923698845,-N000019,-N{semester[semestername]}', data="", headers=headers) #get page with Prüfungen Table
    tempoverview = re.findall('<table class="nb list">[\s\S]*</table>', response.text)[0] # extract table from html body
    tempoverview = re.findall('<tbody>[\s\S]*</tbody>', tempoverview)[0] # extract table body from table
    temprows = tempoverview.split('<tr')[1:-1] # extract all rows from table. [0] is just <tbody ...>

    for row in temprows:
        tempcells = row.split('<td')[1:] # extract all columns from table
        currentrow = list()
        for cell in tempcells:
            cell = cell.split('>', 1)[1].split('</td')[0].lstrip().rstrip() # extract content from cell, remove whitespaces from left and right
            if cell.startswith("<a"): #cell with the link
                cell = cell.split('href="', 1)[1].split('">')[0].replace("&amp;", "&") #only take content in a href="..." and convert url-encoding back to normal
            currentrow.append(cell) # combine cells to row
        currentrow = currentrow[:-1] # i know thats horrible coding, i dont know where that extra cell is from, please fix TODO
        overview.append(currentrow) # combine rows to table

print(overview)

## Get Prüfungen Results

print("Getting Prüfungsresults")

detailview = list() # ['Modulenr', 'Name', 'Course', 'Semester', 'Prüfung', 'Date', 'Bewertung']

for module in overview:
    print(module[1])
    headers = {'Host': 'dualis.dhbw.de', 'Cookie': cnsc,}
    response = requests.get(f'https://dualis.dhbw.de{module[-1]}', data="", headers=headers)
    tempdetails = re.findall('<table class="tb"[\s\S]*</table>', response.text)[0] # extract first table from html body, as it contains the prüfungen
    while '<td class="level02"' in tempdetails:
        currentrow = list()
        currentrow.append(module[0])
        currentrow.append(module[1])
        tempdetails = tempdetails.split('<td class="level02"', 1)[1].split('>', 1)[1].split('</td',1) #remove everything before "level2"-heading. and split left of td end and right. left goes into table, right will be further edited.
        currentrow.append(tempdetails[0])
        tempdetails = tempdetails[1]
        if '<tr>' not in tempdetails: detailview.append(currentrow); break
        tempdetails = tempdetails.split('<tr>', 1)[1].split('</tr>',1) #cut off before next <tr> and split at /tr. [0] is not prüfungstable, [1] is for the next loop
        for cell in re.findall('<td .*>[\s\S]*</td>', tempdetails[0]): #loops over all td elements #TODO this only returns one giant match instead of a list of multiple matches???
            currentrow.append(tempdetails[0].split('>', 1)[1].split('<')[0]) #get content between html tags
        #currentrow = currentrow[] #last two are extern anerkannt and empty, so they get cut off

        detailview.append(currentrow)
        tempdetails = tempdetails[1] #ready for the next loop

print(detailview)