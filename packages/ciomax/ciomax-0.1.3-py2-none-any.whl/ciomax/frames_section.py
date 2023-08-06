from PySide2 import QtWidgets, QtGui

from ciomax.collapsible_section import CollapsibleSection
from ciomax.components.text_field_grp import TextFieldGrp
from ciomax.components.int_field_grp import IntFieldGrp


class FramesSection(CollapsibleSection):
    ORDER = 30

    def __init__(self,dialog):
        super(FramesSection, self).__init__(dialog,"Frames", expanded=False)

        self.chunk_size_component = IntFieldGrp(
            label="Chunk size", default=1, minimum=1)
        self.custom_range_component = TextFieldGrp(
            label="Use custom range", hidable=True)
        self.scout_frames_component = TextFieldGrp(
            label="Use scout frames", enablable=True)

        self.content_layout.addWidget(self.chunk_size_component)
        self.content_layout.addWidget(self.custom_range_component)
        self.content_layout.addWidget(self.scout_frames_component)

    def populate_from_store(self):

        self.chunk_size_component.field.setValue(1)
        self.custom_range_component.set_active(False)
        self.custom_range_component.field.setText("1-10")
        self.scout_frames_component.field.setText("auto:3")
        self.scout_frames_component.set_active(True)

    # def resolve(self):
    #     pass
