from PySide2 import QtCore, QtWidgets

from ciomax.collapsible_section import CollapsibleSection
from ciomax.components.text_field_grp import TextFieldGrp
from ciomax.components.checkbox_grp import CheckboxGrp

from ciomax.components.int_field_grp import IntFieldGrp


class AdvancedSection(CollapsibleSection):
    ORDER = 100

    def __init__(self, dialog):
        super(AdvancedSection, self).__init__(dialog, "Advanced")

        self.autosave_component = TextFieldGrp(
            label="Autosave",
            checkbox=True,
            check_label="Clean up",
            hidable=True)
        self.content_layout.addWidget(self.autosave_component)

        self.task_template_component = TextFieldGrp(
            label="Task template",
            enablable=True)
        self.content_layout.addWidget(self.task_template_component)

        self.retry_preempted_component = IntFieldGrp(
            label="Preempted retries", default=1, minimum=0)
        self.content_layout.addWidget(self.retry_preempted_component)

        self.notification_component = TextFieldGrp(
            label="Send Notifications",
            enablable=True)
        self.content_layout.addWidget(self.notification_component)

        self.location_component = TextFieldGrp(
            label="Location tag")
        self.content_layout.addWidget(self.location_component)

        upload_options_component = CheckboxGrp(
            checkboxes=2,
            sublabels=["Use daemon", "Upload only"]
        )
        self.use_daemon_checkbox = upload_options_component.checkboxes[0]
        self.upload_only_checkbox = upload_options_component.checkboxes[1]
        self.content_layout.addWidget(upload_options_component)

        separator = QtWidgets.QFrame()
        separator.setLineWidth(1)
        separator.setFrameStyle(QtWidgets.QFrame.HLine |
                                QtWidgets.QFrame.Raised)
        self.content_layout.addWidget(separator)

        self.tracebacks_component = CheckboxGrp(label="Show tracebacks")
        self.content_layout.addWidget(self.tracebacks_component)

        self.use_fixtures_component = CheckboxGrp(label="Use fixtures")
        self.content_layout.addWidget(self.use_fixtures_component)

        self.use_daemon_checkbox.clicked.connect(self.enable_autosave_cleanup)
        self.autosave_component.checkbox.setEnabled(False)

    def enable_autosave_cleanup(self, checked):
        self.autosave_component.checkbox.setEnabled(not checked)

    def populate_from_store(self):

        self.task_template_component.field.setText(
            "3dsrender -s <start> -e <end> -b <step> -layer <layer> <Scenefile>")
        self.task_template_component.set_active(False)

        self.notification_component.set_active(False)
        self.notification_component.field.setText("joe@example.com")

        self.autosave_component.set_active(True)
        self.autosave_component.field.setText("<scenedir>/cio_<scenename>")

        self.use_fixtures_component.checkboxes[0].setChecked(True)

        self.use_daemon_checkbox.setCheckState(QtCore.Qt.Checked)
        self.upload_only_checkbox.setCheckState(QtCore.Qt.Unchecked)

    # def resolve(self):
    #     pass
