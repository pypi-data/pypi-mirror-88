from PySide2 import QtWidgets, QtGui, QtCore

from ciomax.collapsible_section import CollapsibleSection
from ciomax.components.key_value_grp import KeyValueGrpList


class EnvironmentSection(CollapsibleSection):
    ORDER = 60

    def __init__(self,dialog):
        super(EnvironmentSection, self).__init__(dialog,"Extra Environment")

        self.kv_widget = KeyValueGrpList(
            checkbox_label="Excl",
            key_label="Name"
        )
        self.content_layout.addWidget(self.kv_widget)

    def populate_from_store(self):
        pass

    # def resolve(self):
    #     pass
