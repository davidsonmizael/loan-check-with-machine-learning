from flask import current_app
from flask import Blueprint, jsonify, request
from core.locale import get_message
from core.database import db
from datetime import datetime
from core.applyance_analysis import analyse_customer_selfie
from core.image_manipulation import add_azure_landmarks_to_base64_image
from core.integration.azure import transform_face_landmarks_on_dict

from sqlalchemy import Column, Integer, String
class CreditAnalysisSubmission(db.Model):
    __tablename__ = "credit_analysis_submission"
    submission_id = Column(Integer, primary_key=True, autoincrement=True)
    create_date = Column(String)
    name = Column(String)
    age = Column(Integer)
    networth = Column(String)
    ethnicity = Column(String)
    gender = Column(String)
    house_owner = Column(Integer)
    side_income = Column(Integer)
    marital_status = Column(String)
    scorlarship = Column(String)
    selfie_image = Column(String)
    selfie_image_with_landmarks = Column(String)
    selfie_calculated_landmarks = Column(String)
    selfie_calculated_facial_features = Column(String)
    image_safe = Column(Integer)
    image_analysis_result = Column(String)
    predicted_age = Column(Integer)
    predicted_gender = Column(String)

blueprint = Blueprint('credit_analysis_handler', __name__)

@blueprint.route("/submit_credit_analysis", methods=["POST"])
def submit_credit_analysis():

    required_fields = [
        'language', 'name', 'age', 
        'networth', 'ethnicity', 'gender', 
        'house_owner', 'side_income', 
        'marital_status', 'scorlarship',
        'selfie_image']

    body = request.json

    diff = body.keys() ^ required_fields
    if diff:
        language = body['language'] if 'language' in body else 'en-EN'

        message = get_message(language, "{message.api_fields_does_not_match}")
        current_app.logger.error(f"Error: '{message}' Payload: {body}")
        return jsonify(status="FAIL", message=message)

    else:

        language = body['language'] if 'language' in body else 'en-EN'
        
        is_image_safe, message, predicted_age, predicted_gender, predicted_facebox, predicted_facial_features = analyse_customer_selfie(body, body['selfie_image'])

        message = get_message(language, message)

        cas = CreditAnalysisSubmission()
        cas.create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cas.age = body['age']
        cas.name = body['name']
        cas.networth = body['networth']
        cas.ethnicity = body['ethnicity']
        cas.gender = body['gender']
        cas.house_owner = body['house_owner']
        cas.side_income = body['side_income']
        cas.marital_status = body['marital_status']
        cas.scorlarship = body['scorlarship']
        cas.selfie_image = body['selfie_image']
        cas.image_safe = is_image_safe
        cas.image_analysis_result = message
        cas.predicted_age = predicted_age
        cas.predicted_gender = predicted_gender.value if predicted_gender else None
        cas.selfie_calculated_landmarks = str(predicted_facebox) if predicted_facebox else None
        cas.selfie_calculated_facial_features = str(transform_face_landmarks_on_dict(predicted_facial_features)) if predicted_facial_features else None

        image_with_landmarks = None
        if is_image_safe and predicted_facebox and predicted_facial_features: 
            image_with_landmarks = add_azure_landmarks_to_base64_image(body['selfie_image'], predicted_facebox, predicted_facial_features)
            cas.selfie_image_with_landmarks = str(image_with_landmarks)

        db.session.add(cas)
        db.session.commit()

        if image_with_landmarks:
            return jsonify(status="OK", language=language, is_image_approved=is_image_safe, image_with_landmarks=image_with_landmarks)
        else:
            return jsonify(status="OK", language=language, is_image_approved=is_image_safe, message=message)
