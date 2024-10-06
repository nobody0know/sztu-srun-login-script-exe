import os
import sys
import time
import threading
from SztuSrunLogin.LoginManager import LoginManager
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw


def get_executable_path():
    """获取打包后可执行文件所在的目录"""
    if hasattr(sys, 'frozen'):
        # 打包后的情况，sys.executable 指向 .exe 文件
        return os.path.dirname(sys.executable)
    else:
        # 未打包情况下，返回当前脚本文件的路径
        return os.path.dirname(__file__)

# 读取txt文件的函数，获取用户名和密码
def read_credentials(file_path):
    # 获取程序所在文件夹路径
    exe_path = get_executable_path()
    # 将文件路径设为可执行文件所在目录中的文件
    file_path = os.path.join(exe_path, file_path)
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"错误: 找不到文件 {file_path}")
        sys.exit(1)  # 退出程序

    with open(file_path, 'r') as f:
        lines = f.readlines()
        if len(lines) < 2:
            print(f"错误: 文件 {file_path} 内容格式不正确")
            sys.exit(1)  # 退出程序

        user_id = lines[0].strip()  # 第一行是用户ID
        password = lines[1].strip()  # 第二行是密码

    return user_id, password

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
    while True:
        time.sleep(checkinterval)
        if not is_connect_internet(testip):
            timestamp()
            try:
                login()
            except Exception:
                pass

# 创建托盘图标
def create_image(width, height, color1, color2):
    # 创建一个空白图像
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        [width // 2, 0, width, height // 2],
        fill=color2)
    dc.rectangle(
        [0, height // 2, width // 2, height],
        fill=color2)
    return image

# 退出程序的回调
def quit_program(icon, item):
    icon.stop()
    sys.exit()

# 系统托盘启动函数
def setup_tray_icon():
    icon = Icon("LoginManager")

    # 创建托盘菜单
    menu = Menu(
        MenuItem('退出', quit_program)
    )

    # 创建图标
    icon.icon = create_image(64, 64, 'black', 'white')
    icon.menu = menu
    icon.run()

if __name__ == "__main__":
    # 假设 credentials.txt 文件在程序同一目录下
    credentials_file = "credentials.txt"

    # 读取用户ID和密码，如果文件不存在或者内容格式不正确则退出
    user_id, password = read_credentials(credentials_file)

    checkinterval = os.getenv("CHECK_INTERVAL", 5 * 60)

    # 使用线程在后台运行登录检查逻辑
    login_thread = threading.Thread(target=always_login, args=(user_id, password, "114.114.114.114", int(checkinterval)))
    login_thread.daemon = True
    login_thread.start()

    # 启动系统托盘图标
    setup_tray_icon()
