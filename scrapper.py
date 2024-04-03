import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def initialize(id, password, url):

    options = Options()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)

    driver.get(url)
	# Finding and clicking the login button (assuming it's the third button)
    # main_button = driver.find_elements(By.CSS_SELECTOR, 'a[role="button"]')[2]
    # main_button.click()

    # filling login information, id-password
    driver.find_element(By.ID, 'user_name') .send_keys(id)
    driver.find_element(By.ID, 'user_pas') .send_keys(password)

    # clicking the login button
    login_button = driver.find_element(By.CSS_SELECTOR, 'button.submit.btn.btn-primary.pull-right')
														# 'button[class="submit btn btn-send"]'
    login_button.click()

    # set grades page URL
    grades_url = 'https://kampus.izu.edu.tr/Ogr/OgrDersSinav'
    driver.get(grades_url)
    time.sleep(5)

	# Finding grade table and extracting column headers
    grade_table = driver.find_element(By.CSS_SELECTOR, 'div[data-ng-if="noteData"]')
    grade_columns = grade_table.find_element(By.CLASS_NAME, 'row').text.split('\n')[1:-2]

	# Initializing an empty list to store course data
    course_table = []

	# Looping through courses and extracting data
    courses = grade_table.find_elements(By.CSS_SELECTOR, 'div[data-ng-repeat="tnotlarNote in birim.tnotlarNotes"]')

    for course in courses:
        values = course.find_elements(By.CSS_SELECTOR, 'p[class="ng-binding ng-scope"]')

		# Extracting data for each course and appending it to the course table
        row = [value.text for value in values[1:-1]]
        course_table.append(row)

    return driver, course_table, grade_columns

def check(driver, course_table, grade_columns):
    # Refreshing the page to get updated grades
    driver.refresh()
    time.sleep(5)

    message = ""
    status = False

	# Finding grade table and extracting courses
    grade_table = driver.find_element(By.CSS_SELECTOR, 'table.table.table-striped.table-bordered.table-hover')
    courses = grade_table.find_elements(By.TAG_NAME, 'tr')[1:]

	# Looping through courses and comparing with previous data
    for i in range(len(courses)):
        values = courses[i].find_elements(By.CSS_SELECTOR, 'p[class="ng-binding ng-scope"]')
        row = [value.text for value in values[1:-1]]

		# Checking for any changes in grades
        for j in range(len(row)):
            if course_table[i][j] != row[j]:
                course_table[i][j] = row[j]
                status = True

				# Generating message for changed grades
                message += f"{row[0]}\n\n"
                for k in range(1, len(row)):
                    if row[k] != "--" and row[k] != "":
                        message += f"{grade_columns[k]}: {row[k]}\n"
                message += "--------------------------\n\n"

    return message, status, course_table
