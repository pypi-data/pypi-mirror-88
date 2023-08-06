from PySide2 import QtWidgets, QtCore


class FormLabel(QtWidgets.QLabel):

    def __init__(self, label, tooltip=None):
        super(FormLabel, self).__init__()

        self.setText(label)
        self.setFixedWidth(120)
        self.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        self.setIndent(5)

        if tooltip:
            self.setToolTip(tooltip)


def add_checkbox(layout, do_checkbox=True, label=""):
    if do_checkbox:
        checkbox = QtWidgets.QCheckBox(label)
        checkbox.setFixedWidth(80)
        layout.addWidget(checkbox)
        return checkbox
    else:
        layout.addSpacing(85)

