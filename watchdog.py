import subprocess
import time

def is_server_running():
    try:
        output = subprocess.check_output(['tasklist', '/FI', 'IMAGENAME eq python.exe'])
        return b'server.py' in output
    except subprocess.CalledProcessError:
        return False

def start_server():
    subprocess.Popen(['python', 'server.py'], creationflags=subprocess.CREATE_NEW_CONSOLE)

while True:
    if not is_server_running():
        start_server()
    time.sleep(10)
