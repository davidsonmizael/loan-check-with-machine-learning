from re import T
from google.cloud import vision
from base64 import b64decode

# Code taken and modified from:
# https://cloud.google.com/vision/docs/detecting-faces#detect_faces_in_a_remote_image
def detect_faces_base64(base64_image):
    """Detects faces in the base64 image provided."""
    client = vision.ImageAnnotatorClient()

    content = b64decode(base64_image)
    image = vision.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    faces_result = []

    for face in faces:
        vertices = ([f'({vertex.x},{vertex.y})' for vertex in face.bounding_poly.vertices])

        faces_result.append(
            {   
                "roll_angle": face.roll_angle,
                "tilt_angle": face.tilt_angle,
                "detection_confidence": face.detection_confidence,
                "landmarking_confidence": face.landmarking_confidence,
                "headwear_likelihood": face.headwear_likelihood,
                "blurred_likelihood": face.blurred_likelihood,
                "bounds": ','.join(vertices)
            })
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    
    return faces_result


# Code taken and modified from:
# https://cloud.google.com/vision/docs/detecting-safe-search#explicit_content_detection_on_a_remote_image
def detect_safe_search_base64(base64_image):
    """Detects unsafe features in the base64 image provided"""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    content = b64decode(base64_image)
    image = vision.Image(content=content)

    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    # more details on what each word means here:
    # https://cloud.google.com/vision/docs/reference/rpc/google.cloud.vision.v1#safesearchannotation
    predicted_result = {
        "adult": safe.adult,
        "medical": safe.medical,
        "spoofed": safe.spoof,
        "violence": safe.violence,
        "racy": safe.racy
    }

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return predicted_result