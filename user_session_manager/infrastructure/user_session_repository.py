from datetime import datetime
from sqlalchemy.exc import IntegrityError
from flask import jsonify, make_response

from ..config.db import db
from ..models.user_session_model import UserSession
from ..dtos.user_session_dto import UserSessionDTO

import bcrypt


class UserSessionRepository:

    @staticmethod
    def create_user_session(user_session_dto: UserSessionDTO) -> UserSession:

        #validate if the session already exists
        existing_user_session = UserSession.query.filter_by(email=user_session_dto.email).first()
       
        if existing_user_session:
            return existing_user_session

        user_session = UserSession()
        user_session.email = user_session_dto.email
        user_session.password = bcrypt.hashpw(user_session_dto.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user_session.type = user_session_dto.type
        user_session.created_at = datetime.now()
        user_session.updated_at = datetime.now()

        try:
            db.session.add(user_session)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            response = make_response(
                jsonify({"error": "Integrity error", "message": str(e.orig)}), 400
            )
            return response
        except Exception as e:
            db.session.rollback()
            response = make_response(
                jsonify({"error": "Internal server error", "message": str(e)}), 500
            )
            return response

        return user_session
    
    @staticmethod
    def get_user_session_by_credentials(email: str, password: str) -> UserSession:
        user_session = UserSession.query.filter_by(email=email).first()

        if user_session is None or bcrypt.checkpw(password.encode('utf-8'), user_session.password.encode('utf-8')) is False:
            return None
        
        return user_session