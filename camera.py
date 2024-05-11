import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QPixmap
from picamera import PiCamera
from time import sleep
import os

class CameraApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Raspberry Pi Camera App")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.preview_label = QLabel()
        self.layout.addWidget(self.preview_label)

        self.start_preview_button = QPushButton("Start Preview")
        self.start_preview_button.clicked.connect(self.start_preview)
        self.layout.addWidget(self.start_preview_button)

        self.capture_image_button = QPushButton("Capture Image")
        self.capture_image_button.clicked.connect(self.capture_image)
        self.layout.addWidget(self.capture_image_button)

        self.start_video_button = QPushButton("Start Video Recording")
        self.start_video_button.clicked.connect(self.start_video_recording)
        self.layout.addWidget(self.start_video_button)

        self.stop_video_button = QPushButton("Stop Video Recording")
        self.stop_video_button.clicked.connect(self.stop_video_recording)
        self.stop_video_button.setEnabled(False)
        self.layout.addWidget(self.stop_video_button)

        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.rotation = 180
        self.is_recording = False

    def start_preview(self):
        self.camera.start_preview()
        sleep(2)  # Add a delay to allow the camera to warm up
        self.capture_preview()

    def capture_preview(self):
        self.camera.capture(os.path.expanduser('~/Pictures/preview.jpg'))
        pixmap = QPixmap(os.path.expanduser('~/Pictures/preview.jpg'))
        self.preview_label.setPixmap(pixmap)
        self.preview_label.show()

    def capture_image(self):
        self.camera.capture(os.path.expanduser('~/Pictures/captured_image.jpg'))
        print("Image captured and saved in Pictures directory as captured_image.jpg")

    def start_video_recording(self):
        self.camera.start_recording(os.path.expanduser('~/Videos/captured_video.h264'))
        self.start_video_button.setEnabled(False)
        self.stop_video_button.setEnabled(True)
        self.is_recording = True

    def stop_video_recording(self):
        self.camera.stop_recording()
        self.start_video_button.setEnabled(True)
        self.stop_video_button.setEnabled(False)
        self.is_recording = False
        print("Video recording stopped")

    def closeEvent(self, event):
        if self.is_recording:
            self.stop_video_recording()
        self.camera.stop_preview()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
