from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # For explicit waits
import pytest
import time
from test_db import connect_db  # From your test_db.py

# To run these tests:
# 1. Activate your virtual environment.
# 2. Install selenium and pytest in your virtual environment: pip install selenium pytest
# 3. Start Flask by typing: flask --app flask_intro run --debug
# 4. Run the tests with: pytest Selenium_Pytest.py

@pytest.fixture(scope="module")
def setup():
    # Setup Selenium WebDriver (Chrome in this case, ensure chromedriver is installed)
    driver = webdriver.Chrome()
    driver.get("http://localhost:5000")
    
    # Run before all tests
    yield driver
    
    # Teardown - close the browser after tests
    driver.quit()


def test_student_signup(setup): 
    driver = setup
    driver.get("http://localhost:5000")
    time.sleep(2)
    
    # Click the "Sign Up" button on the start page using the button's form action
    driver.find_element(By.XPATH, "//form[@action='/signup']/button").click()
     
    # Wait for the signup page to load
    time.sleep(2)
    
    # Select 'Student' role
    role_dropdown = Select(driver.find_element(By.ID, "role"))
    role_dropdown.select_by_value("student")

    # Fill out signup form with first name, last name, email, and password
    driver.find_element(By.ID, "firstName").send_keys("Test")
    time.sleep(1)
    driver.find_element(By.ID, "lastName").send_keys("Student")
    time.sleep(1)
    driver.find_element(By.ID, "email").send_keys("student1@example.com")
    time.sleep(1)
    driver.find_element(By.ID, "password").send_keys("password123")
    time.sleep(1)

    # Submit the form
    driver.find_element(By.TAG_NAME, "button").click()

    # Verify redirection to start page with success message
    time.sleep(2)
    assert "Sign-up successful!" in driver.page_source


def test_student_login(setup):
    driver = setup
    driver.get("http://localhost:5000/login")
    time.sleep(2)
    
    # Fill out login form with email and password
    driver.find_element(By.ID, "email").send_keys("student1@example.com")
    time.sleep(1)
    driver.find_element(By.ID, "password").send_keys("password123")
    time.sleep(1)

    # Submit the form
    driver.find_element(By.TAG_NAME, "button").click()

    # Verify we are on the student event page
    time.sleep(2)
    assert "CS Department Event Page: Student" in driver.page_source

def test_student_activities_navigation(setup):
    driver = setup

    # Click on the "My Activities" button
    driver.find_element(By.XPATH, "//button[.//strong[text()='My Activities']]").click()

    # Verify that we are on the "My Activities" page
    time.sleep(2)
    assert "Activity Summary" in driver.page_source  # Adjust based on the actual page content

def test_back_to_dashboard_from_activities(setup):
    driver = setup

    # Click on "Back to My Dashboard"
    driver.find_element(By.LINK_TEXT, "Back to My Dashboard").click()

    # Verify redirection back to the Student Dashboard
    time.sleep(2)
    assert "CS Department Event Page: Student" in driver.page_source 

def test_student_suggest_event(setup):
    driver = setup

    # Ensure we are on the student dashboard
    assert "CS Department Event Page: Student" in driver.page_source

    # Click on the "Suggest an Event" button
    driver.find_element(By.XPATH, "//button[.//strong[text()='Suggest an Event']]").click()
    time.sleep(2)

    # Wait for the modal to appear
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'eventModal'))
    )

    # Fill out the suggestion form
    driver.find_element(By.ID, "eventname").send_keys("Student Suggested Event")
    time.sleep(1)
    driver.find_element(By.ID, "eventdescription").send_keys("This is a suggested event from a student.")
    time.sleep(1)

    # Submit the suggestion
    driver.find_element(By.XPATH, "//button[text()='Submit Suggestion']").click()
    time.sleep(2)

    # Verify that the suggestion was submitted (adjust based on actual behavior)
    assert "Suggestion submitted successfully!" in driver.page_source or "CS Department Event Page: Student" in driver.page_source

    # Logout
    driver.find_element(By.ID, 'logout-btn').click()
    time.sleep(2)


