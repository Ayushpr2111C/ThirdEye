from deepface import DeepFace


result = DeepFace.find(
    img_path="tests/my_face.jpg",
    db_path="data/faces",
    model_name="ArcFace",
    detector_backend="opencv",
    distance_metric="cosine",
    enforce_detection=True
)

print(result)