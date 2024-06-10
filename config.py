from PyQt5.QtWidgets import *
import platform
import glob


class ConfigTab(QWidget):
    def __init__(self):
        super().__init__()
        self.UI()
        self.scanPorts()
        self.fields = [self.baudsEntry, self.portEntry]

    def UI(self):
        self.widgets()
        self.statusBar()
        self.layouts()

    def widgets(self):
        self.baudsEntry = QComboBox()
        self.baudsEntry.addItem("9600")
        self.baudsEntry.addItem("115000")
        self.bytesizeEntry = QComboBox()
        self.bytesizeEntry.addItem("8")
        self.bytesizeEntry.addItem("7")
        self.bytesizeEntry.addItem("6")
        self.bytesizeEntry.addItem("5")
        # self.bytesizeEntry.addItem("9")
        self.parityEntry = QComboBox()
        self.parityEntry.addItem("None")
        self.parityEntry.addItem("Even")
        self.parityEntry.addItem("Odd")
        self.parityEntry.addItem("Space")
        self.parityEntry.addItem("Mark")
        self.stopbitsEntry = QComboBox()
        self.stopbitsEntry.addItem("1")
        self.stopbitsEntry.addItem("2")
        self.portEntry = QComboBox()
        self.portEntry.setMaxVisibleItems(10)
        self.portEntry.setStyleSheet("combobox-popup: 0;")
        self.charDelayEntry = QSpinBox()
        self.frameDelayEntry = QSpinBox()
        self.openButton = QPushButton("Open")
        self.scanPortsButton = QPushButton("Scan Ports")
        self.scanPortsButton.clicked.connect(self.scanPorts)

    def layouts(self):
        self.wholeLayout = QVBoxLayout()
        self.mainLayout = QVBoxLayout()
        self.formLayout = QFormLayout()

        # Char, Frame, and Buttons Layouts
        self.charDelayLayout = QHBoxLayout()
        self.frameDelayLayout = QHBoxLayout()
        self.buttonsLayout = QHBoxLayout()
        self.charDelayLayout.addWidget(self.charDelayEntry, 80)
        self.charDelayLayout.addWidget(QLabel("ms"), 20)
        self.frameDelayLayout.addWidget(self.frameDelayEntry, 80)
        self.frameDelayLayout.addWidget(QLabel("ms"), 20)
        self.buttonsLayout.addStretch()
        # self.buttonsLayout.addWidget(self.scanPortsButton)
        self.buttonsLayout.addWidget(self.openButton)
        self.buttonsLayout.addStretch()
        self.buttonsLayout.setContentsMargins(0, 10, 0, 0)
        self.portLayout = QHBoxLayout()
        self.portLayout.addWidget(self.portEntry, 70)
        self.portLayout.addWidget(self.scanPortsButton, 30)

        # Form Layout
        self.formLayout.addRow("BAUDS: ", self.baudsEntry)
        self.formLayout.addRow("BYTESIZE: ", self.bytesizeEntry)
        self.formLayout.addRow("PARITY: ", self.parityEntry)
        self.formLayout.addRow("STOPBITS: ", self.stopbitsEntry)
        self.formLayout.addRow("PORT: ", self.portLayout)
        #self.formLayout.addRow("CHAR DELAY: ", self.charDelayLayout)
        #self.formLayout.addRow("FRAME DELAY: ", self.frameDelayLayout)
        self.formLayout.addRow("", self.buttonsLayout)

        # Main Layout
        self.mainLayout.addLayout(self.formLayout)
        # self.mainLayout.addLayout(self.buttonsLayout)
        self.mainLayout.addStretch()
        self.mainLayout.setContentsMargins(200, 100, 200, 100)

        self.wholeLayout.addLayout(self.mainLayout)
        self.wholeLayout.addLayout(self.statusLayout)
        # # set layout
        self.setLayout(self.wholeLayout)

    def statusBar(self):
        self.statusLayout = QHBoxLayout()
        self.statusLabel = QLabel("Disconnected")
        self.statusLabel.setStyleSheet("color:red")
        self.infoLabel = QLabel("")
        self.statusLayout.addWidget(self.statusLabel)
        self.statusLayout.addStretch()
        self.statusLayout.addWidget(self.infoLabel)

    def updateStatusBar(self, status, bauds, port, bytesize, parity, stopbits):
        self.statusLabel.setText(f"{status}")
        self.statusLabel.setStyleSheet("color:green")
        self.infoLabel.setText(f"BAUDS: {bauds}, {bytesize}{parity}{stopbits} PORT: {port}")

    def disconnectStatusBar(self):
        self.statusLabel.setText("Disconnected")
        self.statusLabel.setStyleSheet("color:red")
        self.infoLabel.setText("")

    def scanPorts(self):
        self.portEntry.clear()
        if platform.system() == 'Windows':
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif platform.system() == 'Linux':
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif platform.system() == 'Darwin':
            ports = glob.glob('/dev/tty.usb*')
        else:
            raise EnvironmentError('Unsupported platform')

        if platform.system() == 'Linux':
            for port in ports:
                if port[:9] != '/dev/ttyS' and port != '/dev/ttyprintk':
                    self.portEntry.addItem(port)
        else:
            for port in ports:
                self.portEntry.addItem(port)
