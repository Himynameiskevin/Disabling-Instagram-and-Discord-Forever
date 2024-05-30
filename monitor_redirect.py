import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(level=logging.INFO)

# URLs to redirect
urls_to_redirect = ["https://www.instagram.com", "https://discord.com"]

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")

# Initialize WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

try:
    while True:
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            current_url = driver.current_url
            for url in urls_to_redirect:
                if url in current_url:
                    logging.info(f"Redirecting {current_url} to http://localhost:5000")
                    driver.get('http://localhost:5000')
        time.sleep(5)  # Check every 5 seconds
finally:
    driver.quit()
