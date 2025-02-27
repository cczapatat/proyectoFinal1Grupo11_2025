import os
import gc
import uuid
from flask import Blueprint, jsonify, request, send_file
from werkzeug.exceptions import NotFound, BadRequest, Unauthorized

from ..utils import get_extension
from ..dtos.document_dto import DocumentDTO
from ..infrastructure.document_repository import DocumentRepository
from ..infrastructure.cloud_storage_repository import CloudStorageRepository

bp = Blueprint('document', __name__, url_prefix='/document-manager/document')

internal_token = os.getenv('INTERNAL_TOKEN', default='internal_token')

document_repository = DocumentRepository()
cloud_storage_repository = CloudStorageRepository(bucket_name=os.getenv('GCLOUD_BUCKET', default='massive_proyecto_final'))


def there_is_token():
    token = request.headers.get('x-token', None)

    if token is None:
        raise Unauthorized(description='authorization required')

    if token != internal_token:
        raise Unauthorized(description='authorization required')


@bp.route('/', methods=('POST',))
@bp.route('/create', methods=('POST',))
def create_document():
    there_is_token()
    user_id = request.headers.get('user-id', None)

    if user_id is None:
        return jsonify({'message': 'user-id is required'}), 400

    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if get_extension(file.filename) not in ['csv']:
        return jsonify({'message': 'Invalid file extension'}), 400

    file_name, destination_blob_name = cloud_storage_repository.generate_path(full_file_name=file.filename)
    bucket_path_result = cloud_storage_repository.upload_file(file, destination_blob_name)
    gc.collect()

    if bucket_path_result is None:
        return jsonify({'message': 'Error uploading file'}), 500

    document_dto = DocumentDTO(
        user_id=user_id,
        file_name=file_name,
        path_source=destination_blob_name,
    )
    document = document_repository.add_document_from_user(document_dto=document_dto)

    return jsonify(document.to_dict()), 201


def _get_document_by_id(id_document: str):
    there_is_token()

    try:
        uuid.UUID(id_document)
    except ValueError:
        raise BadRequest(description='Invalid document id')

    document = document_repository.get_document(document_id=id_document)

    if document is None:
        raise NotFound(description='Document not found')

    return document


@bp.route('/<id_document>', methods=('GET',))
def get_document_by_id(id_document: str):
    document = _get_document_by_id(id_document=id_document)

    return jsonify(document.to_dict()), 200


@bp.route('/<id_document>/file', methods=('GET',))
def get_document_file_by_id(id_document: str):
    document = _get_document_by_id(id_document=id_document)

    buffer, content_type = cloud_storage_repository.download_file(destination_blob_name=document.path_source)

    if buffer:
        return send_file(buffer, mimetype=content_type, as_attachment=True, download_name=document.file_name)
    else:
        return jsonify({"error": "Download fail"}), 409
