export class Product {
    id: string;
    manufacturer_id: string;
    name: string;
    description: string;
    category: string;
    unit_price: number;
    currency_price: string;
    is_promotion: boolean;
    discount_price?: number;
    expired_at: string | null;
    url_photo: string;
    store_conditions: string;
    total_items?: number | null | undefined;

    public constructor(
        id: string,
        manufacturer_id: string,
        name: string,
        description: string,
        category: string,
        unit_price: number,
        currency_price: string,
        is_promotion: boolean = false,
        discount_price: number = 0,
        expired_at: string,
        url_photo: string,
        store_conditions: string,
        total_items: number | null | undefined = null
    ) {
        this.id = id;
        this.manufacturer_id = manufacturer_id;
        this.name = name;
        this.description = description;
        this.category = category;
        this.unit_price = unit_price;
        this.currency_price = currency_price;
        this.is_promotion = is_promotion;
        this.discount_price = is_promotion ? discount_price : 0;
        this.expired_at = expired_at ? new Date(expired_at).toISOString() : null;
        this.url_photo = url_photo;
        this.store_conditions = store_conditions;
        this.total_items = total_items;
    }
}
