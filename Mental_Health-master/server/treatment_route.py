


#NEW UPDATED TREATMENT ROUTE

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.treatment import Treatment
from models.user import User



treatment_bp = Blueprint('treatment', __name__)

# # Create a new treatment
# @treatment_bp.route('/treatments', methods=['POST'])
# @jwt_required()
# def create_treatment():
    
#     #added code therapist sumbua error
#     therapist_id = get_jwt_identity()
#     print(f"Therapist ID from JWT: {therapist_id}")
    
#     therapist = User.query.get_or_404(therapist_id)
#     print(f"Therapist user type: {therapist.user_type}")
#     print(f"Therapist full details: {therapist.__dict__}")
    
    
#     data = request.get_json()
#     treatment_name = data.get('treatment_name')
#     description = data.get('description')
#     start_date = data.get('start_date')
#     patient_id = data.get('patient_id')
    
#     print(f"Received data: {data}")


#     # Get the therapist ID from the currently logged-in user
#     therapist_id = get_jwt_identity()

#     if not treatment_name or not patient_id or not therapist_id:
#         return jsonify({"message": "Treatment name, patient, and therapist are required."}), 400

#     # Verify that the current user is a therapist
#     therapist = User.query.get_or_404(therapist_id)
#     if therapist.user_type != 'Therapist':
#         return jsonify({"message": "Only therapists can create treatments"}), 403

#     # Verify that the patient exists and is a patient
#     patient = User.query.get_or_404(patient_id)
#     if patient.user_type != 'Patient':
#         return jsonify({"message": "Invalid patient ID"}), 400
    
    
#     #NEW
#     #added patient query - sumbua error
#     patient = User.query.get_or_404(patient_id)
#     print(f"Patient query result: {patient.__dict__}")


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


# Create a new treatment
@treatment_bp.route('/treatments', methods=['POST'])
@jwt_required()
def create_treatment():
    try:
        # Get therapist ID from JWT
        therapist_id = get_jwt_identity()
        print(f"Therapist ID from JWT: {therapist_id}")

        # Ensure therapist exists
        therapist = User.query.get(therapist_id)
        if not therapist:
            return jsonify({
                "error": {
                    "code": 404,
                    "message": "Therapist not found."
                }
            }), 404

        # Check if the user is indeed a therapist
        if therapist.user_type != 'Therapist':
            return jsonify({
                "error": {
                    "code": 403,
                    "message": "Unauthorized: Only therapists can create treatments."
                }
            }), 403

        # Get request data
        data = request.get_json()
        print(f"Received data: {data}")

        # Extract fields from the request
        treatment_name = data.get('treatment_name')
        description = data.get('description')
        start_date = data.get('start_date')
        patient_id = data.get('patient_id')

        # Validate required fields
        if not treatment_name or not description or not patient_id:
            return jsonify({
                "error": {
                    "code": 400,
                    "message": "Missing required fields: treatment_name, description, and patient_id."
                }
            }), 400

        # Ensure the patient exists
        patient = User.query.get(patient_id)
        if not patient:
            return jsonify({
                "error": {
                    "code": 404,
                    "message": f"Patient with ID {patient_id} not found."
                }
            }), 404

        # Ensure the patient is of the correct user type
        if patient.user_type != 'Patient':
            return jsonify({
                "error": {
                    "code": 400,
                    "message": f"User with ID {patient_id} is not a patient."
                }
            }), 400

        # Validate the start_date (if provided)
        if start_date:
            try:
                # Assume start_date is in ISO 8601 format, convert to date
                datetime.strptime(start_date, '%Y-%m-%d')
            except ValueError:
                return jsonify({
                    "error": {
                        "code": 400,
                        "message": "Invalid start_date format. Expected YYYY-MM-DD."
                    }
                }), 400

        # Create the new treatment
        new_treatment = Treatment(
            treatment_name=treatment_name,
            description=description,
            patient_id=patient_id,
            therapist_id=therapist_id,
            start_date=start_date
        )

        # Add and commit to the database
        db.session.add(new_treatment)
        db.session.commit()

        return jsonify({
            "message": "Treatment created successfully",
            "treatment": {
                "id": new_treatment.id,
                "treatment_name": new_treatment.treatment_name,
                "description": new_treatment.description,
                "patient_id": new_treatment.patient_id,
                "therapist_id": new_treatment.therapist_id,
                "start_date": new_treatment.start_date,
                "is_active": new_treatment.is_active
            }
        }), 201

    except SQLAlchemyError as e:
        # Handle database errors
        db.session.rollback()  # Rollback in case of an error
        print(f"Database error: {str(e)}")
        return jsonify({
            "error": {
                "code": 500,
                "message": "A database error occurred while creating the treatment.",
                "details": str(e)
            }
        }), 500

    except Exception as e:
        # Handle all other unforeseen errors
        print(f"Unexpected error: {str(e)}")
        return jsonify({
            "error": {
                "code": 500,
                "message": "An unexpected error occurred.",
                "details": str(e)
            }
        }), 500




