import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Read environment variables
browser = os.getenv('BROWSER', 'chrome')
hub_host = os.getenv('HUB_HOST', 'localhost')

capabilities = list()

# Initialize the WebDriver for Selenium Grid
if browser == 'chrome':
    capabilities.append(DesiredCapabilities.CHROME)
elif browser == 'firefox':
    capabilities.append(DesiredCapabilities.FIREFOX)

driver = webdriver.Remote(
    command_executor=f'http://{hub_host}:4444/wd/hub',
    options=capabilities
)

# URL of the login page
url = "http://webdriveruniversity.com/Login-Portal/index.html"

# Test data
valid_username = "webdriver"
valid_password = "webdriver123"
invalid_username = "invalid_user"
invalid_password = "invalid_password"


def login(username, password):
    driver.get(url)

    # Find the username, password input fields, and login button
    username_field = driver.find_element(By.ID, "text")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    # Enter username and password
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Click the login button
    login_button.click()

    # Wait for the alert to appear
    time.sleep(2)  # Adjust sleep time if necessary, or use WebDriverWait


def test_valid_login():
    login(valid_username, valid_password)

    # Handle alert for valid login
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        assert "validation succeeded" in alert_text.lower()
        alert.accept()
        print("Valid login test passed")
    except Exception as e:
        print("Valid login test failed:", e)


def test_invalid_login():
    login(invalid_username, invalid_password)

    # Handle alert for invalid login
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        assert "validation failed" in alert_text.lower()
        alert.accept()
        print("Invalid login test passed")
    except Exception as e:
        print("Invalid login test failed:", e)


# Run tests
test_valid_login()
test_invalid_login()

# Close the WebDriver
driver.quit()
