import sys
import sysconfig
from pathlib import Path

from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QDialog

from mp3monitoring import static_data
from mp3monitoring.gui import pkg_data
from mp3monitoring.gui.dialog import show
from mp3monitoring.gui.ui.about_dialog import Ui_AboutDialog
from mp3monitoring.gui.updater import UpdateCheckThread, UpdateAppThread


class AboutDialog(QDialog, Ui_AboutDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~(Qt.WindowContextHelpButtonHint | Qt.MSWindowsFixedSizeDialogHint))

        # set descriptions
        self.version.setText(static_data.VERSION)
        self.author.setText(f"<a href=\"{static_data.AUTHOR_GITHUB}\">{static_data.AUTHOR}</a>")
        self.license.setText("<a href=\"https://github.com/IceflowRE/mp3monitoring/blob/main/LICENSE.md\">GPLv3</a>")
        self.website.setText(f"<a href=\"{static_data.PROJECT_URL}\">Github</a>")

        # set logo
        self.logo.setPixmap(QIcon(str(pkg_data.LOGO)).pixmap(QSize(250, 250)))

        self._update_app_runner = UpdateAppThread()
        self._update_app_runner.finished.connect(self.update_app_check)
        self.update_now.clicked.connect(self.update_app)
        self.update_now.hide()

        self.update_status.setPixmap(QIcon(str(pkg_data.WAIT_SYMBOL)).pixmap(QSize(self.update_info.height() * 0.8, self.update_info.height() * 0.8)))
        self._update_check_runner = UpdateCheckThread()
        self._update_check_runner.finished.connect(self.change_update_check)
        self._update_check_runner.start()

    def update_app(self):
        self.update_now.setDisabled(True)
        self._update_app_runner.start()

    def update_app_check(self):
        if not self._update_app_runner.succeed:
            show.information_dialog("Failed to update", self._update_app_runner.err_msg)
            return
        self.update_info.setText("Restart to finish the update.")
        show.information_dialog("Update succeed", "Restart the app to finish the update.")

    def change_update_check(self):
        if not self._update_check_runner.check_succeed:
            self.update_status.setPixmap(QIcon(str(pkg_data.ERROR_SYMBOL)).pixmap(QSize(self.update_info.height() * 0.8, self.update_info.height() * 0.8)))
            self.update_info.setText(self._update_check_runner.err_msg)
            return
        if self._update_check_runner.update_available:
            self.update_status.setPixmap(QIcon(str(pkg_data.WARNING_SYMBOL)).pixmap(QSize(self.update_info.height() * 0.8, self.update_info.height() * 0.8)))
            self.update_info.setText("An Update is available.")
            # executed in a top-level script environment e.g. pythonw -m mp3monitoring --gui, ONLY then we can update, otherwise the executable is locked
            if Path(sys.modules['__main__'].__file__) == Path(sysconfig.get_paths()['purelib']) / "mp3monitoring" / "__main__.py":
                self.update_now.show()
        else:
            self.update_status.setPixmap(QIcon(str(pkg_data.OK_SYMBOL)).pixmap(QSize(self.update_info.height() * 0.8, self.update_info.height() * 0.8)))
            self.update_info.setText("MP3 Monitoring is up to date.")
            self.update_now.hide()
