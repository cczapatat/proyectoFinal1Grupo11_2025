from .base_command import BaseCommand
from ..models.Models import Manufacturer


class GetPaginateManufacturer(BaseCommand):
    def __init__(self, page: int, per_page: int):
        super().__init__()
        self.page = page
        self.per_page = per_page

    def execute(self):
        return self.handle_query(lambda: [manufacturer.to_dict() for manufacturer in
                                          Manufacturer.query.order_by(Manufacturer.name)
                                 .paginate(page=self.page, per_page=self.per_page, error_out=False)])
