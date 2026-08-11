import cv2
import time
from app.utils.camera import Camera
from app.detectors.motion_detector import MotionDetector
from app.detectors.person_detector import PersonDetector
from app.tracking.visitor_manager import VisitorManager


def main():
    camera = Camera()
    motion = MotionDetector()
    last_motion_time = 0
    MOTION_TIMEOUT = 15 
    visitor_manager = VisitorManager(
    stay_time=15,
    exit_grace=3)

    while True:
        frame = camera.read_frame()
        detected, _ = motion.detect(frame)
        person_detector = PersonDetector()

        persons = []
        persons = person_detector.detect(frame)
        events = visitor_manager.update(persons)
                
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

            person_id = person["id"]

            visitor = visitor_manager.visitors.get(person_id)

            if visitor:

                if visitor["confirmed"]:
                    status = "VISITOR"
                else:
                    elapsed = time.monotonic() - visitor["first_seen"]
                    remaining = max(
                        0,
                        visitor_manager.stay_time - elapsed
                    )

                    status = f"{remaining:.1f}s"

            else:
                status = "..."

            label = f"#{person_id} | {status}"

            # Person box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                2
            )

            # Label
            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 0),
                2,
                cv2.LINE_AA
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