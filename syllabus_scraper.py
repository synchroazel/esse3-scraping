import argparse
import mechanize
import os
import pandas as pd
from bs4 import BeautifulSoup as bs
from tqdm import tqdm


def find_syllabus(course_name):
    url = 'https://www.esse3.unitn.it/Guide/PaginaRicercaInse.do'

    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(url)
    br.select_form(nr=0)

    br.form['nomeInse'] = course_name

    req = br.submit(id='actionBar1')

    soup = bs(req.read(), features="html5lib")

    href = str()

    found = False

    results = [result.text.lower().strip() for result in soup.find(id='risultati').find_all('a')]

    if course_name.lower().strip() in results:

        for element in soup.find(id='risultati').find_all('a'):

            if element.text.lower().strip() == course_name.lower().strip():
                href = element.get('href')

    elif len(results) == 0:

        print('No result was found for \'%s\'' % course_name)

    else:

        print('\nWhich of the following is the right course for \'%s\'?' % course_name)

        i = 1

        for course in [result.text for result in soup.find(id='risultati').find_all('a')]:
            print('[%d] %s' % (i, course))
            i += 1

        choice = input()

        href = soup.find(id='risultati').find_all('a')[int(choice) - 1].get('href')

    return 'https://www.esse3.unitn.it/' + href


if __name__ == '__main__':

    courses = pd.read_csv('courses_db.csv').Course
    syllabus_links = list()

    os.system('clear')

    for course in tqdm(courses):
        syllabus_links.append(find_syllabus(course))

    df = pd.DataFrame(zip(courses, syllabus_links), columns=['course', 'syllabus']).to_csv('syllabuses.csv')
