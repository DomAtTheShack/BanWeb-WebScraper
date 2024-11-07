import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Set the Firefox profile path
firefox_profile_path = "/home/dominichann/snap/firefox/common/.mozilla/firefox/rpnr6zsq.python"

# Configure Firefox options
firefox_options = Options()
firefox_options.add_argument("-profile")
firefox_options.add_argument(f"{firefox_profile_path}")

# Initialize the Firefox driver
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)

# URL for selecting the term
term_url = "https://www.banweb.mtu.edu/owassb/bzskfcls.p_sel_crse_search"

# Step 1: Visit the term selection page
driver.get(term_url)

# Explicit wait: Wait for the term dropdown to load
wait = WebDriverWait(driver, 10)
dropdown = wait.until(EC.presence_of_element_located((By.NAME, "p_term")))

# Step 2: Select the term from the dropdown menu
select_term = Select(dropdown)
select_term.select_by_value("202501")  # Adjust this based on the term options

# Step 3: Submit the form to search for courses
driver.find_element(By.XPATH, "//input[@type='submit' and @value='Submit']").click()

# Explicit wait: Wait for the course selection page to load
wait.until(EC.presence_of_element_located((By.NAME, "sel_subj")))

# Step 4: Select course type from the dropdown menu
course_table = driver.find_element(By.CLASS_NAME, 'dataentrytable')

# Split the data into lines
course_lines = course_table.text.split("\n")

# Regular expression to match the course code and name
course_pattern = re.compile(r"([A-Z]+)-([A-Za-z\s&-]+)")

# Initialize an empty list to store the courses
course_list = []

# Iterate over the lines and match the course data
for line in course_lines:
    # Check if the line is not empty and matches the course pattern
    if line.strip():  # Ignore empty lines
        match = course_pattern.match(line.strip())  # Strip leading/trailing spaces
        if match:
            course_code = match.group(1)
            course_name = match.group(2)
            course_list.append((course_code, course_name))

option = driver.find_element(By.XPATH, f"//option[@value='ACC']").click()
# Now submit the form by clicking the submit button
submit_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Class Search']")
submit_button.click()


# Explicit wait: Wait for the course list to load
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'datadisplaytable')))

# Step 5: Scrape the page content after it's rendered by JavaScript
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Look for the course table
course_table = soup.find('table', {'class': 'datadisplaytable'})
if course_table:
    # Loop through each row in the table (assuming the first row is headers)
    for row in course_table.find_all('tr')[1:]:  # Skip header row
        columns = row.find_all('td')
        course_data = [col.text.strip() for col in columns]
        # Print or store the course data
        print("Course Information:", course_data)
else:
    print("Failed to find the course table.")

# Close the driver
driver.quit()
