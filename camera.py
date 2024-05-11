import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QPixmap
from picamera2 import PiCamera2, PreviewStream, JPEGStream
import os

class CameraApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RobertOS Camera App")

        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create preview label
        self.preview_label = QLabel()
        self.layout.addWidget(self.preview_label)

        # Initialize picamera2
        self.camera = PiCamera2()
        self.camera.resolution = (640, 480)  # Set resolution
        self.preview_stream = None
        self.is_recording = False

        # Create buttons
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

    def start_preview(self):
        self.preview_stream = PreviewStream(self.camera)
        self.preview_stream.start()
        self.capture_preview()

    def capture_preview(self):
        # Capture a preview frame using picamera2
        with self.camera.capture_continuous(self.preview_stream.formats, burst=True) as capture_request:
            for frame in capture_request:
                frame.wait_done()
                # Convert frame data to QPixmap
                pixmap = QPixmap.fromImage(frame.image)
                self.preview_label.setPixmap(pixmap)
                self.preview_label.show()
                break

    def capture_image(self):
        # Use picamera2 for image capture
        with self.camera.capture_single(JPEGStream(self.camera), mainloop=False) as capture_request:
            capture_request.wait_done()
            image_data = capture_request.rents[0].data
            with open(os.path.expanduser('~/Pictures/captured_image.jpg'), 'wb') as f:
                f.write(image_data)
        print("Image captured and saved in Pictures directory as captured_image.jpg")

    def start_video_recording(self):
        # Use picamera2 for video recording (example using h264)
        self.video_stream = self.camera.create_video_stream(encoding="h264")
        self.video_stream.start_recording(os.path.expanduser('~/Videos/captured_video.h264'))
        self.start_video_button.setEnabled(False)
        self.stop_video_button.setEnabled(True)
        self.is_recording = True

    def stop_video_recording(self):
        self.video_stream.stop_recording()
        self.start_video_button.setEnabled(True)
        self.stop_video_button.setEnabled(False)
        self.is_recording = False
        print("Video recording stopped")

def main():
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
