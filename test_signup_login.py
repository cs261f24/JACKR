# test_signup_login.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pytest
import time
from test_db import connect_db  # From your test_tb.py


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
    
    # Wait for the start page to load
    time.sleep(2)
    
    # Click the "SignUp" button on the start page using the button's form action
    driver.find_element(By.XPATH, "//form[@action='/signup']/button").click()
    
    # Wait for the signup page to load
    time.sleep(2)
    
    # Select 'Student' role
    role_dropdown = Select(driver.find_element(By.ID, "role"))
    role_dropdown.select_by_value("student")

    # Fill out signup form
    driver.find_element(By.ID, "email").send_keys("student1@example.com")
    time.sleep(1)
    driver.find_element(By.ID, "username").send_keys("student1")
    time.sleep(1)
    driver.find_element(By.ID, "password").send_keys("password123")
    time.sleep(1)

    # Submit the form
    driver.find_element(By.TAG_NAME, "button").click()

    # Wait for the next page to load
    time.sleep(2)

    # Verify redirection to start page
    assert "Xavier University Events" in driver.page_source

    # Check if the user is added to the database
    conn = connect_db('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = 'student1'")
    user = cursor.fetchone()
    conn.close()

    assert user is not None  # Verify the user was added to the database


def test_student_login(setup):
    driver = setup
    driver.get("http://localhost:5000/login")
    
    # Wait for the page to load
    time.sleep(2)

    # Select 'Student' role
    role_dropdown = Select(driver.find_element(By.ID, "role"))
    role_dropdown.select_by_value("student")

    # Fill out login form
    driver.find_element(By.ID, "username").send_keys("student1")
    time.sleep(1)
    driver.find_element(By.ID, "password").send_keys("password123")
    time.sleep(1)

    # Submit the form
    driver.find_element(By.TAG_NAME, "button").click()

    # Wait for the next page to load
    time.sleep(2)

    # Check if we are on the student event page
    page_source = driver.page_source
    assert "CS Department Event Page: Student" in page_source, f"Actual page content: {page_source}"


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

    # Fill out signup form
    driver.find_element(By.ID, "email").send_keys("faculty1@example.com")
    time.sleep(1)
    driver.find_element(By.ID, "username").send_keys("faculty1")
    time.sleep(1)
    driver.find_element(By.ID, "password").send_keys("password123")
    time.sleep(1)

    # Submit the form
    driver.find_element(By.TAG_NAME, "button").click()

    # Wait for the next page to load
    time.sleep(2)

    # Verify redirection to start page
    assert "Xavier University Events" in driver.page_source

    # Check if the user is added to the database
    conn = connect_db('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = 'faculty1'")
    user = cursor.fetchone()
    conn.close()

    assert user is not None  # Verify the user was added to the database


def test_faculty_login(setup):
    driver = setup
    driver.get("http://localhost:5000/login")
    
    # Wait for the page to load
    time.sleep(2)

    # Select 'Faculty' role (the value is 'admin' in the HTML)
    role_dropdown = Select(driver.find_element(By.ID, "role"))
    role_dropdown.select_by_value("admin")  # Correct value for faculty is 'admin'

    # Fill out login form
    driver.find_element(By.ID, "username").send_keys("faculty1")
    time.sleep(1)
    driver.find_element(By.ID, "password").send_keys("password123")
    time.sleep(1)

    # Submit the form
    driver.find_element(By.TAG_NAME, "button").click()

    # Wait for the next page to load
    time.sleep(2)

    # Check if we are on the faculty event page (update this based on the actual content)
    page_source = driver.page_source
    assert "CS Department Event Page" in page_source, f"Actual page content: {page_source}"
