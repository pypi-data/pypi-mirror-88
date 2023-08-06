"""
Things needed for checking for updates.
"""
import json
import subprocess
import sys

import certifi
import urllib3
from PySide2.QtCore import QThread
from packaging.version import Version

from mp3monitoring import static_data


def get_newest_app_version() -> Version:
    """
    Download the version tag from remote.

    :return: version from remote
    """
    with urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where()) as p_man:
        pypi_json = p_man.urlopen('GET', static_data.PYPI_JSON_URL).data.decode('utf-8')
    releases = json.loads(pypi_json).get('releases', [])
    online_version = Version('0.0.0')
    for release in releases:
        cur_version = Version(release)
        if not cur_version.is_prerelease:
            online_version = max(online_version, cur_version)
    return online_version


def check_for_app_updates() -> bool:
    """
    Check for updates.

    :return: is update available
    """
    return get_newest_app_version() > Version(static_data.VERSION)


def update() -> (bool, str):
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'mp3monitoring'], stdout=sys.stdout, stderr=sys.stderr, check=True)
    except subprocess.CalledProcessError as ex:
        return False, ex.stdout
    return True, ""


class UpdateCheckThread(QThread):
    def __init__(self):
        super().__init__()
        self.check_succeed: bool = False
        self.update_available: bool = False
        self.err_msg: str = ""

    def run(self):
        try:
            self.update_available = check_for_app_updates()
            self.check_succeed = True
        except Exception:
            self.check_succeed = False
            self.err_msg = "Update check failed."


class UpdateAppThread(QThread):
    def __init__(self):
        super().__init__()
        self.succeed: bool = False
        self.err_msg: str = ""

    def run(self):
        self.succeed, self.err_msg = update()
