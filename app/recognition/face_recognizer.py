from deepface import DeepFace
import os


class FaceRecognizer:

    def __init__(self, database_path="data/faces"):

        self.database_path = database_path

        os.makedirs(
            self.database_path,
            exist_ok=True
        )

        self.model_name = "ArcFace"
        self.detector_backend = "opencv"
        self.distance_metric = "cosine"

    def recognize(self, frame):

        try:

            results = DeepFace.find(
                img_path=frame,
                db_path=self.database_path,
                model_name=self.model_name,
                detector_backend=self.detector_backend,
                distance_metric=self.distance_metric,
                enforce_detection=False,
                silent=True
            )

            if not results:
                return None

            result = results[0]

            if result.empty:
                return None

            identity = result.iloc[0]["identity"]

            # Extract person's folder name
            person_name = os.path.basename(
                os.path.dirname(identity)
            )

            return person_name

        except Exception as e:

            print(
                f"[FACE] Recognition error: {e}"
            )

            return None