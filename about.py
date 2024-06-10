from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class AboutTab(QWidget):
    def __init__(self):
        super().__init__()
        self.version = "0.2.2"
        self.versionDate = "sep 06 2021"
        self.UI()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        self.titleLabel = QLabel("Paradoxa MODBUS Tool")
        self.titleLabel.setStyleSheet("font: bold 30px")
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.authorLabel = QLabel("Author: ")
        self.authorLabel.setStyleSheet("font-size: 18px")
        self.nameLabel = QLabel("Eden Candelas")
        self.nameLabel.setStyleSheet("font-size: 18px")
        self.versionTextLabel = QLabel("Version: ")
        self.versionTextLabel.setStyleSheet("font-size: 18px")
        self.versionLabel = QLabel(self.version)
        self.versionLabel.setStyleSheet("font-size: 18px")
        self.dateTextLabel = QLabel("Version date: ")
        self.dateTextLabel.setStyleSheet("font-size: 18px")
        self.dateLabel = QLabel(self.versionDate)
        self.dateLabel.setStyleSheet("font-size: 18px")
        self.webpageTextLabel = QLabel("Webpage: ")
        self.webpageTextLabel.setStyleSheet("font-size: 18px")
        self.webpageLabel = QLabel('<a href="https://paradoxalabs.com/">https://paradoxalabs.com/</a>')
        self.webpageLabel.setOpenExternalLinks(True)
        self.webpageLabel.setStyleSheet("font-size: 18px")

    def layouts(self):

        self.titleLayout = QVBoxLayout()
        self.titleLayout.addWidget(self.titleLabel)

        self.formLayout = QFormLayout()
        self.formLayout.addRow(self.authorLabel, self.nameLabel)
        self.formLayout.addRow(self.versionTextLabel, self.versionLabel)
        self.formLayout.addRow(self.dateTextLabel, self.dateLabel)
        self.formLayout.addRow(self.webpageTextLabel, self.webpageLabel)
        # self.formLayout.setContentsMargins(200, 0, 150, 0)

        self.mainLabel = QHBoxLayout()
        self.mainLabel.addStretch()
        self.mainLabel.addLayout(self.formLayout)
        self.mainLabel.addStretch()

        self.wholeLayout = QVBoxLayout()
        self.wholeLayout.addLayout(self.titleLayout, 40)
        self.wholeLayout.addLayout(self.mainLabel, 60)

        self.setLayout(self.wholeLayout)
