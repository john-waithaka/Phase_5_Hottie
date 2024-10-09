
# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from extensions import db
# from models.treatment import Treatment
# from models.user import User

# treatment_bp = Blueprint('treatment', __name__)

# # Create a new treatment
# @treatment_bp.route('/treatments', methods=['POST'])
# @jwt_required()
# def create_treatment():
#     data = request.get_json()
#     treatment_name = data.get('treatment_name')
#     description = data.get('description')
#     start_date = data.get('start_date')
#     patient_id = data.get('patient_id')
#     # therapist_id = data.get('therapist_id')
#     # patient_id = data.get('patient_id')
    
#     # therapist_id = current_user_id  # Assume logged-in user is the therapist

#     # Get the therapist ID from the currently logged-in user
#     therapist_id = get_jwt_identity()

#     if not treatment_name or not patient_id or not therapist_id:
#         return jsonify({"message": "Treatment name, patient, and therapist are required."}), 400

# # Verify that the current user is a therapist
#     therapist = User.query.get_or_404(therapist_id)
#     if therapist.user_type != 'therapist':
#         return jsonify({"message": "Only therapists can create treatments"}), 403

#     # Verify that the patient exists and is a patient
#     patient = User.query.get_or_404(patient_id)
#     if patient.user_type != 'patient':
#         return jsonify({"message": "Invalid patient ID"}), 400


#     new_treatment = Treatment(
#         treatment_name=treatment_name,
#         description=description,
#         patient_id=patient_id,
#         therapist_id=therapist_id,
#         start_date=start_date
#     )

#     db.session.add(new_treatment)
#     db.session.commit()

#     return jsonify({"message": "Treatment created successfully", "treatment": new_treatment.id}), 201

# # Get all treatments
# @treatment_bp.route('/treatments', methods=['GET'])
# @jwt_required()
# def get_treatments():
#     treatments = Treatment.query.all()
#     return jsonify([{
#         "id": treatment.id,
#         "treatment_name": treatment.treatment_name,
#         "description": treatment.description,
#         "patient_id": treatment.patient_id,
#         "therapist_id": treatment.therapist_id,
#         "start_date": treatment.start_date,
#         "end_date": treatment.end_date,
#         "is_active": treatment.is_active
#     } for treatment in treatments]), 200

# # Get treatment by ID
# @treatment_bp.route('/treatments/<id>', methods=['GET'])
# @jwt_required()
# def get_treatment(id):
#     treatment = Treatment.query.get_or_404(id)
#     return jsonify({
#         "id": treatment.id,
#         "treatment_name": treatment.treatment_name,
#         "description": treatment.description,
#         "patient_id": treatment.patient_id,
#         "therapist_id": treatment.therapist_id,
#         "start_date": treatment.start_date,
#         "end_date": treatment.end_date,
#         "is_active": treatment.is_active
#     }), 200

# # Update a treatment
# @treatment_bp.route('/treatments/<id>', methods=['PUT'])
# @jwt_required()
# def update_treatment(id):
#     treatment = Treatment.query.get_or_404(id)
#     data = request.get_json()

#     treatment.treatment_name = data.get('treatment_name', treatment.treatment_name)
#     treatment.description = data.get('description', treatment.description)
#     treatment.start_date = data.get('start_date', treatment.start_date)
#     treatment.end_date = data.get('end_date', treatment.end_date)
#     treatment.is_active = data.get('is_active', treatment.is_active)

#     db.session.commit()
#     return jsonify({"message": "Treatment updated successfully"}), 200

# # Delete a treatment
# @treatment_bp.route('/treatments/<id>', methods=['DELETE'])
# @jwt_required()
# def delete_treatment(id):
#     treatment = Treatment.query.get_or_404(id)
#     db.session.delete(treatment)
#     db.session.commit()
#     return jsonify({"message": "Treatment deleted successfully"}), 200





#NEW UPDATED TREATMENT ROUTE

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.treatment import Treatment
from models.user import User

treatment_bp = Blueprint('treatment', __name__)

# Create a new treatment
@treatment_bp.route('/treatments', methods=['POST'])
@jwt_required()
def create_treatment():
    data = request.get_json()
    treatment_name = data.get('treatment_name')
    description = data.get('description')
    start_date = data.get('start_date')
    patient_id = data.get('patient_id')

    # Get the therapist ID from the currently logged-in user
    therapist_id = get_jwt_identity()

    if not treatment_name or not patient_id or not therapist_id:
        return jsonify({"message": "Treatment name, patient, and therapist are required."}), 400

    # Verify that the current user is a therapist
    therapist = User.query.get_or_404(therapist_id)
    if therapist.user_type != 'therapist':
        return jsonify({"message": "Only therapists can create treatments"}), 403

    # Verify that the patient exists and is a patient
    patient = User.query.get_or_404(patient_id)
    if patient.user_type != 'patient':
        return jsonify({"message": "Invalid patient ID"}), 400

    new_treatment = Treatment(
        treatment_name=treatment_name,
        description=description,
        patient_id=patient_id,
        therapist_id=therapist_id,
        start_date=start_date
    )

    db.session.add(new_treatment)
    db.session.commit()

    return jsonify({"message": "Treatment created successfully", "treatment": new_treatment.id}), 201

# Get all treatments
@treatment_bp.route('/treatments', methods=['GET'])
@jwt_required()
def get_treatments():
    treatments = Treatment.query.all()
    return jsonify([{
        "id": treatment.id,
        "treatment_name": treatment.treatment_name,
        "description": treatment.description,
        "patient_id": treatment.patient_id,
        "therapist_id": treatment.therapist_id,
        "start_date": treatment.start_date,
        "end_date": treatment.end_date,
        "is_active": treatment.is_active
    } for treatment in treatments]), 200

# Get treatment by ID
@treatment_bp.route('/treatments/<int:id>', methods=['GET'])
@jwt_required()
def get_treatment(id):
    treatment = Treatment.query.get_or_404(id)
    return jsonify({
        "id": treatment.id,
        "treatment_name": treatment.treatment_name,
        "description": treatment.description,
        "patient_id": treatment.patient_id,
        "therapist_id": treatment.therapist_id,
        "start_date": treatment.start_date,
        "end_date": treatment.end_date,
        "is_active": treatment.is_active
    }), 200

# Update a treatment
@treatment_bp.route('/treatments/<int:id>', methods=['PUT'])
@jwt_required()
def update_treatment(id):
    treatment = Treatment.query.get_or_404(id)
    data = request.get_json()

    treatment.treatment_name = data.get('treatment_name', treatment.treatment_name)
    treatment.description = data.get('description', treatment.description)
    treatment.start_date = data.get('start_date', treatment.start_date)
    treatment.end_date = data.get('end_date', treatment.end_date)
    treatment.is_active = data.get('is_active', treatment.is_active)

    db.session.commit()
    return jsonify({"message": "Treatment updated successfully"}), 200

# Delete a treatment
@treatment_bp.route('/treatments/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_treatment(id):
    treatment = Treatment.query.get_or_404(id)
    db.session.delete(treatment)
    db.session.commit()
    return jsonify({"message": "Treatment deleted successfully"}), 200
