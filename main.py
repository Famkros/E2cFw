#new code
import urequests
import os
import machine
from time import sleep

OTA_URL = "http://your-server.com/main.py"  # đổi link này

def ota_update():
    try:
        msg("OTA", ["Connecting..."])

        r = urequests.get(OTA_URL)

        if r.status_code != 200:
            msg("OTA FAIL", ["HTTP", str(r.status_code)])
            return

        msg("OTA", ["Downloading..."])

        # ghi vào file tạm trước
        with open("main_new.py", "w") as f:
            while True:
                chunk = r.raw.read(512)
                if not chunk:
                    break
                f.write(chunk)

        r.close()

        msg("OTA", ["Verifying..."])

        # check file có tồn tại + không rỗng
        if "main_new.py" not in os.listdir():
            msg("OTA FAIL", ["No file"])
            return

        if os.stat("main_new.py")[6] < 100:
            msg("OTA FAIL", ["Too small"])
            return

        msg("OTA", ["Installing..."])

        # backup file cũ
        try:
            os.rename("main.py", "main_backup.py")
        except:
            pass

        # replace file
        os.rename("main_new.py", "main.py")

        msg("OTA", ["Done!", "Rebooting..."])
        sleep(1)

        machine.reset()

    except Exception as e:
        msg("OTA ERR", [str(e)])