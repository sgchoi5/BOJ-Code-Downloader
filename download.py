import sys
import requests
import getpass
from bs4 import BeautifulSoup as bs

url = "https://www.acmicpc.net"

USER_INFO = {
    'id': '',
    'pw': ''
}

TYPE_TABLE = {
    'C': '.c',
    'C (Clang)': '.c',
    'C11': '.c',
    'C11 (Clang)': '.c',
    'C++': '.cpp',
    'C++ (Clang)': '.cpp',
    'C++11': '.cpp',
    'C++11 (Clang)': '.cpp',
    'C++14': '.cpp',
    'C++14 (Clang)': '.cpp',
    'C++17': '.cpp',
    'C++17 (Clang)': '.cpp',
    'Python 2': '.py',
    'Python 3': '.py',
    'Pypy': '.py',
    'Pypy 3': '.py',
    'Java': '.java',
    'Text': '.txt'
}

sess = requests.Session()

def load_user_data():
    id_str = input("\nUser ID:")
    pw_str = getpass.getpass("User PW:")
    USER_INFO['id'] = id_str
    USER_INFO['pw'] = pw_str

def sign_in():
    data = {
        'login_user_id': USER_INFO['id'],
        'login_password': USER_INFO['pw']
    }
    sess.post(url + "/signin", data=data)

def is_invalid_login():
    soup = bs(sess.get(url).text, 'html.parser')
    if soup.find('a', {'class': 'username'}) is None:
        print("Login failed : Invalid ID or Password.")
        return True
    else:
        return False

def print_problem_list(x, total):
    if x == 1: print()
    print("\rCreating accept-code list... [%.2f%%]" % (min(x / total * 100, 100)), end='')

def print_downloading(x, total):
    if x == 1 or x == 2: print(); return
    end_idx = int(30 * x / total)
    print("\rDownloading: |", end='')
    for i in range(end_idx):
        print("#", end='')
    for i in range(30 - end_idx):
        print('_', end='')
    print("|", end='')
    print(" [%d/%d | %.2f%%]" % (x, total, x / total * 100), end='')
    if x == total: print(" [finished]")

def make_problem_list():
    soup = bs(sess.get(url + "/user/" + USER_INFO['id']).text, 'html.parser')
    problem_total_num = int(soup.find(href="/status?user_id=" + USER_INFO['id'] + "&result_id=4").string)
    problem_list = []
    problem_url = url + "/status?user_id=" + USER_INFO['id'] + "&result_id=4"
    idx = 0
    while True:
        soup = bs(sess.get(problem_url).text, 'html.parser')
        trlist = soup.find('tbody').find_all('tr')
        for tr in trlist:
            idx += 1
            print_problem_list(idx, problem_total_num)
            a = tr.find_all('a')

            ProblemNum = a[1].string
            ProblemUrl = url + "/source/download/" + tr.find('td').string
            if a[2].string.strip() in TYPE_TABLE:
                FileName = ProblemNum + TYPE_TABLE[a[2].string.strip()]
                problem_list.append((ProblemNum, ProblemUrl, FileName))

        next_page = soup.find(id='next_page')
        if next_page != None:
            problem_url = url + next_page['href']
        else:
            break
    return problem_list

def sort_problem_list(problem_list):
    problem_list.sort()
    idx = 1
    while 1:
        if problem_list[idx - 1][0] == problem_list[idx][0]:
            del problem_list[idx - 1]
            idx -= 1
        idx += 1
        if idx >= len(problem_list):
            break

def download(problem_list):
    idx = 0
    for problem in problem_list:
        idx += 1
        print_downloading(idx, len(problem_list))
        res = sess.get(problem[1])
        with open("./download/" + problem[2], "wb") as f:
            for chunk in res.iter_content(1024):
                f.write(chunk)

if __name__ == "__main__":
    load_user_data()
    sign_in()

    if is_invalid_login():
        sys.exit()

    problem_list = make_problem_list()
    sort_problem_list(problem_list)
    download(problem_list)

    sess.close()
