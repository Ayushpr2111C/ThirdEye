import cv2
import os
from collections import deque
from datetime import datetime


class Recorder:

    def __init__(
        self,
        output_dir="data/recordings",
        fps=20,
        buffer_seconds=15
    ):
        self.output_dir = output_dir
        self.fps = fps

        # Number of frames kept in temporary memory
        self.buffer_size = int(fps * buffer_seconds)

        self.buffer = deque(maxlen=self.buffer_size)

        self.writer = None
        self.recording = False
        self.file_path = None

        os.makedirs(self.output_dir, exist_ok=True)

    def update(self, frame):
        """
        Add the current frame to the rolling buffer.

        If recording is active, also save it permanently.
        """

        # Always maintain the rolling buffer
        self.buffer.append(frame.copy())

        # If recording, write the current frame
        if self.recording and self.writer:
            self.writer.write(frame)

    def start(self, frame):
        """
        Start permanent recording and save
        the frames currently in the buffer first.
        """

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

        if not self.writer.isOpened():
            self.writer = None
            raise RuntimeError(
                "Could not open video writer."
            )

        self.recording = True

        print(
            f"[REC] Started: {self.file_path}"
        )

        # Save the previous buffered footage
        for buffered_frame in self.buffer:
            self.writer.write(buffered_frame)

        print(
            f"[REC] Saved {len(self.buffer)} "
            f"pre-event frames."
        )

    def stop(self):
        """
        Stop permanent recording.
        """

        if not self.recording:
            return None

        self.writer.release()

        self.writer = None
        self.recording = False

        saved_file = self.file_path

        print(
            f"[REC] Saved: {saved_file}"
        )

        self.file_path = None

        return saved_file