
def likelihood_to_boolean(likelihood):
    if likelihood.value <= 2:
        return False
    return True

def check_if_face_detection_found_a_face(predicted_values):

    if len(predicted_values) == 0:
        return False, "{messages.face_not_found}"

    if len(predicted_values) > 1:
        return False, "{messages.too_many_faces}."

    predicted_values = predicted_values[0]

    if predicted_values['detection_confidence'] < 0.6:
        return False, "{messages.face_not_found}"
    
    if likelihood_to_boolean(predicted_values['headwear_likelihood']):
        return False, "{messages.accessory_found}"

    if likelihood_to_boolean(predicted_values['blurred_likelihood']):
        return False, "{messages.blurred_image}"
    
    if predicted_values['detection_confidence'] >= 0.6:
        return True, "{messages.face_found}"

def check_if_image_contains_explicit_content(predicted_values):

    for value in predicted_values.values():
        if likelihood_to_boolean(value):
            return True, "{messages.explicit_content_found}"

    return False, "{messages.explicit_content_not_found}"

def check_if_user_input_matches_predicted_values(input_age, input_gender,predicted_age, predicted_gender):

    if input_age > (predicted_age + 5) or input_age < (predicted_age - 5): #default as 5 per request, but could be a flexible value
        return False, "{messages.age_does_not_match}"

    if input_gender.lower() != predicted_gender.value:
        return False, "{messages.gender_does_not_match}"

    return True, "{messages.image_ok}"