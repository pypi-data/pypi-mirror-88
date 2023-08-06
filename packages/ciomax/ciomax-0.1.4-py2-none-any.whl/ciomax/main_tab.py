import sys
import os

from PySide2 import QtWidgets, QtCore, QtGui
from ciocore.expander import Expander

from ciomax.collapsible_section import CollapsibleSection

from ciomax.general_section import GeneralSection
from ciomax.software_section import SoftwareSection
from ciomax.frames_section import FramesSection
from ciomax.info_section import InfoSection
from ciomax.environment_section import EnvironmentSection
from ciomax.metadata_section import MetadataSection
from ciomax.extra_assets_section import ExtraAssetsSection
from ciomax.advanced_section import AdvancedSection
from ciocore import data as coredata
# from ciomax.store import ConductorStore

from ciocore.gpath import Path

FIXTURES_DIR = os.path.expanduser(os.path.join("~", "Conductor", "fixtures"))


class MainTab(QtWidgets.QScrollArea):
    """
    Build the tab that contains the main configuration sections.
    """

    def __init__(self, dialog):
        super(MainTab, self).__init__()

        self.dialog = dialog
        coredata.init(product="maya-io")
        coredata.set_fixtures_dir(FIXTURES_DIR)
        coredata.data()

        widget = QtWidgets.QWidget()
        self.setWidget(widget)
        self.setWidgetResizable(1)

        sections_layout = QtWidgets.QVBoxLayout()
        widget.setLayout(sections_layout)

        self._section_classes = sorted(
            CollapsibleSection.__subclasses__(), key=lambda x: x.ORDER)
        self.sections = [cls(self.dialog) for cls in self._section_classes]

        for section in self.sections:
            sections_layout.addWidget(section)

        sections_layout.addStretch()

    def populate_from_store(self):
        for section in self.sections:
            section.populate_from_store()

    def section(self, classname):
        """
        Convenience to find sections by name.

        Makes it easier to allow sections to talk to each other.
        Example: Calculate info from stuff in the frames section
            self.section("InfoSection").calculate(self.section("FramesSection"))

        """

        return next(s for s in self.sections if s.__class__.__name__ == classname)

    def resolve(self, **kwargs):
        submission = {}
        context = self.get_context()
        expander = Expander(safe=True, **context)
        for section in self.sections:
            submission.update(section.resolve(expander, **kwargs))
        return submission

    def get_context(self):
        scenefile = "/get/doc/name.3ds"
        if scenefile:
            scenefile = Path(scenefile).posix_path(with_drive=False)
        scenedir = os.path.dirname(scenefile)
        scenenamex, ext = os.path.splitext(os.path.basename(scenefile))

        result = {
            "scenefile": scenefile,
            "scenedir": scenedir,
            "scenenamex": scenenamex,
            "ext": ext
        }
        return result
