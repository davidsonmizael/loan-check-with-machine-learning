import os
from core.http_handler import post_request

from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import Coordinate
from msrest.authentication import CognitiveServicesCredentials

from core.image_manipulation import base64_to_image_object

def predict_face_age_and_gender_base64(base64_image):

    face_client = FaceClient(os.getenv("AZ_IR_ENDPOINT"), CognitiveServicesCredentials(os.getenv("AZ_KEY")))

    im = base64_to_image_object(base64_image)
    detected_faces = face_client.face.detect_with_stream(im, detection_model='detection_01', return_face_attributes=['age','gender'])
    if not detected_faces:
        raise Exception('No face detected from image')

    if len(detected_faces) > 1:
        raise Exception('Multiple faces detected in image')
    
    face = detected_faces[0]

    return face.face_attributes.age, face.face_attributes.gender

def get_face_landmarks_base64(base64_image):

    face_client = FaceClient(os.getenv("AZ_IR_ENDPOINT"), CognitiveServicesCredentials(os.getenv("AZ_KEY")))

    im = base64_to_image_object(base64_image)
    detected_faces = face_client.face.detect_with_stream(im, detection_model='detection_01', return_face_landmarks=True)

    if not detected_faces:
        raise Exception('No face detected from image')

    if len(detected_faces) > 1:
        raise Exception('Multiple faces detected in image')
    
    face = detected_faces[0]

    return face.face_rectangle, face.face_landmarks

def transform_face_landmarks_on_dict(face_landmarks):

    output_dict = {}

    for attr in vars(face_landmarks):
        dot = getattr(face_landmarks, attr)

        if isinstance(dot, Coordinate):
            output_dict[attr] = {"x": dot.x, "y": dot.y}

    return output_dict

def call_credit_predict_model_api(model_api, request_data):

    headers = {
        "Content-Type": "application/json"
    }

    data =  {
        "data": request_data,
        "method": "predict"
    }

    result = post_request(model_api, headers=headers, data=data)
    try:
        response = result['content']['predict'][0]
        return response
    except:
        raise Exception(f"Request failed. Response: {result}")