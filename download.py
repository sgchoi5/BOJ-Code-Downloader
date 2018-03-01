import sys
import requests
import getpass
import platform
from selenium import webdriver
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


def print_file_list(x, total):
    if x == 1: print()
    print("\rCreating file list... [%.2f%%]" % (min(x / total * 100, 100)), end='')


def print_downloading(x, total):
    if x == 1 or x == 2: print(); return
    end_idx = int(30 * x / total)
    print("\rDownloading : |", end='')
    for i in range(end_idx):
        print("#", end='')
    for i in range(30 - end_idx):
        print('_', end='')
    print("|", end='')
    print(" [%d/%d | %.2f%%]" % (x, total, x / total * 100), end='')
    if x == total: print("\n\nDownload finished!")


# Input user data
USER_INFO['id'] = input("\nUser ID:")
USER_INFO['pw'] = getpass.getpass("User PW:")

print("----------------------------------------------------------------------------------------------------")

# Set driver
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
os_name = platform.system()
if os_name == "Windows":
    driver = webdriver.Chrome('./driver/chromedriver_win.exe', chrome_options=options)
elif os_name == "Darwin":
    driver = webdriver.Chrome('./driver/chromedriver_mac', chrome_options=options)
elif os_name == "Linux":
    driver = webdriver.Chrome('./driver/chromedriver_linux', chrome_options=options)

# Login by driver
driver.get(url + "/login")
driver.find_element_by_name('login_user_id').send_keys(USER_INFO['id'])
driver.find_element_by_name('login_password').send_keys(USER_INFO['pw'])
driver.find_element_by_xpath("/html/body/div[3]/div[3]/div/div/form/div[4]/div[2]/button").click()

print("----------------------------------------------------------------------------------------------------")

# Set cookies
sess = requests.Session()
cookies = driver.get_cookies()
for cookie in cookies:
    sess.cookies.set(cookie['name'], cookie['value'])

# Login check
soup = bs(sess.get(url).text, 'html.parser')
if soup.find('a', {'class': 'username'}) == None:
    print("\nLogin failed : Invalid ID or Password.")
    sys.exit()

# Creating file list
soup = bs(sess.get(url + "/user/" + USER_INFO['id']).text, 'html.parser')
problem_total_num = int(soup.find(href="/status/?user_id=" + USER_INFO['id'] + "&result_id=4").string)
problem_list = []
problem_url = url + "/status/?user_id=" + USER_INFO['id'] + "&result_id=4"
idx = 0
while True:
    soup = bs(sess.get(problem_url).text, 'html.parser')
    trlist = soup.find('tbody').find_all('tr')
    for tr in trlist:
        idx += 1
        print_file_list(idx, problem_total_num)
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

# Sort problem list
problem_list.sort()
idx = 1
while 1:
    if problem_list[idx - 1][0] == problem_list[idx][0]:
        del problem_list[idx - 1]
        idx -= 1
    idx += 1
    if idx >= len(problem_list):
        break

# Download source codes
idx = 0
for problem in problem_list:
    idx += 1
    print_downloading(idx, len(problem_list))
    res = sess.get(problem[1])
    with open("./download/" + problem[2], "wb") as f:
        for chunk in res.iter_content(1024):
            f.write(chunk)
print("\n----------------------------------------------------------------------------------------------------")
