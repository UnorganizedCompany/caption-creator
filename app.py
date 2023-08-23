import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
                             QLineEdit, QFileDialog, QMessageBox, QTabWidget, QTextEdit)
from PyQt5.QtCore import Qt
from file_reader import FileReader, CaptionInfo
import mm_generator

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.tabs = QTabWidget()

        self.srt_tab = QWidget()
        self.srt_tab_layout = QVBoxLayout()

        self.fileLabel = QLabel("SRT 파일을 드래그 앤 드롭 하세요", self)
        self.filePathEdit = QLineEdit(self)
        self.outputPathEdit = QLineEdit(self)
        self.outputPathButton = QPushButton("Output Path 선택", self)

        self.video_tab = QWidget()
        self.video_tab_layout = QVBoxLayout()

        self.generateButton = QPushButton("Video Generate", self)

        self.single_tab = QWidget()
        self.single_tab_layout = QVBoxLayout()

        self.textInput = QTextEdit(self)
        self.singleGenButton = QPushButton("Single Image Gen", self)

        self.captions = []
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        layout.addWidget(self.tabs)

        # SRT 가져오기 탭
        self.fileLabel.setAlignment(Qt.AlignCenter)
        self.fileLabel.setAcceptDrops(True)
        self.fileLabel.setStyleSheet("background-color: lightgray;")
        self.fileLabel.setFixedSize(300, 100)
        self.fileLabel.dragEnterEvent = self.dragEnterEvent
        self.fileLabel.dropEvent = self.dropEvent
        self.fileLabel.mousePressEvent = self.openFileBrowser
        self.srt_tab_layout.addWidget(self.fileLabel)

        self.filePathEdit.setReadOnly(True)
        self.srt_tab_layout.addWidget(self.filePathEdit)

        self.outputPathEdit.setText(f"{os.getcwd()}/dist/")
        self.outputPathEdit.setReadOnly(True)
        self.srt_tab_layout.addWidget(self.outputPathEdit)

        self.outputPathButton.clicked.connect(self.setOutputPath)
        self.srt_tab_layout.addWidget(self.outputPathButton)

        self.srt_tab.setLayout(self.srt_tab_layout)
        self.tabs.addTab(self.srt_tab, "SRT 가져오기")

        # 비디오 생성 탭
        self.generateButton.clicked.connect(self.generateVideo)
        self.video_tab_layout.addWidget(self.generateButton)
        self.video_tab.setLayout(self.video_tab_layout)
        self.tabs.addTab(self.video_tab, "비디오 생성")
        self.video_tab.setEnabled(False)

        # 단일 이미지 생성 탭
        self.textInput.setPlaceholderText("이미지로 변환할 텍스트를 입력하세요.")
        self.singleGenButton.clicked.connect(self.generateSingleImage)
        self.single_tab_layout.addWidget(self.textInput)
        self.single_tab_layout.addWidget(self.singleGenButton)
        self.single_tab.setLayout(self.single_tab_layout)
        self.tabs.addTab(self.single_tab, "단일 이미지 생성")

        self.setLayout(layout)
        self.setWindowTitle('Caption Creator')
        self.resize(400, 300)
        self.show()

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        filepath = e.mimeData().urls()[0].toLocalFile()
        if filepath.endswith('.srt'):
            self.fileLabel.setText(filepath)
            reader = FileReader(filepath)
            self.captions = reader.get_captions()
            mm_generator.generate_image(reader.get_captions(), self.outputPathEdit.text().strip())
            self.video_tab.setEnabled(True)
        else:
            QMessageBox.warning(self, "경고", "SRT 파일만 가능합니다!")

    def openFileBrowser(self, e):
        filepath, _ = QFileDialog.getOpenFileName(self, "SRT 파일 선택", "", "SRT Files (*.srt)")
        if filepath.endswith('.srt'):
            self.fileLabel.setText(filepath)
            reader = FileReader(filepath)
            self.captions = reader.get_captions()
            mm_generator.generate_image(reader.get_captions(), self.outputPathEdit.text().strip())
            self.video_tab.setEnabled(True)
        else:
            QMessageBox.warning(self, "경고", "SRT 파일만 가능합니다!")
        super().mousePressEvent(e)

    def setOutputPath(self):
        dirpath = QFileDialog.getExistingDirectory(self, "Output Path 선택")
        if dirpath:
            self.outputPathEdit.setText(dirpath)

    def generateVideo(self):
        output_path = self.outputPathEdit.text().strip()

        if len(self.captions) == 0:
            QMessageBox.warning(self, "경고", "이미지를 먼저 생성해주세요!")
            return

        if not os.path.exists(output_path) or not os.path.isdir(output_path):
            QMessageBox.warning(self, "경고", "유효한 경로를 선택해주세요!")
            return

        files_in_dir = os.listdir(output_path)
        png_files = [f for f in files_in_dir if f.endswith(".png")]

        if len(png_files) == 0:
            QMessageBox.warning(self, "경고", "선택한 경로에 PNG 이미지 파일이 없습니다!")
            return

        mm_generator.generate_video(self.captions, output_path)

    def generateSingleImage(self):
        output_path = self.outputPathEdit.text().strip()

        if not os.path.exists(output_path) or not os.path.isdir(output_path):
            QMessageBox.warning(self, "경고", "유효한 경로를 선택해주세요!")
            return

        mm_generator.generate_image([CaptionInfo(99999, 0, 0, self.textInput.toPlainText().split("\n"))], output_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
