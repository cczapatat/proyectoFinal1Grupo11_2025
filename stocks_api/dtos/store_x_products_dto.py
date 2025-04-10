from dataclasses import dataclass, field

@dataclass
class ProductStockDTO:
    id : str = field(default=None)
    id_product: int = field(default=None)
    assigned_stock: int = field(default=None)

    def to_dict(self):
        return {
            'id': str(self.id),
            'product_id': str(self.id_product),
            'assigned_stock': int(self.assigned_stock)
        }

@dataclass
class StoreXProductsDTO:
    id_store: int = field(default=None)
    stocks: list[ProductStockDTO] = field(default_factory=list)

    def to_dict(self):
        return {
            'store_id': str(self.id_store),
            'stocks': [stock.to_dict() for stock in self.stocks]
        }