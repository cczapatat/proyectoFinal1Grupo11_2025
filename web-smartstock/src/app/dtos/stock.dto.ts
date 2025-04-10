export interface ProductStockDTO {
  id: string;
  product_name: string;
  quantity_in_stock: number;
  last_quantity: number;
  enabled: boolean;
  update_date: string;
  creation_date: string;
}