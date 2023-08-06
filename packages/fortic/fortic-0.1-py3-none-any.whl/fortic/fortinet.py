import logging
import os
import shutil
import subprocess


class FortiClient:

    def __init__(self, path):
        self.path = path
        self.bin = self.detect_binary()

    def connect(self, url, user, password):
        logging.info('Connecting to ' + url)
        proc = subprocess.Popen([self.bin, 'connect',
                                 '-h' + url,
                                 '-u' + user + ':' + password,
                                 '-m'])
        try:
            proc.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            # we need to detach
            pass

    def disconnect(self):
        subprocess.Popen([self.bin, 'disconnect'])
        logging.info('Disconnected')

    def detect_binary(self):
        executable = "FortiSSLVPNclient.exe"

        bin = None

        if self.path is not None:
            if os.path.isdir(self.path):
                bin = os.path.join(self.path, executable)
            elif os.path.isfile(self.path):
                bin = self.path

            if os.path.exists(bin):
                return bin
        else:
            bin = os.path.join("C:\\Program Files (x86)\\Fortinet\\SslvpnClient", executable)
            if os.path.exists(bin):
                return bin

            bin = os.path.join("C:\\Program Files\\Fortinet\\SslvpnClient", executable)
            if os.path.exists(bin):
                return bin

            # look in FORTISSLVPN_HOME
            env_path = os.environ.get('FORTISSLVPN_HOME')
            if env_path is not None:
                bin = os.path.join(env_path, executable)
                if os.path.exists(bin):
                    return bin

            # look in PATH
            bin = shutil.which(executable)
            if bin is not None:
                return bin

        raise Exception("Could not find " + executable)
