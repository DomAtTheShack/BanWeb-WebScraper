import json
import os
import re

from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

# Set the Firefox profile path
firefox_profile_path = "C:\\Users\\dooli\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\8r1v7kxn.python"

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
dropdown_element = wait.until(EC.presence_of_element_located((By.NAME, 'p_term')))

# Create a Select object for the dropdown
select_term = Select(dropdown_element)

# Initialize an empty list to store the options
options_list = []

# Loop through each option in the dropdown (skipping the first "None" option)
for option in select_term.options[1:]:
    # Get the text of the option
    option_text = option.text.strip()

    # Check if "View Only" is in the option text
    is_view_only = "View only" in option_text

    # Get the value attribute of the option
    option_value = option.get_attribute("value")

    # Add the option details to the list
    options_list.append({
        "text": option_text,
        "value": option_value,
        "view_only": is_view_only
    })

for semValue in options_list[17:]:

    dropdown_element = wait.until(EC.presence_of_element_located((By.NAME, 'p_term')))
    select_term = Select(dropdown_element)
    sem_value = semValue.get("value")  # This gives you the value from the dictionary
    select_term.select_by_value(sem_value)  # Adjust this based on the term options


    today = datetime.now().strftime("%d-%m-%Y")

    if semValue.get("view_only") == False:
        os.mkdir("./" + semValue.get("text") + '-' + today)
    else:
        os.mkdir("./" + semValue.get("text"))

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
    course_type_list = []

    # Iterate over the lines and match the course data
    for line in course_lines:
        # Check if the line is not empty and matches the course pattern
        if line.strip():  # Ignore empty lines
            match = course_pattern.match(line.strip())  # Strip leading/trailing spaces
            if match:
                course_code = match.group(1)
                course_name = match.group(2)
                course_type_list.append((course_code, course_name))

    for (course_code, course_name) in course_type_list:
        # Select the course type option
        option = driver.find_element(By.XPATH, f"//option[@value='{course_code}']").click()

        # Submit the form by clicking the submit button
        submit_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Class Search']")
        submit_button.click()

        # Explicit wait: Wait for the course list to load
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'datadisplaytable')))

        # Scrape the page content after it's rendered by JavaScript
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Look for the course table
        course_table = soup.find('table', {'class': 'datadisplaytable'})
        course_list = []

        if course_table:
            # Loop through each row in the table (skipping the header row)
            for row in course_table.find_all('tr')[2:]:  # Skip header row
                columns = row.find_all('td')

                # Check if the first column has an <a> tag with an href attribute
                crn_cell = columns[0].find('a')
                if crn_cell:
                    crn = crn_cell.text.strip()
                    crn_link = crn_cell['href']
                else:
                    crn = columns[0].text.strip()
                    crn_link = "N/A"  # Set to None if there's no link

                # Extract remaining column data
                course_data = [col.text.strip() for col in columns]

                # Define headers and map them to course data, adding CRN link
                course_info = {
                    "CRN": crn,
                    "CRN_Link": "https://www.banweb.mtu.edu" + crn_link,
                    "Subject": course_data[1],
                    "Course": course_data[2],
                    "Section": course_data[3],
                    "Campus": course_data[4],
                    "Credits": course_data[5],
                    "Title": course_data[6],
                    "Days": course_data[7],
                    "Time": course_data[8],
                    "Max Enroll": course_data[9],
                    "Current Enroll": course_data[10],
                    "Seats Available": course_data[11],
                    "Instructor": course_data[12],
                    "Dates": course_data[13],
                    "Location": course_data[14],
                    "Lab Fee": course_data[15] if len(course_data) > 15 else None,  # Check for Lab Fee
                }

                # Append to course list
                course_list.append(course_info)

                # Append to course list
                course_list.append(course_info)

            # Convert to JSON format
            course_json = json.dumps(course_list, indent=4)

            # Save JSON to file named after course name and date
            if semValue.get("view_only") == True:
                with open(f'./{semValue.get("text")}/{course_name}.json', 'w') as f:
                    f.write(course_json)
            else:
                with open(f'./{semValue.get("text") + '-' + today}/{course_name}.json', 'w') as f:
                    f.write(course_json)
        else:
            print("Failed to find the course table for course:", course_name)

        # Navigate back to the previous page to select the next course
        driver.back()

        wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='submit' and @value='Class Search']")))
        option = driver.find_element(By.XPATH, "//input[@type='reset' and @value='Reset']").click()

    driver.back()

    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='submit' and @value='Submit']")))

# Close the driver
driver.quit()