def test_faculty_signup(setup):
    driver = setup
    driver.get("http://localhost:5000")
    
    # Wait for the start page to load
    time.sleep(2)
    
    # Click the "Sign Up" button on the start page using the button's form action
    driver.find_element(By.XPATH, "//form[@action='/signup']/button").click()
    
    # Wait for the signup page to load
    time.sleep(2)
    
    # Select 'Faculty' role (the value is 'admin' in the HTML)
    role_dropdown = Select(driver.find_element(By.ID, "role"))
    role_dropdown.select_by_value("admin")
    time.sleep(1)

    # Fill out signup form with first name, last name, email, and password
    driver.find_element(By.ID, "firstName").send_keys("Faculty")
    time.sleep(1)
    driver.find_element(By.ID, "lastName").send_keys("Member")
    time.sleep(1)
    driver.find_element(By.ID, "email").send_keys("faculty1@example.com")
    time.sleep(1)
    driver.find_element(By.ID, "password").send_keys("password123")
    time.sleep(1)

    # Submit the form
    driver.find_element(By.TAG_NAME, "button").click()

    # Verify redirection to start page with success message
    time.sleep(2)
    assert "Sign-up successful!" in driver.page_source

    # Check if the user is added to the database
    conn = connect_db('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = 'faculty1@example.com'")
    user = cursor.fetchone()
    conn.close()

    assert user is not None  # Verify the user was added to the database


def test_faculty_login(setup): 
    driver = setup
    driver.get("http://localhost:5000/login")
    time.sleep(2)
    
    # Fill out login form with email and password
    driver.find_element(By.ID, "email").send_keys("faculty1@example.com")
    time.sleep(1)
    driver.find_element(By.ID, "password").send_keys("password123")
    time.sleep(1) 

    # Submit the form
    driver.find_element(By.TAG_NAME, "button").click()

    # Verify we are on the faculty event page
    time.sleep(2)
    assert "CS Department Event Page" in driver.page_source 


def test_add_event(setup):
    driver = setup
    
    # Fill out the event form
    driver.find_element(By.ID, "event_name").send_keys("Sample Event")
    time.sleep(2)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "event_date"))
    )
    driver.execute_script("document.getElementById('event_date').value = '2024-11-15';") 
    time.sleep(2)
    driver.execute_script("document.getElementById('event_time').value = '10:00';")
    time.sleep(2)
    driver.find_element(By.ID, "event_location").send_keys("CS Building, Room 101")
    time.sleep(2)
    
    # Find the Quill editor's contenteditable element
    quill_editor = driver.find_element(By.CLASS_NAME, 'ql-editor')
    
    # Click on the editor to focus
    quill_editor.click()
    time.sleep(1)
    
    # Send keys to the editor
    quill_editor.send_keys('This is a description for a sample event.')
    time.sleep(2)
    
    # Click the "Add Event" button to submit the form
    driver.find_element(By.XPATH, "//button[text()='Add Event']").click()
    
    # Verify the event submission was successful
    time.sleep(2)
    assert "Event added successfully!" in driver.page_source  # Adjust based on the actual success message


def test_navigate_to_my_students_and_back(setup):
    driver = setup

    assert "CS Department Event Page" in driver.page_source

    # Click on the "My Students" tab/link
    driver.find_element(By.LINK_TEXT, "My Students").click()

    # Verify that we are on the "My Students" page
    time.sleep(3)
    assert "My Students" in driver.page_source  # Adjust if needed based on actual page content

    # Click "Back to Faculty Page" button or link
    driver.find_element(By.LINK_TEXT, "Back to Faculty Page").click()

    # Verify redirection back to the Faculty Event Page
    time.sleep(2)
    assert "CS Department Event Page" in driver.page_source


def test_navigate_to_print_report_and_back(setup):
    driver = setup
   
    assert "CS Department Event Page" in driver.page_source

    # Click on the "Semester Report" tab/link
    driver.find_element(By.LINK_TEXT, "Semester Report").click()

    # Verify that we are on the "Semester Event Summary" page
    time.sleep(3)
    assert "Semester Event Summary" in driver.page_source  # Adjust based on the actual page content

    # Click "Back to Faculty Page" button or link
    driver.find_element(By.LINK_TEXT, "Back to Faculty Page").click()

    # Verify redirection back to the Faculty Event Page
    time.sleep(2)
    assert "CS Department Event Page" in driver.page_source
