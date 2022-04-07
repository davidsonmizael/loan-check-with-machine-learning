import re
import base64
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face.models import Coordinate

def clear_base64(base64_data):
    return re.sub('^data:image/.+;base64,', '', base64_data)

def base64_to_image_object(base64_image):

    image_data = clear_base64(base64_image)
    return BytesIO(base64.b64decode(image_data))

def add_azure_landmarks_to_base64_image(base64_image, landmarks_rect, landmarks_dots):

    def get_landmark_retangle(face_rectangle):
        rect = face_rectangle
        left = rect.left
        top = rect.top
        right = left + rect.width
        bottom = top + rect.height
        
        return ((left, top), (right, bottom))

    #print(landmarks_dots)
    img = Image.open(base64_to_image_object(base64_image))
    draw = ImageDraw.Draw(img)
    draw.rectangle(get_landmark_retangle(landmarks_rect), outline='red')
    for attr in vars(landmarks_dots):
        dot = getattr(landmarks_dots, attr)

        if isinstance(dot, Coordinate):
            draw.ellipse((dot.x, dot.y, dot.x+2, dot.y+2), fill='red')

    buffered = BytesIO()
    img.save(buffered, format="JPEG")

    return clear_base64(base64.b64encode(buffered.getvalue()).decode())
    


