from datetime import datetime
from sqlalchemy.exc import IntegrityError
from flask import jsonify, make_response

from ..config.db import db
from ..models.seller_model import Seller
from ..dtos.seller_dto import SellerDTO


class SellerRepository:

    @staticmethod
    def create_seller(seller_dto: SellerDTO) -> Seller:
        seller = Seller()
        seller.user_id = seller_dto.user_id
        seller.name = seller_dto.name
        seller.phone = seller_dto.phone
        seller.email = seller_dto.email
        seller.zone = seller_dto.zone
        seller.quota_expected = seller_dto.quota_expected
        seller.currency_quota = seller_dto.currency_quota
        seller.quartely_target = seller_dto.quartely_target
        seller.currency_target = seller_dto.currency_target
        seller.performance_recomendations = seller_dto.performance_recomendations
        seller.created_at = datetime.now()
        seller.updated_at = datetime.now()

        try:
            db.session.add(seller)
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

        return seller
    
    @staticmethod
    def get_seller_by_user_id(user_id: int) -> Seller:
        return Seller.query.filter_by(user_id=user_id).first()