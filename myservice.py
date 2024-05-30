import win32serviceutil
import win32service
import win32event
import servicemanager
import subprocess
import logging

logging.basicConfig(
    filename='C:\\path\\to\\log\\myservice.log',  # Update this path to a valid location
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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
        logging.info("Service stopped")

    def SvcDoRun(self):
        logging.info("Service started")
        self.main()

    def main(self):
        logging.info("Running main process")
        self.process = subprocess.Popen(['python', 'monitor_redirect.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        self.process.wait()

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(MyService)
