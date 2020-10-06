from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

def gettable():

    url = 'https://www.worldometers.info/coronavirus/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    body = [str(i).split('\n') for i in soup.find('table').findAll('tr')]
    for i in range(len(body)):
                    body[i].pop(0)

    for a in range(len(body)):         
            lst = [re.findall('>.*<', i) for i in body[a] if re.findall('>.*<', i)]
            lst = [i[0] for i in lst]
            lst = [i.replace(',', '').replace('+', '') for i in lst]
            for i in range(len(lst)):
                    lst[i] = list(lst[i])
                    lst[i].pop()
                    lst[i].pop(0)
                    lst[i] = ''.join(lst[i])
            lst = [i.replace('</a>', '').replace('/span', '').replace('<strong>', '').replace('</strong>', '') for i in lst]
            for i in range(len(lst)):
                    if re.findall('<a.*">', lst[i]):
                            lst[i] = lst[i].replace(re.findall('<a.*">', lst[i])[0], '')
                    if re.findall('<span.*">', lst[i]):
                            lst[i] = lst[i].replace(re.findall('<span.*">', lst[i])[0], '')
            lst2 = lst[len(lst)-1].split('<td>')
            for i in range(len(lst2)):
                    lst2[i] = lst2[i].replace('</td>', '')
            lst.pop()
            for i in lst2:
                    lst.append(i)
            
            body[a] = lst

    body.pop(0)

    for i in range(len(body)):
            for i2 in range(len(body[i])):
                    if body[i][i2] == '' or body[i][i2] == ' ' or 'N/A' in body[i][i2]:
                            body[i][i2] = ''
                    try:
                            body[i][i2] = int(body[i][i2])
                    except:
                            pass
            if len(body[i]) == 18:
                    body[i].append('')

    for i in body:
        i.pop(0)

    body = body[8:len(body)-8]

    def takeSecond(elem):
        return elem[1]

    body.sort(key=takeSecond, reverse=True)

    for i in range(len(body)):
        body[i][0] = body[i][0].replace('<', '').replace('>', '')

        body[i][2] = '+'+str(body[i][2]) if body[i][2] else body[i][2]

    return body
