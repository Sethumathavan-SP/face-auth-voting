import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
face_app = FaceAnalysis(name="buffalo_l", providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
face_app.prepare(ctx_id=0)
def check_similarity(image1_blob, image2_bgr):
    image1_array = np.frombuffer(image1_blob, np.uint8)
    img1 = cv2.imdecode(image1_array, cv2.IMREAD_COLOR)
    faces1 = face_app.get(img1)
    faces2 = face_app.get(image2_bgr)
    if not faces1 or not faces2:
        print("no face detected")
        return 0
    emb1 = faces1[0].embedding
    emb2 = faces2[0].embedding
    sim = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
    return sim * 100
