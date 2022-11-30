# Scrapes emails of students from elearning.iba-suk.edu.pk


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import time, sleep
import os
import json

USERNAME = os.environ['ELEARNING_USERNAME']
PASSWORD = os.environ['ELEARNING_PASSWORD']

# set up web driver
options = webdriver.ChromeOptions()
options.add_argument("--disable-site-isolation-trials")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

driver.implicitly_wait(8)
driver.maximize_window()

driver.get('http://elearning.iba-suk.edu.pk/')

# login to the page
name_input = driver.find_element(By.CSS_SELECTOR, "input#username")
password_input = driver.find_element(By.CSS_SELECTOR, "input#password")
name_input.send_keys(USERNAME)
password_input.send_keys(PASSWORD)

login_btn = driver.find_element(By.CSS_SELECTOR, "button#loginbtn")
login_btn.click()


# go to a course page and grab every user's profile link
user_links = []

for i in range(5):
    course_link = f'http://elearning.iba-suk.edu.pk/user/index.php?id=1086&page={i}'
    driver.get(course_link)
    
    atags = driver.find_elements(By.CSS_SELECTOR, "tbody tr a")

    for a in atags:
        user_links.append(a.get_attribute('href'))

    sleep(2)


print(f'Total links found: {len(user_links)}')
print(user_links)

with open('profile_links.json', mode='w') as f:
    json.dump(user_links, f, indent=2)



# go to each user's profile, grab his/her name and email

with open('profile_links.json') as f:
    user_links = json.load(f)


students_info = []

letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ '

for link in user_links:
    driver.get(link)
    try:
        grabbed_name = driver.find_element(By.CSS_SELECTOR, "a[aria-current='page']").text
        student_email = driver.find_element(By.CSS_SELECTOR, "dd a[href^='mailto']").text
    except:
        continue
    else:
        student_name = ''.join([char for char in grabbed_name if char in letters])
        student_name = student_name.title()
        info = {
            'name':student_name,
            'email': student_email
        }
        print(info)
        students_info.append(info)



with open('student_info.json', mode='w') as f:
    json.dump(students_info, f, indent=2)



