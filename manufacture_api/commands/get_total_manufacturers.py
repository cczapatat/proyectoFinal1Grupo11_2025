from .base_command import BaseCommand
from ..models.Models import Manufacturer


class GetTotalManufacturers(BaseCommand):
    def __init__(self):
        super().__init__()

    def execute(self):
        return self.handle_query(lambda: Manufacturer.query.count())
