import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# URLs to redirect
urls_to_redirect = ["https://www.instagram.com", "https://discord.com"]

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")

# Initialize WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

try:
    while True:
        for url in urls_to_redirect:
            if any(url in tab.get('url') for tab in driver.window_handles):
                driver.execute_script(f"window.location.href = 'http://localhost:5000';")
        time.sleep(5)  # Check every 5 seconds
finally:
    driver.quit()
