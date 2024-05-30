import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Replace this path with the path to your WebDriver executable
driver_path = 'path/to/your/webdriver'

options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(executable_path=driver_path, options=options)

try:
    # Open the password-protected page
    driver.get('http://localhost:5000')

    # Simulate waiting for the user to watch GIFs and enter password
    time.sleep(30)

    # In a real scenario, you would interact with the page to check the password and download the file
    # Here, just simulate some interaction
    password_input = driver.find_element_by_id('password')
    password_input.send_keys('password123')
    password_input.send_keys(Keys.RETURN)

    # Wait for the file to download (adjust the time as necessary)
    time.sleep(5)

finally:
    driver.quit()
