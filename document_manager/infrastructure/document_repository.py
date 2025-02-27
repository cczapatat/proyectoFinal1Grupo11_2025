from datetime import datetime

from ..config.db import db
from ..models.document_model import Document
from ..dtos.document_dto import DocumentDTO


class DocumentRepository:

    @staticmethod
    def add_document_from_user(document_dto: DocumentDTO) -> Document:
        document = Document()
        document.user_id = document_dto.user_id
        document.file_name = document_dto.file_name
        document.path_source = document_dto.path_source
        document.created_at = datetime.now()
        document.updated_at = datetime.now()

        db.session.add(document)
        db.session.commit()

        return document

    @staticmethod
    def get_document(document_id: str) -> Document | None:
        document = db.session.query(Document).filter_by(id=document_id).one_or_none()

        return document
