# test_signup_login.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pytest
import time
from test_db import connect_db  # From your test_tb.py

#to run these tests first start your virtual enviroment 
#install selenium and pytest in your virtual enviroment created for this project 
#pip install selenium pytest 
#start flask by typing flask --app flask_intro run --debug
#then pytest test_signup_login.py will start the tests

@pytest.fixture(scope="module")
def setup():
    # Setup Selenium WebDriver (Chrome in this case, make sure chromedriver is installed)
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
    
    # Click the "SignUp" button on the start page using the button's form action
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

    # Verify redirection to start page
    time.sleep(2)


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

    # Click on the "My Activities" tab/link
    driver.find_element(By.LINK_TEXT, "My Activities").click()

    # Verify that we are on the "My Activities" page
    time.sleep(2)
    assert "Activity Summary" in driver.page_source  # Adjust based on the actual page content

def test_back_to_dashboard_from_activities(setup):
    driver = setup

    # Click on "Back to Dashboard"
    driver.find_element(By.LINK_TEXT, "Back to Dashboard").click()  # Ensure this matches the button's link text

    # Verify redirection back to the Student Dashboard
    time.sleep(2)
    assert "CS Department Event Page: Student" in driver.page_source 


def test_faculty_signup(setup):
    driver = setup
    driver.get("http://localhost:5000")
    
    # Wait for the start page to load
    time.sleep(2)
    
    # Click the "SignUp" button on the start page using the button's form action
    driver.find_element(By.XPATH, "//form[@action='/signup']/button").click()
    
    # Wait for the signup page to load
    time.sleep(2)
    
    # Select 'Faculty' role (the value is 'admin' in the HTML)
    role_dropdown = Select(driver.find_element(By.ID, "role"))
    role_dropdown.select_by_value("admin")  # Correct value for faculty is 'admin'
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

    # Verify redirection to start page
    time.sleep(2)
    assert "Xavier University Events" in driver.page_source

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

    assert "CS Department Event Page" in driver.page_source
    
    # Fill out the event form
    driver.find_element(By.ID, "event_name").send_keys("Sample Event")
    time.sleep(2)
    driver.find_element(By.ID, "event_date").send_keys("2024-11-15")  # Format as YYYY-MM-DD
    time.sleep(2)
    driver.find_element(By.ID, "event_description").send_keys("This is a description for a sample event.")
    time.sleep(2)
    driver.find_element(By.ID, "event_location").send_keys("CS Building, Room 101")
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
    driver.find_element(By.LINK_TEXT, "Back to Faculty Page").click()  # Ensure this text matches the actual link

    # Verify redirection back to the Faculty Event Page
    time.sleep(2)
    assert "CS Department Event Page" in driver.page_source


def test_navigate_to_print_report_and_back(setup):
    driver = setup
   
    assert "CS Department Event Page" in driver.page_source

    # Click on the "Print Report" tab/link
    driver.find_element(By.LINK_TEXT, "Print Report").click()

    # Verify that we are on the "Print Report" page
    time.sleep(3)
    assert "Print Event Reports" in driver.page_source  # Adjust based on actual page content

    # Click "Back to Faculty Page" button or link
    driver.find_element(By.LINK_TEXT, "Back to Faculty Page").click()  # Ensure this text matches the actual link

    # Verify redirection back to the Faculty Event Page
    time.sleep(2)
    assert "CS Department Event Page" in driver.page_source










