from .base_command import BaseCommand
from ..models.Models import Manufacturer


class GetAllManufacturer(BaseCommand):
    def __init__(self):
        super().__init__()

    def execute(self):
        return self.handle_query(lambda: [manufacturer.to_dict() for manufacturer in Manufacturer.query.all()])
