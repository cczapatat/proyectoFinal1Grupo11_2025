
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from ..config.db import db


class ClientSeller(db.Model):
    __tablename__ = 'client_seller'

    client_id = Column(UUID(as_uuid=True), ForeignKey('clients.id'), primary_key=True)
    seller_id = Column(UUID(as_uuid=True), primary_key=True)

    # Use string references for the relationships
    client = relationship("Client", back_populates="seller_association")

    def __init__(self, client_id, seller_id):
        self.client_id = client_id
        self.seller_id = seller_id