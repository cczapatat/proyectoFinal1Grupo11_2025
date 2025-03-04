import csv
import io
import uuid
from datetime import datetime

def process_bulk_file(file_bytes: bytes):
    file_str = file_bytes.decode("utf-8")
    reader = csv.DictReader(io.StringIO(file_str))
    rows = []
    for row in reader:
        if row.get("quantity_in_stock", "").strip().lower() == "quantity_in_stock":
            continue
        try:
            quantity_in_stock = int(row.get("quantity_in_stock", 0))
        except ValueError:
            continue
        product_name = row.get("product_name", "").strip()
        if not product_name:
            continue
        row_dict = {
            "id": str(uuid.uuid4()),
            "product_name": product_name,
            "quantity_in_stock": quantity_in_stock,
            "last_quantity": quantity_in_stock,
            "enabled": True,
            "update_date": datetime.utcnow(),
            "creation_date": datetime.utcnow()
        }
        rows.append(row_dict)
    return rows