# Get all treatments
@treatment_bp.route('/treatments', methods=['GET'])
@jwt_required()
def get_treatments():
    try:
        treatments = Treatment.query.all()  # Fetch all treatments
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
    except Exception as e:  # Catch any exceptions that may arise
        print(f"Error occurred while retrieving treatments: {str(e)}")  # Log the error
        return jsonify({"message": "An error occurred while retrieving treatments."}), 500  # Return a 500 Internal Server Error






# Get treatment by ID
@treatment_bp.route('/treatments/<string:treatment_id>', methods=['GET'])  # Change to <string:treatment_id>
@jwt_required()
def get_treatment(treatment_id):  # Use treatment_id here
    
    print(f"Requested treatment ID: {treatment_id}")  # Log the ID received
    treatment = Treatment.query.get(treatment_id)  # Use treatment_id to query
    
    # Check if treatment exists
    if treatment is None:
        print(f"Treatment with ID {treatment_id} not found.")  # Log not found
        return jsonify({"message": "Treatment not found."}), 404
    
    # If treatment exists, return details
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





# Update treatment by ID
@treatment_bp.route('/treatments/<string:id>', methods=['PUT'])
@jwt_required()
def update_treatment(id):
    data = request.get_json()
    treatment = Treatment.query.get(id)

    if treatment is None:
        return jsonify({
            "error": {
                "code": 404,
                "message": f"Treatment with ID {id} not found."
            }
        }), 404

    # Update the treatment fields
    treatment.treatment_name = data.get('treatment_name', treatment.treatment_name)
    treatment.description = data.get('description', treatment.description)
    treatment.patient_id = data.get('patient_id', treatment.patient_id)
    treatment.start_date = data.get('start_date', treatment.start_date)
    treatment.end_date = data.get('end_date', treatment.end_date)
    treatment.is_active = data.get('is_active', treatment.is_active)

    db.session.commit()  # Commit the changes to the database

    return jsonify({
        "message": "Treatment updated successfully.",
        "treatment": {
            "id": treatment.id,
            "treatment_name": treatment.treatment_name,
            "description": treatment.description,
            "patient_id": treatment.patient_id,
            "therapist_id": treatment.therapist_id,
            "start_date": treatment.start_date,
            "end_date": treatment.end_date,
            "is_active": treatment.is_active
        }
    }), 200




# Delete a treatment by ID
@treatment_bp.route('/treatments/<string:id>', methods=['DELETE'])
@jwt_required()
def delete_treatment(id):
    treatment = Treatment.query.get(id)  # Use get to handle the treatment

    if treatment is None:
        return jsonify({
            "error": {
                "code": 404,
                "message": f"Treatment with ID {id} not found."
            }
        }), 404

    # Soft delete
    treatment.is_active = False
    db.session.commit()
    return jsonify({"message": "Treatment deleted successfully."}), 200






# Restore a treatment by ID
@treatment_bp.route('/treatments/<string:id>/restore', methods=['PUT'])
@jwt_required()
def restore_treatment(id):
    # Fetch the treatment by ID, including soft-deleted records
    treatment = Treatment.query.filter_by(id=id, is_active=False).first()

    # Check if the treatment exists and is soft-deleted
    if treatment is None:
        return jsonify({
            "error": {
                "code": 404,
                "message": f"Treatment with ID {id} not found or already active."
            }
        }), 404

    # Restore the treatment
    treatment.is_active = True
    db.session.commit()

    return jsonify({
        "message": "Treatment restored successfully.",
        "treatment": {
            "id": treatment.id,
            "treatment_name": treatment.treatment_name,
            "description": treatment.description,
            "patient_id": treatment.patient_id,
            "therapist_id": treatment.therapist_id,
            "start_date": treatment.start_date,
            "end_date": treatment.end_date,
            "is_active": treatment.is_active
        }
    }), 200
