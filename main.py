import base64
import binascii
import sys

import serial
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor
from datetime import datetime
from serial import Serial, SerialException
from threading import Event

import single
import config
import scan
import about


ser = Serial()


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paradoxa Labs Modbus Toolbox")
        self.setGeometry(610, 300, 750, 500)
        self.UI()
        self.show()
        self.statusBars = []

    def UI(self):
        self.addTabWidget()
        self.connectWidgets()

    def addTabWidget(self):
        self.tabWidget = QTabWidget()
        self.setCentralWidget(self.tabWidget)

        self.scanTab = scan.ScanTab()
        self.singleTab = single.SingleTab()
        self.configTab = config.ConfigTab()
        self.aboutTab = about.AboutTab()

        self.tabWidget.addTab(self.scanTab, "Scan")
        self.tabWidget.addTab(self.singleTab, "Single")
        self.tabWidget.addTab(self.configTab, "Config")
        self.tabWidget.addTab(self.aboutTab, "About")

    def connectWidgets(self):
        # Scan Tab
        self.scanTab.sendButton.clicked.connect(self.scan)
        self.scanTab.disconnectButton.clicked.connect(self.openPort)
        # Single Tab
        self.singleTab.sendButton.clicked.connect(self.singleSend)
        self.singleTab.disconnectButton.clicked.connect(self.openPort)
        # Config Tab
        self.configTab.openButton.clicked.connect(self.openPort)

    def scan(self):
        if ser.isOpen():
            try:
                if int(self.scanTab.toRegisterEntry.text(), base=16) - int(self.scanTab.fromRegisterEntry.text(), base=16) >= 0:
                    for address in range(int(self.scanTab.fromRegisterEntry.text(), base=16), int(self.scanTab.toRegisterEntry.text(), base=16)+1):
                        self.scanTab.sendButton.setEnabled(False)
                        self.scanTab.updateSentText(0, hex(address)[2:])
                        send = bytes.fromhex(self.scanTab.sentEntry.text())
                        if self.scanTab.timeoutEntry.text() != "":
                            ser.timeout = float(self.scanTab.timeoutEntry.text())
                        ser.write(send)
                        sent_time = datetime.now().strftime('%H:%M:%S.%f')
                        received_list = []
                        Event().wait(0.0025)
                        while ser.in_waiting > 0:
                            line = ser.readline()
                            if len(line) > 4:
                                received_list.append(line.hex())
                            else:
                                line = line.decode("utf-8").strip()
                                if len(line) < 2:
                                    line = '0' + line
                                received_list.append(line)
                        received_time = datetime.now().strftime('%H:%M:%S.%f')
                        print(received_list)
                        self.showInfoScanTab(received_list, sent_time, received_time)
                        self.scanTab.sendButton.setEnabled(True)
                else:
                    self.scanTab.textEditor.setTextColor(QColor(255, 0, 0))
                    self.scanTab.textEditor.append("Please enter a valid range")
            except ValueError:
                print("Value error in scan fields")
                self.scanTab.sendButton.setEnabled(True)
                self.scanTab.textEditor.setTextColor(QColor(255, 0, 0))
                self.scanTab.textEditor.append("Fields cannot be empty")
        elif not ser.isOpen():
            self.scanTab.textEditor.setTextColor(QColor(255, 0, 0))
            self.scanTab.textEditor.append("Serial Port is not Open")
            self.scanTab.textEditor.setTextColor(QColor(0, 0, 0))

    def singleSend(self):
        if ser.isOpen():
            send = bytes.fromhex(self.singleTab.sentEntry.text())
            if self.singleTab.timeoutEntry.text() != "":
                ser.timeout = float(self.singleTab.timeoutEntry.text())
            ser.write(send)
            sent_time = datetime.now().strftime('%H:%M:%S.%f')
            received_list = []
            Event().wait(0.1)
            while ser.in_waiting > 0:
                line = ser.readline()
                if len(line) > 4:
                    received_list.append(line.hex())
                else:
                    line = line.decode("utf-8").strip()
                    if len(line) < 2:
                        line = '0' + line
                    received_list.append(line)
            print(received_list)
            received_time = datetime.now().strftime('%H:%M:%S.%f')
            self.showInfo(received_list, sent_time, received_time)
        elif not ser.isOpen():
            self.singleTab.textEditor.setTextColor(QColor(255, 0, 0))
            self.singleTab.textEditor.append("Serial Port is not Open")
            self.singleTab.textEditor.setTextColor(QColor(0, 0, 0))

    def showInfo(self, info, send_time, receive_time):
        if self.singleTab.showTimestampCheckbox.isChecked() and self.singleTab.showSentCheckbox.isChecked():
            self.singleTab.textEditor.setTextColor(QColor(0, 0, 180))
            self.singleTab.textEditor.append(f"{send_time} - {self.singleTab.sentEntry.text()} - ")
            self.singleTab.textEditor.setTextColor(QColor(0, 125, 0))
            self.singleTab.textEditor.append(f"{receive_time} - {''.join(info)}")
            self.singleTab.textEditor.setTextColor(QColor(0, 0, 0))
        elif self.singleTab.showTimestampCheckbox.isChecked():
            self.singleTab.textEditor.setTextColor(QColor(0, 0, 255))
            self.singleTab.textEditor.append(f"{send_time}")
            self.singleTab.textEditor.setTextColor(QColor(0, 125, 0))
            self.singleTab.textEditor.append(f"{receive_time} - {''.join(info)}")
        elif self.singleTab.showSentCheckbox.isChecked():
            self.singleTab.textEditor.setTextColor(QColor(0, 0, 255))
            self.singleTab.textEditor.append(f"{self.singleTab.sentEntry.text()}")
            self.singleTab.textEditor.setTextColor(QColor(0, 125, 0))
            self.singleTab.textEditor.append(f"{''.join(info)}")
        else:
            self.singleTab.textEditor.setTextColor(QColor(0, 125, 0))
            self.singleTab.textEditor.append(f"{''.join(info)}")
            self.singleTab.textEditor.setTextColor(QColor(0, 0, 0))

    def showInfoScanTab(self, info, send_time, receive_time):
        if self.scanTab.showTimestampCheckbox.isChecked() and self.scanTab.showSentCheckbox.isChecked():
            self.scanTab.textEditor.setTextColor(QColor(0, 0, 180))
            self.scanTab.textEditor.append(f"{send_time} - {self.scanTab.sentEntry.text()} - ")
            self.scanTab.textEditor.setTextColor(QColor(0, 125, 0))
            self.scanTab.textEditor.append(f"{receive_time} - {''.join(info)}")
            self.scanTab.textEditor.setTextColor(QColor(0, 0, 0))
        elif self.scanTab.showTimestampCheckbox.isChecked():
            self.scanTab.textEditor.setTextColor(QColor(0, 125, 255))
            self.scanTab.textEditor.append(f"{send_time}")
            self.scanTab.textEditor.setTextColor(QColor(0, 125, 0))
            self.scanTab.textEditor.append(f"{receive_time} - {''.join(info)}")
        elif self.scanTab.showSentCheckbox.isChecked():
            self.scanTab.textEditor.setTextColor(QColor(0, 0, 255))
            self.scanTab.textEditor.append(f"{self.scanTab.sentEntry.text()}")
            self.scanTab.textEditor.setTextColor(QColor(0, 125, 0))
            self.scanTab.textEditor.append(f"{''.join(info)}")
        else:
            self.scanTab.textEditor.setTextColor(QColor(0, 125, 0))
            self.scanTab.textEditor.append(f"{''.join(info)}")
            self.scanTab.textEditor.setTextColor(QColor(0, 0, 0))

    def setBytesize(self):
        if self.configTab.bytesizeEntry.currentText() == '8':
            ser.bytesize = serial.EIGHTBITS
        elif self.configTab.bytesizeEntry.currentText() == '7':
            ser.bytesize = serial.SEVENBITS
        elif self.configTab.bytesizeEntry.currentText() == '6':
            ser.bytesize = serial.SIXBITS
        elif self.configTab.bytesizeEntry.currentText() == '5':
            ser.bytesize = serial.FIVEBITS

    def setParity(self):
        if self.configTab.parityEntry.currentText() == 'None':
            ser.parity = serial.PARITY_NONE
        elif self.configTab.parityEntry.currentText() == 'Even':
            ser.parity = serial.PARITY_EVEN
        elif self.configTab.parityEntry.currentText() == 'Odd':
            ser.parity = serial.PARITY_ODD
        elif self.configTab.parityEntry.currentText() == 'Space':
            ser.parity = serial.PARITY_SPACE
        elif self.configTab.parityEntry.currentText() == 'Mark':
            ser.parity = serial.PARITY_SPACE

    def openPort(self):
        for field in self.configTab.fields:
            if field.currentText() == "":
                QMessageBox.information(self, "Warning", "Select a port to open")
                break
        ser.baudrate = int(self.configTab.baudsEntry.currentText())
        # self.setBytesize()
        # self.setParity()
        ser.bytesize = int(self.configTab.bytesizeEntry.currentText())
        ser.parity = self.configTab.parityEntry.currentText()[0]
        ser.stopbits = int(self.configTab.stopbitsEntry.currentText())
        ser.port = self.configTab.portEntry.currentText()
        ser.timeout = 1
        if not ser.isOpen():
            try:
                ser.open()
                self.updateConnectionButtons()
            except SerialException:
                print("Error. Could not open port. Serial Exception")
                QMessageBox.information(self, "Error", f"Serial Exception. Could not open port {ser.port}")
        else:
            print("Port already open")
        self.updateStatusBars()

    def updateConnectionButtons(self):
        if ser.isOpen():
            self.configTab.openButton.setText("Disconnect")
            self.configTab.openButton.disconnect()
            self.configTab.openButton.clicked.connect(self.disconnect)
            self.singleTab.disconnectButton.setText("DISCONNECT")
            self.singleTab.disconnectButton.disconnect()
            self.singleTab.disconnectButton.clicked.connect(self.disconnect)
            self.scanTab.disconnectButton.setText("DISCONNECT")
            self.scanTab.disconnectButton.disconnect()
            self.scanTab.disconnectButton.clicked.connect(self.disconnect)
        elif not ser.isOpen():
            self.configTab.openButton.setText("Open")
            self.configTab.openButton.disconnect()
            self.configTab.openButton.clicked.connect(self.openPort)
            self.singleTab.disconnectButton.setText("OPEN")
            self.singleTab.disconnectButton.disconnect()
            self.singleTab.disconnectButton.clicked.connect(self.openPort)
            self.scanTab.disconnectButton.setText("OPEN")
            self.scanTab.disconnectButton.disconnect()
            self.scanTab.disconnectButton.clicked.connect(self.openPort)

    def updateStatusBars(self):
        if ser.isOpen():
            status = "Connected"
            self.scanTab.updateStatusBar(status, ser.baudrate, ser.port, ser.bytesize, ser.parity, ser.stopbits)
            self.singleTab.updateStatusBar(status, ser.baudrate, ser.port, ser.bytesize, ser.parity, ser.stopbits)
            self.configTab.updateStatusBar(status, ser.baudrate, ser.port, ser.bytesize, ser.parity, ser.stopbits)

    def disconnectStatusBars(self):
        if not ser.isOpen():
            self.scanTab.disconnectStatusBar()
            self.singleTab.disconnectStatusBar()
            self.configTab.disconnectStatusBar()

    def disconnect(self):
        if ser.isOpen():
            ser.close()
            self.disconnectStatusBars()
            self.updateConnectionButtons()
            if not ser.isOpen():
                if self.singleTab.isVisible():
                    self.singleTab.textEditor.setTextColor(QColor(255, 0, 0))
                    self.singleTab.textEditor.append(f"Disconnected from {ser.port}")
                    self.singleTab.textEditor.setTextColor(QColor(0, 0, 0))
                elif self.scanTab.isVisible():
                    self.scanTab.textEditor.setTextColor(QColor(255, 0, 0))
                    self.scanTab.textEditor.append(f"Disconnected from {ser.port}")
                    self.scanTab.textEditor.setTextColor(QColor(0, 0, 0))
        else:
            if self.singleTab.isVisible():
                self.singleTab.textEditor.setTextColor(QColor(255, 0, 0))
                self.singleTab.textEditor.append(f"Serial port is not open")
                self.singleTab.textEditor.setTextColor(QColor(0, 0, 0))
            elif self.scanTab.isVisible():
                self.scanTab.textEditor.setTextColor(QColor(255, 0, 0))
                self.scanTab.textEditor.append(f"Serial port is not open")
                self.scanTab.textEditor.setTextColor(QColor(0, 0, 0))


def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())


if __name__ == "__main__":
    main()
