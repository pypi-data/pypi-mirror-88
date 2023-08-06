import sys
from pathlib import Path

import pylnk3
from mutagen import mp3

from mp3monitoring.gui import pkg_data


def is_mp3(file_path: Path):
    """
    Return true if a file is an mp3.
    :param file_path: file to be checked
    """
    try:
        return not mp3.MP3(str(file_path)).info.sketchy
    except mp3.HeaderNotFoundError:
        pass
    except FileNotFoundError:
        pass
    return False


def create_start_menu_entry():
    start_menu_dir = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs"
    start_menu_entry = start_menu_dir / "MP3 Monitoring.lnk"

    if not start_menu_dir.is_dir():
        return False, "Could not find start menu directory.\nPlease report this error."

    exe = Path(sys.executable).with_stem("pythonw")
    try:
        pylnk3.for_file(str(exe.absolute()), lnk_name=str(start_menu_entry), icon_file=str(pkg_data.LOGO_ICO), arguments="-m mp3monitoring --gui")
    except Exception as ex:
        return False, str(ex)
    return True, ""


def edit_startup_link(create: bool = True) -> (bool, str):
    """

    :param create: Create or remove the link.
    :return: Success and error message.
    """
    startup_dir = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    startup_file = startup_dir / "MP3 Monitoring.lnk"

    if not create:
        try:
            startup_file.unlink()
        except FileNotFoundError:
            return True, ""
        except PermissionError:
            return False, "Could not remove the Startup entry, due to permission error."
        return True, ""

    startup_dir.mkdir(exist_ok=True)
    if create and not startup_dir.is_dir():
        return False, "Could not find startup directory.\nPlease report this error."

    exe = Path(sys.executable).with_stem("pythonw")
    try:
        pylnk3.for_file(str(exe.absolute()), lnk_name=str(startup_file), icon_file=str(pkg_data.LOGO_ICO), arguments="-m mp3monitoring --gui")
    except Exception as ex:
        return False, str(ex)
    return True, ""
