import cv2


class MotionDetector:
    def __init__(self, min_area=2000):
        self.previous_frame = None
        self.min_area = min_area

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.previous_frame is None:
            self.previous_frame = gray
            return False, []

        frame_delta = cv2.absdiff(self.previous_frame, gray)

        thresh = cv2.threshold(
            frame_delta,
            25,
            255,
            cv2.THRESH_BINARY
        )[1]

        thresh = cv2.dilate(thresh, None, iterations=2)

        contours, _ = cv2.findContours(
            thresh,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        boxes = []

        for contour in contours:
            if cv2.contourArea(contour) < self.min_area:
                continue

            x, y, w, h = cv2.boundingRect(contour)
            boxes.append((x, y, w, h))

        self.previous_frame = gray

        return len(boxes) > 0, boxes