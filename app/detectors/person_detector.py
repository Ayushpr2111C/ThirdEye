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
            verbose=False
        )[0]

        detections = sv.Detections.from_ultralytics(results)

        detections = self.tracker.update_with_detections(detections)

        persons = []

        for i in range(len(detections)):
            if detections.class_id[i] != 0:
                continue

            tracker_id = detections.tracker_id[i]

            # ByteTrack can occasionally return None
            if tracker_id is None:
                continue

            x1, y1, x2, y2 = map(
                int,
                detections.xyxy[i]
            )

            confidence = float(detections.confidence[i])

            persons.append({
                "id": int(tracker_id),
                "box": (x1, y1, x2, y2),
                "confidence": confidence
            })

        return persons