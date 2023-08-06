from cryptography.fernet import Fernet
import base64
import platform
import getmac
import hashlib


class SystemId:

    def __init__(self):
        sep = ' - '
        self._system_id = platform.system() + sep + platform.node() + sep + getmac.get_mac_address() + \
            sep + platform.machine() + sep + platform.processor()
        self._b_system_id = self._system_id.encode()
        self._md5 = hashlib.md5(self._b_system_id)
        return

    def id(self):
        return self._md5.hexdigest()


class EncDec:

    def __init__(self):
        _systemid_key = SystemId().id().encode('ASCII')
        _key = base64.b64encode(_systemid_key)
        self._fernet = Fernet(_key)

    def encrypt(self, msg):
        return self._fernet.encrypt(msg.encode()).decode()

    def decrypt(self, msg):
        msg_bytes = msg.encode()
        return self._fernet.decrypt(msg_bytes).decode()


if __name__ == '__main__':
    ed = EncDec()
    msg = 'this is the message in clear text'
    encrypted = ed.encrypt(msg)
    decrypted = ed.decrypt(encrypted)
    print(encrypted)
    print(decrypted)