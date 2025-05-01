from .base_command import BaseCommand
from ..errors.errors import ApiError
from ..models.Models import db, BulkTask
import traceback


class ResetBulkTask(BaseCommand):
    def execute(self):
        try:
            db.session.query(BulkTask).delete()
            db.session.commit()
        except Exception as e:
            traceback.print_exc()
            raise ApiError(e)