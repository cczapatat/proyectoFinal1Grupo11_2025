export interface AssignedStock {
    assigned_stock: number;
    id: string;
    product_id: string;
}

export interface AssignedStockDto {
    stocks: AssignedStock[];
    store_id: string;
}