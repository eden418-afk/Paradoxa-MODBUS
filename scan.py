import libscrc
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ScanTab(QWidget):
    def __init__(self):
        super().__init__()
        self.UI()

    def UI(self):
        self.statusBar()
        self.widgets()
        self.layouts()

    def widgets(self):
        self.textEditor = QTextEdit()
        self.textEditor.setReadOnly(True)
        self.clearButton = QPushButton("Clear")
        self.clearButton.clicked.connect(self.clearTextEditor)

        self.fromRegisterEntry = QLineEdit()
        self.toRegisterEntry = QLineEdit()
        self.fromRegisterEntry.setPlaceholderText("0 - ff")
        self.toRegisterEntry.setPlaceholderText("0 - ff")
        addressEntryrx = QRegExp("[abcdef0123456789]{2}")
        self.fromRegisterEntry.setValidator(QRegExpValidator(addressEntryrx))
        self.toRegisterEntry.setValidator(QRegExpValidator(addressEntryrx))
        self.fromRegisterEntry.textEdited.connect(self.updateSentText)
        self.toRegisterEntry.textEdited.connect(self.updateSentText)
        self.commandEntry = QSpinBox()
        self.commandEntry.setRange(0, 6)
        self.commandEntry.setPrefix("0")
        self.commandEntry.valueChanged.connect(self.updateSentText)
        self.registerEntry = QLineEdit()
        self.registerEntry.textEdited.connect(self.updateSentText)
        self.registerEntry.setPlaceholderText("0 - ffff")
        registerEntryrx = QRegExp("[abcdef0123456789]{4}")
        self.registerEntry.setValidator(QRegExpValidator(registerEntryrx))
        self.quantityEntry = QSpinBox()
        self.quantityEntry.setRange(0, 32)
        self.quantityEntry.setPrefix("000")
        self.quantityEntry.valueChanged.connect(self.updateSentText)
        self.timeoutEntry = QLineEdit()
        self.timeoutEntry.setPlaceholderText("Default 1s")
        timeoutEntryrx = QRegExp("[+-]?([0-9]*[.])?[0-9]+")
        self.timeoutEntry.setValidator(QRegExpValidator(timeoutEntryrx))
        # Checkboxes
        self.flipCRCCheckbox = QCheckBox("Flip CRC")
        self.flipCRCCheckbox.stateChanged.connect(self.updateSentText)
        self.showSentCheckbox = QCheckBox("Show sent")
        self.showTimestampCheckbox = QCheckBox("Show timestamp")
        # Buttons
        self.sendButton = QPushButton("SEND")
        self.disconnectButton = QPushButton("OPEN")
        # Sent Entry
        self.sentLabel = QLabel("SENT")
        self.sentEntry = QLineEdit()
        self.sentEntry.setReadOnly(True)

    def layouts(self):
        self.wholeLayout = QVBoxLayout()
        self.mainLayout = QHBoxLayout()
        self.leftLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()
        self.formLayout = QFormLayout()
        self.buttonsLayout = QHBoxLayout()
        self.adressLabelsLayout = QHBoxLayout()
        self.adressEntriesLayout = QHBoxLayout()
        self.textEditorLabelsLayout = QHBoxLayout()
        # left layout
        self.textEditorLabelsLayout.addStretch()
        self.textEditorLabelsLayout.addWidget(QLabel("SENT"))
        self.textEditorLabelsLayout.addWidget(QLabel(":"))
        self.textEditorLabelsLayout.addWidget((QLabel("RECEIVED")))
        self.textEditorLabelsLayout.addStretch()
        # self.leftLayout.addLayout(self.textEditorLabelsLayout)
        self.leftLayout.addWidget(self.textEditor)
        self.leftLayout.addWidget(self.clearButton)
        # register layouts
        self.adressLabelsLayout.addWidget(QLabel("FROM"))
        self.adressLabelsLayout.addWidget(QLabel("TO"))
        self.adressEntriesLayout.addWidget(self.fromRegisterEntry)
        self.adressEntriesLayout.addWidget(self.toRegisterEntry)
        # form layout
        self.formLayout.addRow("", self.adressLabelsLayout)
        self.formLayout.addRow("ADDRESS: ", self.adressEntriesLayout)
        self.formLayout.addRow("COMMAND: ", self.commandEntry)
        self.formLayout.addRow("REGISTER: ", self.registerEntry)
        self.formLayout.addRow("QUANTITY: ", self.quantityEntry)
        self.formLayout.addRow("Timeout: ", self.timeoutEntry)
        # buttons layout
        self.buttonsLayout.addWidget(self.sendButton)
        self.buttonsLayout.addWidget(self.disconnectButton)
        # right layout
        self.rightLayout.addLayout(self.formLayout)
        self.rightLayout.addWidget(self.flipCRCCheckbox)
        self.rightLayout.addWidget(self.showSentCheckbox)
        self.rightLayout.addWidget(self.showTimestampCheckbox)
        self.rightLayout.addWidget(self.sentLabel)
        self.rightLayout.addWidget(self.sentEntry)
        self.rightLayout.addLayout(self.buttonsLayout)
        self.rightLayout.addStretch()
        self.rightLayout.setContentsMargins(0, 0, 0, 0)
        # main layout
        self.mainLayout.addLayout(self.leftLayout, 60)
        self.mainLayout.addLayout(self.rightLayout, 40)
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
        self.infoLabel.setText(f"BAUDS: {bauds}, {bytesize}{parity}{stopbits}, PORT: {port}")

    def disconnectStatusBar(self):
        self.statusLabel.setText("Disconnected")
        self.statusLabel.setStyleSheet("color:red")
        self.infoLabel.setText("")

    def fillRegisterEntry(self):
        zeroCount = 4 - len(self.registerEntry.text())
        return f"{'0' * zeroCount}{self.registerEntry.text()}"

    def calculateCRC16(self):
        try:
            text = self.sentEntry.text()
            n = 2
            list = [text[i:i+n] for i in range(0, len(text), n)]
            joined = f"{list[0]}{list[1]}{list[2]}{list[3]}{list[4]}{list[5]}"
            toBytes = bytes.fromhex(joined)
            hexadecimal = hex(libscrc.modbus(toBytes))
            zeroCount = 6 - len(hexadecimal)
            return f"{'0' * zeroCount}{hexadecimal[2:]}"
        except ValueError:
            pass

    def updateSentText(self, a, address=None):
        if address is None:
            address = self.fromRegisterEntry.text()
        addressWithZero = f"0{address}"

        if self.quantityEntry.value() < 10:
            self.quantityEntry.setPrefix("000")
        else:
            self.quantityEntry.setPrefix("00")

        try:
            self.sentEntry.setText(f"{address if len(str(address)) == 2 else addressWithZero}"
                                   f"{self.commandEntry.text()}"
                                   f"{self.registerEntry.text() if len(self.registerEntry.text()) == 4 else self.fillRegisterEntry()}"
                                   f"{self.quantityEntry.text()}")
            if self.flipCRCCheckbox.isChecked():
                self.sentEntry.setText(f"{self.sentEntry.text()}{self.calculateCRC16()}")
            else:
                self.sentEntry.setText(f"{self.sentEntry.text()}{self.calculateCRC16()[2:]}{self.calculateCRC16()[0:2]}")
        except TypeError:
            print("Error in scanTab Entries")

    def clearTextEditor(self):
        self.textEditor.clear()
