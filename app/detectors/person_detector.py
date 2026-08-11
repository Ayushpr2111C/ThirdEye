from ultralytics import YOLO
import supervision as sv


class PersonDetector:

    def __init__(self):
        self.model = YOLO("yolo11n.pt")
        self.tracker = sv.ByteTrack()

    def detect(self, frame):

        results = self.model.predict(
            frame,
            classes=[0],
            conf=0.5,
            imgsz=640,
            verbose=False
        )[0]

        detections = sv.Detections.from_ultralytics(results)

        detections = self.tracker.update_with_detections(detections)

        persons = []

        # Prevent duplicate tracker IDs
        seen_ids = set()

        for i in range(len(detections)):

            tracker_id = detections.tracker_id[i]

            if tracker_id is None:
                continue

            tracker_id = int(tracker_id)

            # Ignore duplicate IDs
            if tracker_id in seen_ids:
                continue

            seen_ids.add(tracker_id)

            x1, y1, x2, y2 = map(
                int,
                detections.xyxy[i]
            )

            confidence = float(
                detections.confidence[i]
            )

            persons.append({
                "id": tracker_id,
                "box": (x1, y1, x2, y2),
                "confidence": confidence
            })

        return persons