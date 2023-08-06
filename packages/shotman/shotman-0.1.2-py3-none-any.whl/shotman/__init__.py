import logging
import os
import subprocess
import sys

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication

logger = logging.getLogger(__name__)


# Examples on actions and keyboard shortcuts: https://stackoverflow.com/q/59346440


class Spacer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Preferred,
        )


class DoneAction(QtGui.QAction):
    def __init__(self, parent):
        super().__init__("Done", parent=parent)
        self.setShortcuts(
            [
                QtGui.QKeySequence.Quit,
                QtGui.QKeySequence.Save,
                QtGui.QKeySequence.Close,
                QtGui.QKeySequence(QtCore.Qt.Key_Q)
            ]
        )
        # TODO: Exit with `q` and `ctrl+s`.


class DeleteAction(QtGui.QAction):
    def __init__(self, parent):
        # icon = QtGui.QIcon.fromTheme("user-trash")
        icon = QtGui.QIcon("./trash-alt.svg")
        super().__init__(icon, "&Delete", parent=parent)
        self.setShortcuts(
            [
                QtGui.QKeySequence.Delete,
                QtGui.QKeySequence.Cancel,
                QtGui.QKeySequence(QtCore.Qt.Key_D)
            ]
        )


class CopyAction(QtGui.QAction):
    def __init__(self, parent):
        # icon = QtGui.QIcon.fromTheme("edit-copy")
        icon = QtGui.QPixmap("./copy.svg")
        super().__init__(icon, "&Copy", parent=parent)
        self.setShortcuts(QtGui.QKeySequence.Copy)


class Toolbar(QtWidgets.QToolBar):
    """The toolbar shown at the top with three actions."""

    def __init__(self, parent):
        super().__init__(parent)
        self.done_action = DoneAction(self)
        self.delete_action = DeleteAction(self)
        self.copy_action = CopyAction(self)

        self.addAction(self.done_action)
        self.addWidget(Spacer())
        self.addAction(self.delete_action)
        self.addAction(self.copy_action)


class MainWindow(QtWidgets.QDialog):
    def __init__(self, app, filename):
        super().__init__()
        self._app = app
        self._filename = filename

        self.setWindowTitle("shotman")

        self.image = QtGui.QImage(filename)
        pixmap = QtGui.QPixmap(self.image)
        width = pixmap.width() * 0.20
        height = pixmap.height() * 0.20

        # XXX: handling resizing?: https://stackoverflow.com/a/8212120 ?
        # Might be nice someday have zoom-on-click, and have preview grow.
        image_label = QtWidgets.QLabel(self)
        image_label.setFixedWidth(width)
        image_label.setFixedHeight(height)
        image_label.setPixmap(
            pixmap.scaled(
                image_label.size(),
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation,
            )
        )

        toolbar = Toolbar(self)
        toolbar.done_action.triggered.connect(self.on_done)
        toolbar.delete_action.triggered.connect(self.on_delete)
        toolbar.copy_action.triggered.connect(self.on_copy)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)  # No outer margins.
        self.layout.setSpacing(0)  # No space between components.
        self.layout.addWidget(toolbar)
        self.layout.addWidget(image_label)
        self.setLayout(self.layout)

        # Force the window to be a floating one:
        # FIXME: This magic 8 doesn't make sense. There's no spacing or margins,
        # so the sum of these two should match perfectly. However, it doesn't.
        self.setFixedSize(width, height + toolbar.height() + 8)

    @Slot()
    def on_done(self):
        self._app.exit()

    @Slot()
    def on_delete(self):
        os.unlink(self._filename)
        logger.info(f"Deleted {self._filename}.")
        self._app.exit()

    @Slot()
    def on_copy(self):
        clipboard = self._app.clipboard()
        clipboard.setImage(self.image)
        logger.info("Image copied to clipboard")
        # TODO: linger until we lose clipboard


def run():
    if len(sys.argv) != 2:
        logger.error("Bad usage.")
        sys.exit(1)

    shot_type = sys.argv[1]
    if shot_type not in ["active", "screen", "output", "area", "window"]:
        logger.error(f"Bad param: {shot_type}")
        sys.exit(2)

    grimshot = subprocess.run(["grimshot", "save", shot_type], capture_output=True)
    if grimshot.returncode:
        logger.error("Grimshot failed!")
        sys.exit(3)

    filename = grimshot.stdout.decode().strip()
    logger.info(f"Screenshot file is {filename}.")

    app = QApplication(sys.argv)
    widget = MainWindow(app, filename)
    widget.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
