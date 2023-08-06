from PySide2 import QtWidgets, QtGui, QtCore

from ciomax.collapsible_section import CollapsibleSection
from ciomax.components.key_value_grp import KeyValueGrpList


class MetadataSection(CollapsibleSection):
    ORDER = 70

    def __init__(self,dialog):
        super(MetadataSection, self).__init__(dialog,"Metadata")

        self.kv_widget = KeyValueGrpList()
        self.content_layout.addWidget(self.kv_widget)

    def populate_from_store(self):
        pass

    # def resolve(self, expander):
    #     pass
