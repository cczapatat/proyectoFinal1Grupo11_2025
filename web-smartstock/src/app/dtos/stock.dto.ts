import { Product } from '../product/product';

export interface ProductStockDTO {
  id: string;
  quantity_in_stock: number;
  last_quantity: number;
  product: Product;
  enabled: boolean;
  update_date: string;
  creation_date: string;
}

export interface ProductStockPaginateDTO {
  page: number;
  per_page: number;
  total: number;
  stocks: ProductStockDTO[];
}
