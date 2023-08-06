from PySide2 import QtWidgets, QtCore

from ciomax.components import widgets

LETTER_WIDTH = 7
LETTER_PAD = 35


class ModelBaseGrp(QtWidgets.QWidget):
    """
    Base class for  widget groups that use a model.
    """

    def __init__(self, **kwargs):
        super(ModelBaseGrp, self).__init__()

        self.model = None

        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        layout.addWidget(widgets.FormLabel(kwargs.get("label", "")))

        self.checkbox = widgets.add_checkbox(
            layout,
            kwargs.get("checkbox"),
            kwargs.get("check_label", "")
        )


class ComboBoxGrp(ModelBaseGrp):
    """Single combo box"""

    def __init__(self,  **kwargs):
        super(ComboBoxGrp, self).__init__(**kwargs)

        self.combobox = QtWidgets.QComboBox()
        self.layout().insertWidget(1, self.combobox)

    def set_by_text(self, text, column=0, default=0):
        for row in range(self.model.rowCount()):
            if self.model.item(row, column).text() == text:
                self.combobox.setCurrentIndex(row)
                return
        self.combobox.setCurrentIndex(default)

    def set_model(self, model):
        self.model = model
        self.combobox.setModel(self.model)


class InstanceTypeComboBoxGrp(ModelBaseGrp):
    """Combo box pair.

    The model is a tree of depth 2, and therefore the second combo box is
    maintained to always contain the children of the model item selected in the
    first combo box.
    """

    def __init__(self, **kwargs):
        super(InstanceTypeComboBoxGrp, self).__init__(**kwargs)

        self.combobox_category = QtWidgets.QComboBox()
        self.combobox_machine = QtWidgets.QComboBox()

        self.layout().insertWidget(1, self.combobox_category)
        self.layout().insertWidget(2, self.combobox_machine)

        self.combobox_category.currentIndexChanged.connect(self.root_changed)

    def set_model(self, model):
        """Set the model, """
        self.model = model
        self.combobox_category.setModel(self.model)
        self.combobox_machine.setModel(self.model)

        root_width = self.calc_root_width()
        self.combobox_category.setFixedWidth(root_width)

        model_index = self.model.index(0, 0)
        self.combobox_machine.setRootModelIndex(model_index)

        self.combobox_category.setCurrentIndex(0)
        self.combobox_machine.setCurrentIndex(0)

   
    def root_changed(self, index):

        if not self.model:
            return
        self.set_by_indices(index, 0)

    def set_by_indices(self, i, j):

        if not ((self.combobox_category.count() > i) and (self.combobox_machine.count() > j)):
            return
        self.combobox_category.setCurrentIndex(i)
        model_index = self.model.index(i, 0)
        self.combobox_machine.setRootModelIndex(model_index)
        self.combobox_machine.setCurrentIndex(j)

    def set_by_text(self, text, column=0, default=(0, 0)):
        if not self.model:
            return
        for root_row in range(self.model.rowCount()):
            root_item = self.model.item(root_row)
            for row in range(root_item.rowCount()):
                if root_item.child(row, column).text() == text:
                    self.set_by_indices(root_row, row)
                    return

        self.set_by_indices(default[0], default[1])

    def calc_root_width(self):
        letters = 0
        for row in range(self.model.rowCount()):
            curr_letters = len(self.model.item(row).text())
            if curr_letters > letters:
                letters = curr_letters
        return (letters * LETTER_WIDTH) + LETTER_PAD

    def get_item_name(self, long_name):
        for root_row in range(self.model.rowCount()):
            root_item = self.model.item(root_row)
            for row in range(root_item.rowCount()):
                if root_item.child(row, 0).text() == long_name:
                    return root_item.child(row, 1).text()
 