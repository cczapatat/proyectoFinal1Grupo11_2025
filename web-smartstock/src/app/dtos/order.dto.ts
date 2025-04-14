export class ProductStockCreateDTO {
  constructor(
    public product_id: string,
    public units: number
  ) {}
}

export class OrderCreateDTO {
  constructor(
    public client_id: string,
    public delivery_date: string,
    public payment_method: string,
    public products: ProductStockCreateDTO[],
    public seller_id?: string,
  ) {}
}

export class ProductStockCreatedDTO extends ProductStockCreateDTO {
  constructor(
    public id: string,
    public order_id: string,
    public override product_id: string,
    public override units: number,
    public created_at: string,
    public updated_at: string,
  ) {
    super(product_id, units);
  }
}

export class OrderCreatedDTO extends OrderCreateDTO {
  constructor(
    public id: string,
    public override client_id: string,
    public override delivery_date: string,
    public override payment_method: string,
    public override products: ProductStockCreatedDTO[],
    public override seller_id: string,
    public state: string,
    public total_amount: number,
    public user_id: string,
    public created_at: string,
    public updated_at: string,
  ) {
    super(client_id, delivery_date, payment_method, products, seller_id);
  }
}