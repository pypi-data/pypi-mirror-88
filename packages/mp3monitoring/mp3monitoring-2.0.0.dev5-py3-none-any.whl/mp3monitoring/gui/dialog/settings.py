import platform

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog

from mp3monitoring import tools
from mp3monitoring.core.manager import Manager
from mp3monitoring.core.settings import Settings, save_config
from mp3monitoring.gui.dialog import show
from mp3monitoring.gui.ui.settings_dialog import Ui_SettingsDialog


class SettingsDialog(QDialog, Ui_SettingsDialog):
    def __init__(self, settings: Settings, manager: Manager, parent):
        super().__init__(parent)

        self._manager: Manager = manager
        self._settings: Settings = settings

        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & (~Qt.WindowContextHelpButtonHint | Qt.MSWindowsFixedSizeDialogHint))

        self.start_minimized.setChecked(self._settings.start_minimized)
        self.start_with_system.setChecked(self._settings.start_with_system)

        if platform.system() != "Windows":
            self.start_with_system.hide()
            self.start_with_system_l.hide()
            self.create_start_menu_entry.hide()

        self.create_start_menu_entry.clicked.connect(self.add_start_menu_entry)

        self.button_box.accepted.connect(self.apply)
        self.button_box.rejected.connect(self.cancel)

    def add_start_menu_entry(self):
        success, err = tools.create_start_menu_entry()
        if success:
            show.information_dialog("Success", "Start menu entry successful created.")
        else:
            show.information_dialog("Could not create a start menu entry", err)

    def apply(self):
        settings_changed = False

        if platform.system() == "Windows" and self._settings.start_with_system != self.start_with_system.isChecked():
            success, err = tools.edit_startup_link(self.start_with_system.isChecked())
            if success:
                self._settings.start_with_system = self.start_with_system.isChecked()
                settings_changed = True
            else:
                show.information_dialog("Settings change failed", err)

        if self._settings.start_minimized != self.start_minimized.isChecked():
            self._settings.start_minimized = self.start_minimized.isChecked()
            settings_changed = True
        if settings_changed:
            save_config(self._settings, self._manager.get_configurations())

        self.close()

    def cancel(self):
        self.close()
