from core.integration.google_cloud import detect_faces_base64
from core.integration.google_cloud import detect_safe_search_base64

from core.integration.azure import predict_face_age_and_gender_base64
from core.integration.azure import get_face_landmarks_base64

from core.prediction_analysis import check_if_face_detection_found_a_face
from core.prediction_analysis import check_if_image_contains_explicit_content
from core.prediction_analysis import check_if_user_input_matches_predicted_values

def analyse_customer_selfie(customer_input, img_b64):
    face_detection_results, explicit_content_results = get_data_from_customer_picture(img_b64)

    is_safe, message = check_if_customer_selfie_is_safe(face_detection_results, explicit_content_results)
    
    predicted_age = predicted_gender = predicted_face = predicted_landmarks = None
    
    if is_safe:
        predicted_age, predicted_gender = predict_face_age_and_gender_base64(img_b64)
        predicted_face, predicted_landmarks = get_face_landmarks_base64(img_b64)
        is_safe, message = check_if_user_input_matches_predicted_values(customer_input['age'], customer_input['gender'], predicted_age, predicted_gender)

    return is_safe, message, predicted_age, predicted_gender, predicted_face, predicted_landmarks

def get_data_from_customer_picture(img_b64):
    
    face_detection_results = detect_faces_base64(img_b64)

    explicit_content_results = detect_safe_search_base64(img_b64)

    return face_detection_results, explicit_content_results

def check_if_customer_selfie_is_safe(face_detection_results, explicit_content_results):

    contains_explicit_content, explicit_content_result_message = check_if_image_contains_explicit_content(explicit_content_results)

    if contains_explicit_content:
        return False, explicit_content_result_message

    face_detection_approved, face_detection_message = check_if_face_detection_found_a_face(face_detection_results)

    if not face_detection_approved:
        return False, face_detection_message

    return True, "{messages.image_ok}"

