from PySide2 import QtWidgets
from ciomax.collapsible_section import CollapsibleSection


class ExtraAssetsSection(CollapsibleSection):
    ORDER = 65

    def __init__(self,dialog):
        super(ExtraAssetsSection, self).__init__(dialog,"Extra Assets")

        # Buttons
        self.button_layout = QtWidgets.QHBoxLayout()

        for button in [
            {"label": "Clear", "func": self.clear},
            {"label": "Remove selected", "func": self.remove_selected},
            {"label": "Browse files", "func": self.browse_files},
            {"label": "Browse directory", "func": self.browse_dir},
        ]:

            btn = QtWidgets.QPushButton(button["label"])
            btn.clicked.connect(button["func"])
            self.button_layout.addWidget(btn)

        self.content_layout.addLayout(self.button_layout)

        # List
        self.list_component = QtWidgets.QListWidget()
        self.list_component.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_component.setFixedHeight(140)
        self.content_layout.addWidget(self.list_component)

    def clear(self):
        self.list_component.clear()

    def remove_selected(self):
        for row in sorted([index.row() for index in self.list_component.selectionModel().selectedIndexes()], reverse=True):
            self.list_component.model().removeRow(row)

    def browse_files(self):
        result = QtWidgets.QFileDialog.getOpenFileNames(
            parent=None, caption="Select files to upload")
        if len(result) and len(result[0]):
            self.list_component.addItems(result[0])

    def browse_dir(self):
        result = QtWidgets.QFileDialog.getExistingDirectory(
            parent=None, caption="Select a directory to upload")
        if result:
            self.list_component.addItem(result)

    def populate_from_store(self):
        for i in range(1, 4):
            self.list_component.addItem("/path/to/file.{:04d}.exr".format(i))

    # def resolve(self):
    #     pass
