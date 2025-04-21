import csv
import io
import os
import requests

x_token = os.getenv('INTERNAL_TOKEN', 'internal_token')
host_document_manager = os.getenv('DOCUMENT_MANAGER_PATH', 'http://localhost:3003')

headers = {'x-token': x_token}
class DocumentManagerService:
    def get_json_from_document(self, file_id):
        url = f"{host_document_manager}/document-manager/document/{file_id}/file"
        print(f"[Get Document] Fetching file from {url}")
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"[Get Document] Failed to fetch file, status code: {response.status_code}")
            return None

        csv_content = response.text
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        return [row for row in csv_reader]