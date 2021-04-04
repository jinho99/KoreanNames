import json
from bs4 import BeautifulSoup
from lxml import etree
import mysql.connector
import os
from random import randint
import re
import requests
import time

LASTNAME_MAX_PAGE = 20

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='my-secret-pw',
    database='project'
)

def register_students(num=500, delete_existings=False):

    mycursor = mydb.cursor()
    if delete_existings:
        sql = 'DELETE FROM student WHERE id > 0'
        mycursor.execute(sql)
        mydb.commit()

    names = generate_names(num)
    dept_min = 1
    dept_max = 20
    grade_min = 1
    grade_max = 4

    sql = 'INSERT INTO student (name, dept_id, grade) VALUES(%s, %s, %s)'
    val = []
    for name in names:
        val.append((name, randint(dept_min, dept_max), randint(grade_min, grade_max)))
    mycursor.executemany(sql, val)
    mydb.commit()

def generate_names(num=500):
    """
    가장 많이 쓰이는 한국 성씨와 이름들을 크롤링으로 가져온뒤
    random하게 full name을 생성한다.
    :param num: number of names to generate
    :return: list of full names
    """
    fullnames = []
    lastnames = get_lastnames()
    firstnames = get_firstnames()

    for i in range(num):
        fullnames.append(lastnames[randint(0, len(lastnames)-1)] +\
                         firstnames[randint(0, len(firstnames)-1)])
    return fullnames

def get_firstnames(save_file=False):
    filename = 'firstnames.txt'
    firstnames = []
    if save_file:
        if os.path.exists(filename):
            os.remove(filename)

    for i in range(1, LASTNAME_MAX_PAGE+1):
        names = []
        headers = {
            'Content-type': 'application/json'
        }
        url = f'https://koreanname.me/api/rank/2008/2021/{i}'
        try:
            r = requests.get(url)
            if r.status_code == 200:
                jsondata = r.json()
                names += [x['name'] for x in jsondata['female']]
                names += [x['name'] for x in jsondata['male']]
                if not jsondata['femaleHasNext'] and not jsondata['maleHasNext']:
                    break
                if save_file:
                    save_to_file(filename, names)
                firstnames += names
            print(f'page {i} processed.')

        except Exception as e:
            print(f'failed to fetch {url}. {e}')

        time.sleep(1)

    return firstnames

def get_lastnames():
    url = 'https://m.blog.naver.com/for_my_blog/221792214148'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    trs = soup.select('#SE-ddd10a8e-98a4-4931-b58a-ec498066505b > div > div > div > table > tbody')

    dom = etree.HTML(str(trs[0]))
    spans = dom.xpath('//td[2]/div/p/span')
    return [re.search(r'[^\(]+', x.text).group(0) for x in spans if not x]

def save_to_file(filename, names):
    with open(filename, 'a+', encoding='utf-8') as f:
        f.write('\n'.join(names) + '\n')
        f.flush()

def run_main():
    register_students(num=20000, delete_existings=True)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_main()

