from PySide2 import QtWidgets, QtCore

from ciomax.components import widgets


class KeyValueHeaderGrp(QtWidgets.QWidget):

    def __init__(self, **kwargs):
        super(KeyValueHeaderGrp, self).__init__()

        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)
        self.add_button = QtWidgets.QPushButton("Add")
        self.add_button.setFixedWidth(40)

        self.key_header = QtWidgets.QPushButton(kwargs.get("key_label", "Key"))
        policy = self.key_header.sizePolicy()
        policy.setHorizontalStretch(2)
        self.key_header.setSizePolicy(policy)
        self.key_header.setEnabled(False)

        self.value_header = QtWidgets.QPushButton(
            kwargs.get("value_label", "Value"))
        policy = self.value_header.sizePolicy()
        policy.setHorizontalStretch(3)
        self.value_header.setSizePolicy(policy)
        self.value_header.setEnabled(False)

        layout.addWidget(self.add_button)
        layout.addWidget(self.key_header)
        layout.addWidget(self.value_header)

        if kwargs.get("checkbox_label") is not None:
            self.excl_header = QtWidgets.QPushButton(
                kwargs.get("checkbox_label", "Active"))
            self.excl_header.setFixedWidth(40)
            self.excl_header.setEnabled(False)
            layout.addWidget(self.excl_header)
        else:
            layout.addSpacing(45)


class KeyValuePairGrp(QtWidgets.QWidget):

    delete_pressed = QtCore.Signal(QtWidgets.QWidget)

    def __init__(self, do_checkbox):
        super(KeyValuePairGrp, self).__init__()

        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)
        self.delete_button = QtWidgets.QPushButton("X")
        self.delete_button.setFixedWidth(40)

        self.delete_button.clicked.connect(self.delete_me)

        self.key_field = QtWidgets.QLineEdit()
        policy = self.key_field.sizePolicy()
        policy.setHorizontalStretch(2)
        self.key_field.setSizePolicy(policy)
 
        self.value_field = QtWidgets.QLineEdit()
        policy = self.value_field.sizePolicy()
        policy.setHorizontalStretch(3)
        self.value_field.setSizePolicy(policy)


        layout.addWidget(self.delete_button)
        layout.addWidget(self.key_field)
        layout.addWidget(self.value_field)

        if do_checkbox:
            self.excl_checkbox = QtWidgets.QCheckBox()
            self.excl_checkbox.setFixedWidth(40)
            layout.addWidget(self.excl_checkbox)
        else:
            layout.addSpacing(45)

    def delete_me(self):
        self.delete_pressed.emit(self)


class KeyValueGrpList(QtWidgets.QWidget):

    def __init__(self, **kwargs):
        super(KeyValueGrpList, self).__init__()

        self.has_checkbox = kwargs.get("checkbox_label") is not None

        self.header_component = KeyValueHeaderGrp(**kwargs)
        self.content_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.content_layout)

        self.content_layout.addWidget(self.header_component)

        self.entries_component = QtWidgets.QWidget()
        self.entries_layout = QtWidgets.QVBoxLayout()
        self.entries_component.setLayout(self.entries_layout)
        self.content_layout.addWidget(self.entries_component)

        self.header_component.add_button.clicked.connect(self.add_row)

    def add_row(self):
        entry = KeyValuePairGrp(self.has_checkbox)
        self.entries_layout.addWidget(entry)
        entry.delete_pressed.connect(remove_widget)


@QtCore.Slot(QtWidgets.QWidget)
def remove_widget(widget):
    widget.layout().removeWidget(widget)
    widget.deleteLater()
