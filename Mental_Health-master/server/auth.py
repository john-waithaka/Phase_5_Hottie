from flask import Blueprint, request, jsonify
from extensions import db, bcrypt
from models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from models.tokenblacklist import TokenBlacklist

auth_bp = Blueprint('auth', __name__)



@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    user_type = data.get('user_type')  # Should be either 'Patient' or 'Therapist'

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered'}), 400
    

    new_user = User(
        email=email,
        full_name=full_name,
        password=password,  # Use the hashed password here
        user_type=user_type
    )
    
    print(f' is hashed : {new_user.check_password(password)}')
    
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.id)
    return jsonify(access_token=access_token), 201



@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    
    print(user)
    print(f'saved hash {user.password_hash}')
    print(f"received password hashed {user.check_password(password)}")
    
    if user:
        if not bcrypt.check_password_hash(user.password_hash, password):  # Fix variable name for password check
            return jsonify({'message': 'Invalid email or password'}), 401
    else:
        return jsonify({'message': 'user not found!'}), 401

    access_token = create_access_token(identity=user.id) # Store user ID in JWT
    return jsonify({'access_token': access_token}), 200



@auth_bp.route('/logout', methods=['POST'])
@jwt_required()  # Ensure the user is logged in with a valid JWT
def logout():
    try:
        jti = get_jwt()["jti"]  # Get the JWT's unique identifier (JTI)
        
        #Warui added this to check if token had been blacklisted
        token_exists = TokenBlacklist.query.filter_by(token=jti).first()        
        if token_exists:
            return jsonify({'message': 'Token already blacklisted'}), 200
        
        blacklisted_token = TokenBlacklist(token=jti)
        db.session.add(blacklisted_token)
        db.session.commit()

        return jsonify({'message': 'Logout successful. Token has been blacklisted.'}), 200

    except Exception as e:
        return jsonify({'message': f'An error occurred during logout: {str(e)}'}), 500
