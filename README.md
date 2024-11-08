# MTU Course Scraper

A comprehensive system for scraping, processing, and storing Michigan Tech University course data. This system consists of three main components: the Course Scraper, Building Lookup, and Database Manager.

## System Components

### 1. Course Scraper
The main scraping script that extracts course information from MTU's Banweb system.

**Key Features:**
- Uses Selenium WebDriver with Firefox to automate web navigation
- Scrapes multiple semesters of course data
- Creates organized directory structure by semester
- Extracts detailed course information including:
  - CRN and direct link
  - Course details (subject, number, section)
  - Scheduling information (days, times, location)
  - Enrollment statistics
  - Instructor information

**Output Format:**
```json
{
    "CRN": "10004",
    "CRN_Link": "https://www.banweb.mtu.edu/owassb/bwckschd.p_disp_listcrse?term_in=199409&subj_in=AF&crse_in=101&crn_in=10004",
    "Subject": "AF",
    "Course": "101",
    "Section": "01L",
    "Campus": "1",
    "Credits": "0.000",
    "Title": "Aerospace Studies 1",
    "Days": "T",
    "Time": "01:00 pm-01:55 pm",
    "Max Enroll": "160",
    "Current Enroll": "18",
    "Seats Available": "142",
    "Instructor": "Matkin",
    "Dates": "09/06-11/11",
    "Location": "04 0100",
    "Lab Fee": ""
}
```

### 2. Building Lookup Script
Processes the location codes in the JSON files and converts them to human-readable building names.

**Key Features:**
- Uses SortedDict for efficient building code lookup
- Maintains a comprehensive mapping of MTU building codes to names
- Updates location information in-place within JSON files
- Handles building numbers from 1 to 119
- Preserves room numbers while updating building names

**Example Conversion:**
- Input: `"Location": "04 0100"`
- Output: `"Location": "ROTC Building 0100"`

### 3. Database Manager (MkDB)
Handles the storage of course data in a MySQL database with automated schema and table creation.

**Key Features:**
- Automatic database and table creation based on directory structure
- UUID generation for unique record tracking
- Handles multiple semesters and course subjects
- Efficient bulk data insertion
- Error handling and logging

**Database Structure:**
- Creates a schema for each semester
- Tables named after course subjects
- Columns match JSON structure
- Includes additional fields:
  - `id`: Auto-incrementing primary key
  - `uuid`: Unique identifier for each record

## Setup Requirements

1. Python Dependencies:
```
selenium
beautifulsoup4
mysql-connector-python
sortedcontainers
webdriver-manager
```

2. System Requirements:
- Firefox browser installed
- Firefox WebDriver (automatically managed)
- MySQL Server
- Python 3.x

3. Database Configuration:
```python
db_config = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost'
}
```

## Usage Flow

1. Run the Course Scraper:
   - Scrapes course data from Banweb
   - Creates JSON files organized by semester

2. Run the Building Lookup:
   - Processes all JSON files in the directory
   - Updates location codes to building names

3. Run the Database Manager:
   - Creates necessary database schemas and tables
   - Imports processed JSON data into MySQL

## Notes

- The system handles view-only semesters differently in directory naming
- Building codes are continuously updated to match MTU's current building numbering system
- Each component can be run independently if needed
- JSON files serve as an intermediate format for data verification and backup
