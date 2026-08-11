import cv2
import os
from datetime import datetime


class Recorder:

    def __init__(self, output_dir="data/recordings", fps=20):
        self.output_dir = output_dir
        self.fps = fps

        self.writer = None
        self.recording = False
        self.file_path = None

        os.makedirs(self.output_dir, exist_ok=True)

    def start(self, frame):

        if self.recording:
            return

        height, width = frame.shape[:2]

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        self.file_path = os.path.join(
            self.output_dir,
            f"visitor_{timestamp}.mp4"
        )

        fourcc = cv2.VideoWriter_fourcc(
            *"mp4v"
        )

        self.writer = cv2.VideoWriter(
            self.file_path,
            fourcc,
            self.fps,
            (width, height)
        )

        self.recording = True

        print(f"[REC] Started: {self.file_path}")

    def write(self, frame):

        if self.recording and self.writer:
            self.writer.write(frame)

    def stop(self):

        if not self.recording:
            return None

        self.writer.release()

        self.writer = None
        self.recording = False

        print(f"[REC] Saved: {self.file_path}")

        saved_file = self.file_path
        self.file_path = None

        return saved_file