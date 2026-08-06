import cv2
import time
import lzma
from app.utils.camera import Camera
from app.detectors.motion_detector import MotionDetector
from app.detectors.person_detector import PersonDetector


def main():
    camera = Camera()
    motion = MotionDetector()
    last_motion_time = 0
    MOTION_TIMEOUT = 15 

    while True:
        frame = camera.read_frame()
        detected, _ = motion.detect(frame)
        person_detector = PersonDetector()

        persons = []
        persons = person_detector.detect(frame)
        
        if detected:
            last_motion_time = time.time()

        if time.time() - last_motion_time < MOTION_TIMEOUT:
            status = "Motion Detected"
            color = (0, 0, 255)
        else:
            status = "No Motion"
            color = (0, 255, 0)

        for person in persons:

            x1, y1, x2, y2 = person["box"]

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                2
            )

            cv2.putText(
                frame,
                f"Person {person['confidence']:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 0),
                2
            )

        if len(persons):
            status = "Person Detected"
            color = (0, 0, 255)
        else:
            status = "No Person"
            color = (0, 255, 0)

        cv2.putText(
            frame,
            status,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            2,
        )

        cv2.imshow("ThirdEye", frame)

        key = cv2.waitKey(1)

        if key == ord("q"):
            break

    camera.release()


if __name__ == "__main__":
    main()