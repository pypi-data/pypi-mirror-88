import sys
import os

from PySide2 import QtWidgets, QtCore, QtGui
import qtmax
from pymxs import runtime as rt

# DO NOT SORT IMPORTS
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# While in development, we reload classes when this file is executed.
from ciomax import reloader
reload(reloader)


from ciomax.store import ConductorStore
from ciomax.main_tab import MainTab
from ciomax.preview_tab import PreviewTab

BACKGROUND_COLOR = "rgb(48, 48, 48)"
STYLESHEET = """
QLineEdit {{ background: {bg}; }}
QSpinBox {{ background: {bg}; }}
QListWidget {{ background: {bg}; }}
QToolButton {{ border: none; }}
QTextEdit {{ background: {bg}; }}""".format(bg=BACKGROUND_COLOR)

class ConductorDialog(QtWidgets.QDialog):
    """
    Build the dialog as a child of the Max window.

    We build a tab layout, and the first tab contains the main controls.
    """

    def __init__(self):
        QtWidgets.QDialog.__init__(
            self, QtWidgets.QWidget.find(rt.windows.getMAXHWND()))
        self.setStyleSheet(STYLESHEET)
        self.store = ConductorStore()
        self.setWindowTitle("Conductor")
        self.layout = QtWidgets.QVBoxLayout()
        self.tab_widget = QtWidgets.QTabWidget()

        self.button_row = QtWidgets.QWidget()
        button_row_layout = QtWidgets.QHBoxLayout()
        self.button_row.setLayout(button_row_layout)

        button_row_layout.addWidget(QtWidgets.QPushButton("Close"))
        button_row_layout.addWidget(QtWidgets.QPushButton("Validate"))
        button_row_layout.addWidget(QtWidgets.QPushButton("Submit"))

        self.setLayout(self.layout)
        self.layout.addWidget(self.tab_widget)
        self.layout.addWidget(self.button_row)

        self.main_tab = MainTab(self)
        self.preview_tab = PreviewTab(self)

        self.tab_widget.addTab(self.main_tab, "Configure")
        self.tab_widget.addTab(self.preview_tab, "Preview")

        self.main_tab.populate_from_store()


def main():

    dlg = ConductorDialog()
    dlg.resize(600, 800)

    # exec_() causes the window to be modal. This means we don't have to manage
    # any communication between max and the dialog like changes to the frame
    # range, while the dialog is open.
    dlg.exec_()


if __name__ == '__main__':
    main()
