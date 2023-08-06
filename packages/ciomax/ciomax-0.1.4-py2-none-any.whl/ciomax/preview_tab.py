from PySide2 import QtWidgets, QtGui

JSON = """{
    "autoretry_policy": {
        "failed": {
            "max_retries": 1
        }, 
        "preempted": {
            "max_retries": 1
        }
    }, 
    "environment": {
        "ADSKFLEX_LICENSE_FILE": "@conductor_adlm", 
        "ARNOLD_PLUGIN_PATH": "/opt/solidangle/arnold-max/3/arnold-max-max2019-3.1.2-2./plug-ins:/opt/solidangle/arnold-max/3/arnold-max-max2019-3.1.2-2./shaders", 
        "AUTODESK_ADLM_THINCLIENT_ENV": "/opt/autodesk/max-io/2019/max-io2019.SP0/Conductor/AdlmThinClientCustomEnv.xml", 
        "LD_LIBRARY_PATH": "/opt/autodesk/max-io/2019/max-io2019.SP0/lib:/opt/autodesk/max-io/2019/max-io2019.SP0/plug-ins/xgen/lib:/opt/autodesk/max-io/2019/max-io2019.SP0/plug-ins/bifrost/lib", 
        "MAX_DEBUG_ENABLE_CRASH_REPORTING": "0", 
        "MAX_DEBUG_SIGTERM_AS_SIGINT": "1", 
        "MAX_DISABLE_CER": "1", 
        "MAX_DISABLE_CLIC_IPM": "1", 
        "MAX_LICENSE": "unlimited", 
        "MAX_LICENSE_METHOD": "network", 
        "MAX_LOCATION": "/opt/autodesk/max-io/2019/max-io2019.SP0", 
        "MAX_PLUG_IN_PATH": "/opt/solidangle/arnold-max/3/arnold-max-max2019-3.1.2-2./plug-ins", 
        "MAX_RENDER_DESC_PATH": "/opt/solidangle/arnold-max/3/arnold-max-max2019-3.1.2-2.", 
        "MAX_SCRIPT_PATH": "/opt/solidangle/arnold-max/3/arnold-max-max2019-3.1.2-2./scripts", 
        "PATH": "/opt/autodesk/max-io/2019/max-io2019.SP0/bin:/opt/solidangle/arnold-max/3/arnold-max-max2019-3.1.2-2./bin", 
        "PYTHONPATH": "/opt/autodesk/max-io/2019/max-io2019.SP0/Conductor:/opt/solidangle/arnold-max/3/arnold-max-max2019-3.1.2-2./scripts", 
        "solidangle_LICENSE": "4101@docker_host"
    }, 
    "instance_type": "n1-standard-1", 
    "job_title": "Max: - quack.0003 renderSetupLayer1", 
    "local_upload": false, 
    "location": "london", 
    "metadata": {
        "ConductorVersion": "0.1.42"
    }, 
    "notify": [], 
    "output_path": "/Volumes/xtr/gd/duck/images", 
    "preemptible": true, 
    "project": "ATestForScott", 
    "scout_frames": "1,11,21,31,41,51,61,71,81,91", 
    "software_package_ids": [
        "732e688c522899625db1627adaa7cf3e", 
        "8e87ae3ee8c721aad91f8a9e9c25db7e"
    ], 
    "tasks_data": [
        {
            "command": "3dsrender -r  -s 1 -e 1 -b 1 -rl renderSetupLayer1 -rd /Volumes/xtr/gd/duck/images  -proj /Volumes/xtr/gd/duck /Volumes/xtr/gd/duck/scenes/quack.0003.ma", 
            "frames": "1"
        }, 
        {
            "command": "3dsrender -r  -s 2 -e 2 -b 1 -rl renderSetupLayer1 -rd /Volumes/xtr/gd/duck/images  -proj /Volumes/xtr/gd/duck /Volumes/xtr/gd/duck/scenes/quack.0003.ma", 
            "frames": "2"
        }, 
        {
            "command": "3dsrender -r  -s 3 -e 3 -b 1 -rl renderSetupLayer1 -rd /Volumes/xtr/gd/duck/images  -proj /Volumes/xtr/gd/duck /Volumes/xtr/gd/duck/scenes/quack.0003.ma", 
            "frames": "3"
        }, 
        {
            "command": "3dsrender -r  -s 4 -e 4 -b 1 -rl renderSetupLayer1 -rd /Volumes/xtr/gd/duck/images  -proj /Volumes/xtr/gd/duck /Volumes/xtr/gd/duck/scenes/quack.0003.ma", 
            "frames": "4"
        }, 
        {
            "command": "3dsrender -r  -s 5 -e 5 -b 1 -rl renderSetupLayer1 -rd /Volumes/xtr/gd/duck/images  -proj /Volumes/xtr/gd/duck /Volumes/xtr/gd/duck/scenes/quack.0003.ma", 
            "frames": "5"
        }, 
        {
            "command": "3dsrender -r  -s 6 -e 6 -b 1 -rl renderSetupLayer1 -rd /Volumes/xtr/gd/duck/images  -proj /Volumes/xtr/gd/duck /Volumes/xtr/gd/duck/scenes/quack.0003.ma", 
            "frames": "6"
        }, 
        {
            "command": "3dsrender -r  -s 7 -e 7 -b 1 -rl renderSetupLayer1 -rd /Volumes/xtr/gd/duck/images  -proj /Volumes/xtr/gd/duck /Volumes/xtr/gd/duck/scenes/quack.0003.ma", 
            "frames": "7"
        }, 
        {
            "command": "3dsrender -r  -s 8 -e 8 -b 1 -rl renderSetupLayer1 -rd /Volumes/xtr/gd/duck/images  -proj /Volumes/xtr/gd/duck /Volumes/xtr/gd/duck/scenes/quack.0003.ma", 
            "frames": "8"
        }, 
        {
            "command": "3dsrender -r  -s 9 -e 9 -b 1 -rl renderSetupLayer1 -rd /Volumes/xtr/gd/duck/images  -proj /Volumes/xtr/gd/duck /Volumes/xtr/gd/duck/scenes/quack.0003.ma", 
            "frames": "9"
        }, 
        {
            "command": "3dsrender -r  -s 10 -e 10 -b 1 -rl renderSetupLayer1 -rd /Volumes/xtr/gd/duck/images  -proj /Volumes/xtr/gd/duck /Volumes/xtr/gd/duck/scenes/quack.0003.ma", 
            "frames": "10"
        }
    ], 
    "upload_only": false, 
    "upload_paths": [
        "/Volumes/xtr/gd/duck/scenes/cone.ma", 
        "/Volumes/xtr/gd/duck/scenes/quack.0003.ma", 
        "/Volumes/xtr/gd/duck/sourceimages/alcazar.jpg", 
        "/Volumes/xtr/gd/duck/sourceimages/bugs_seq/bugs.0001.jpg", 
        "/Volumes/xtr/gd/duck/sourceimages/bugs_seq/bugs.0002.jpg", 
        "/Volumes/xtr/gd/duck/sourceimages/bugs_seq/bugs.0003.jpg", 
        "/Volumes/xtr/gd/duck/sourceimages/bugs_seq/bugs.0004.jpg", 
        "/Volumes/xtr/gd/duck/sourceimages/bugs_seq/bugs.0005.jpg", 
        "/Volumes/xtr/gd/duck/sourceimages/bugs_seq/bugs.0006.jpg", 
        "/Volumes/xtr/gd/duck/sourceimages/bugs_seq/bugs.0007.jpg", 
        "/Volumes/xtr/gd/duck/sourceimages/bugs_seq/bugs.0008.jpg", 
        "/Volumes/xtr/gd/duck/sourceimages/bugs_seq/bugs.0009.jpg", 
        "/Volumes/xtr/gd/duck/sourceimages/bugs_seq/bugs.0010.jpg", 
        "/Volumes/xtr/gd/duck/sourceimages/bush_restaurant_4k.hdr", 
        "/Volumes/xtr/gd/duck/sourceimages/bush_restaurant_4k.tx"
    ]
}
"""


class PreviewTab(QtWidgets.QScrollArea):

    def __init__(self,dialog):
        super(PreviewTab, self).__init__()
    
        widget = QtWidgets.QWidget()
        self.dialog = dialog
        self.setWidget(widget)
        self.setWidgetResizable(1)

        layout = QtWidgets.QHBoxLayout()
        widget.setLayout(layout)

        self.text_area = QtWidgets.QTextEdit()

        self.text_area.setReadOnly(True)
        self.text_area.setWordWrapMode(QtGui.QTextOption.NoWrap)
        layout.addWidget(self.text_area)

        self.populate(JSON)

    def populate(self, json):
        self.text_area.setText(json)
