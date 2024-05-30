import os
import subprocess
import sys

def install_packages():
    packages = ['selenium', 'flask', 'pywin32', 'webdriver-manager']
    for package in packages:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def setup_files():
    if not os.path.exists('server.py'):
        with open('server.py', 'w') as f:
            f.write("""\
from flask import Flask, redirect

app = Flask(__name__)

@app.route('/')
def home():
    return redirect("https://nkevi.com/haha", code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
""")

    if not os.path.exists('monitor_redirect.py'):
        with open('monitor_redirect.py', 'w') as f:
            f.write("""\
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
""")

    if not os.path.exists('myservice.py'):
        with open('myservice.py', 'w') as f:
            f.write("""\
import win32serviceutil
import win32service
import win32event
import servicemanager
import subprocess
import os

class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "URLRedirectService"
    _svc_display_name_ = "URL Redirect Service"
    _svc_description_ = "Redirects specific URLs to a custom page"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.process = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        if self.process:
            self.process.terminate()
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        self.process = subprocess.Popen(['python', 'monitor_redirect.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        self.process.wait()

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(MyService)
""")

def create_service():
    subprocess.check_call([sys.executable, 'myservice.py', 'install'])
    subprocess.check_call([sys.executable, 'myservice.py', 'start'])

if __name__ == '__main__':
    install_packages()
    setup_files()
    create_service()
    print("Setup complete. The server and URL monitor should now be running as a service.")
