import os
import time
from SztuSrunLogin.LoginManager import LoginManager


def is_connect_internet(testip):
    status = os.system("ping {} -c 8 > /dev/null 2>&1".format(testip))
    return status == 0


def always_login(username, password, testip, checkinterval):
    lm = LoginManager()
    login = lambda: lm.login(username=username, password=password)
    timestamp = lambda: print(time.asctime(time.localtime(time.time())))

    timestamp()
    try:
        login()
    except Exception:
        pass
    while 1:
        time.sleep(checkinterval)
        if not is_connect_internet(testip):
            timestamp()
            try:
                login()
            except Exception:
                pass


if __name__ == "__main__":
    user_id = os.getenv("USER_ID", "Your user id")
    password = os.getenv("PASSWORD", "Your password")
    checkinterval = os.getenv("CHECK_INTERVAL", 5 * 60)

    always_login(user_id, password, "114.114.114.114", int(checkinterval))
