import cv2
import time
from datetime import datetime

from app.utils.camera import Camera
from app.detectors.person_detector import PersonDetector
from app.tracking.visitor_manager import VisitorManager
from app.recording.recorder import Recorder
from app.database.database import Database


def main():

    # -----------------------------
    # INITIALIZE SYSTEM
    # -----------------------------

    camera = Camera()

    detector = PersonDetector()

    visitor_manager = VisitorManager(
        stay_time=15,
        exit_grace=3
    )

    recorder = Recorder(
        output_dir="data/recordings",
        fps=20,
        buffer_seconds=15
    )

    database = Database()

    # Currently active database events
    active_events = {}

    print("================================")
    print("       SENTINEL AI STARTED")
    print("================================")

    while True:

        # -----------------------------
        # CAMERA
        # -----------------------------

        ret, frame = camera.read()

        if not ret:
            print("Camera frame failed.")
            break

        # -----------------------------
        # YOLO + BYTETRACK
        # -----------------------------

        persons = detector.detect(frame)

        # -----------------------------
        # VISITOR MANAGEMENT
        # -----------------------------

        events = visitor_manager.update(persons)

        # -----------------------------
        # ALWAYS UPDATE RECORDING BUFFER
        # -----------------------------

        recorder.update(frame)

        # -----------------------------
        # HANDLE EVENTS
        # -----------------------------

        for event in events:

            event_type = event["type"]
            person_id = event["person_id"]

            # =============================
            # VISITOR CONFIRMED
            # =============================

            if event_type == "visitor_confirmed":

                print(
                    f"[VISITOR] Person #{person_id} "
                    f"confirmed."
                )

                # Create database event
                event_id = database.create_event(
                    person_id=person_id,
                    start_time=event["first_seen_time"],
                    confirmed_time=datetime.now().isoformat(
                        timespec="seconds"
                    )
                )

                active_events[person_id] = {
                    "event_id": event_id,
                    "confirmed_time": time.monotonic()
                }

                # Start permanent recording
                recorder.start(frame)

            # =============================
            # VISITOR LEFT
            # =============================

            elif event_type == "visitor_left":

                print(
                    f"[VISITOR] Person #{person_id} "
                    f"left."
                )

                active_event = active_events.pop(
                    person_id,
                    None
                )

                # Stop recording
                recording_path = recorder.stop()

                if active_event:

                    end_time = datetime.now()

                    duration = (
                        time.monotonic()
                        - active_event["confirmed_time"]
                    )

                    database.finish_event(
                        event_id=active_event["event_id"],
                        end_time=end_time.isoformat(
                            timespec="seconds"
                        ),
                        duration=duration,
                        recording_path=recording_path
                    )

                    print(
                        f"[DATABASE] Event "
                        f"#{active_event['event_id']} "
                        f"completed."
                    )

        # -----------------------------
        # DRAW PERSONS
        # -----------------------------

        for person in persons:

            x1, y1, x2, y2 = person["box"]

            person_id = person["id"]

            visitor = visitor_manager.visitors.get(
                person_id
            )

            if visitor:

                if visitor["confirmed"]:

                    status = "VISITOR"

                else:

                    elapsed = (
                        time.monotonic()
                        - visitor["first_seen"]
                    )

                    remaining = max(
                        0,
                        visitor_manager.stay_time - elapsed
                    )

                    status = f"{remaining:.1f}s"

            else:

                status = "..."

            label = f"#{person_id} | {status}"

            # Bounding box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                2
            )

            # Person label
            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 25)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 0),
                2,
                cv2.LINE_AA
            )

        # -----------------------------
        # STATUS
        # -----------------------------

        if recorder.recording:

            status = "● RECORDING"

        elif persons:

            status = "PERSON DETECTED"

        else:

            status = "NO PERSON"

        cv2.putText(
            frame,
            status,
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255) if recorder.recording
            else (0, 255, 0),
            2,
            cv2.LINE_AA
        )

        # -----------------------------
        # DISPLAY
        # -----------------------------

        cv2.imshow(
            "Sentinel AI",
            frame
        )

        # Q = Quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # -----------------------------
    # CLEANUP
    # -----------------------------

    if recorder.recording:
        recorder.stop()

    database.close()
    camera.release()


if __name__ == "__main__":
    main()