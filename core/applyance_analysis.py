import os
import random

from core.integration.google_cloud import detect_faces_base64
from core.integration.google_cloud import detect_safe_search_base64

from core.integration.azure import predict_face_age_and_gender_base64
from core.integration.azure import get_face_landmarks_base64
from core.integration.azure import call_credit_predict_model_api

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
        gender = "Male" if customer_input['gender'] else "Female"
        is_safe, message = check_if_user_input_matches_predicted_values(customer_input['age'], gender, predicted_age, predicted_gender)

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

def analyse_customer_eligibility(customer_input, base64):

    credit_approved = False

    model_with_ethnicity_url = os.getenv('AZ_MODEL1')
    model_without_ethnicity_url = os.getenv('AZ_MODEL2')

    is_safe, message, predicted_age, predicted_gender, predicted_face, predicted_landmarks = analyse_customer_selfie(customer_input, base64)

    prediction_with_ethnicity = prediction_without_ethnicity = None
    if is_safe: 
        prediction_with_ethnicity = call_credit_predict_model_api(model_with_ethnicity_url, __transform_customer_input_to_match_azure_fields(customer_input, ethnicity=True))
        prediction_without_ethnicity = call_credit_predict_model_api(model_without_ethnicity_url, __transform_customer_input_to_match_azure_fields(customer_input, ethnicity=False))
        
        if prediction_with_ethnicity == 0 and prediction_without_ethnicity == 0:
            credit_approved = True
            message = "{messages.credit_approved}"
        else:
            message = "{messages.credit_not_approved}"
    
    return is_safe, credit_approved, prediction_with_ethnicity, prediction_without_ethnicity, message, predicted_age, predicted_gender, predicted_face, predicted_landmarks
    
def __transform_customer_input_to_match_azure_fields(customer_input, ethnicity=False):
    index = random.randint(1,10000)
    azure_input = {}
    azure_input['renda'] = {f"{index}": customer_input['networth']}
    azure_input['idade'] = {f"{index}": customer_input['age']}
    azure_input['gender'] = {f"{index}": customer_input['gender']}
    azure_input['casapropria'] = {f"{index}": customer_input['house_owner']}
    azure_input['outrasrendas'] = {f"{index}": customer_input['side_income']}
    azure_input['estadocivil'] = {f"{index}": customer_input['marital_status']}
    azure_input['escolaridade'] = {f"{index}": customer_input['scorlarship']}

    if ethnicity:
        azure_input['etnia'] = {f"{index}": customer_input['ethnicity']}

    return azure_input