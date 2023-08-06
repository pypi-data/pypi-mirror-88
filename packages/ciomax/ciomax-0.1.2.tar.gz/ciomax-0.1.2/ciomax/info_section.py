

from PySide2 import QtWidgets, QtGui

from ciomax.collapsible_section import CollapsibleSection
from ciomax.components.text_field_grp import TextFieldGrp


class InfoSection(CollapsibleSection):
    ORDER = 40

    def __init__(self,dialog):
        super(InfoSection, self).__init__(dialog,"Info", expanded=True)

        self.frame_info_component = TextFieldGrp(
            label="Frame info")
        self.scout_info_component = TextFieldGrp(
            label="Scout info")

        self.frame_info_component.field.setEnabled(False)
        self.scout_info_component.field.setEnabled(False)

        self.content_layout.addWidget(self.frame_info_component)
        self.content_layout.addWidget(self.scout_info_component)

        self.populate(
            "spec:101-200 --- tasks:100 --- frames:100",
            "spec:120-180x30 --- tasks:3 --- frames:3"
        )

    def populate(self, frame_info, scout_info):
        self.frame_info_component.field.setText(frame_info)
        self.scout_info_component.field.setText(scout_info)

    def resolve(self):
        pass
