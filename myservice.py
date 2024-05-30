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
