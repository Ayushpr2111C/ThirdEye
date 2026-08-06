from ultralytics import YOLO


class PersonDetector:
    def __init__(self):
        self.model = YOLO("yolo11n.pt")

    def detect(self, frame):
        results = self.model(frame, verbose=False)

        persons = []

        for result in results:
            for box in result.boxes:

                cls = int(box.cls[0])

                # COCO class 0 = person
                if cls != 0:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                confidence = float(box.conf[0])

                persons.append({
                    "box": (x1, y1, x2, y2),
                    "confidence": confidence
                })

        return persons