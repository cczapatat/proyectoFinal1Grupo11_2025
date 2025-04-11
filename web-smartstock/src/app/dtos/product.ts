export class ProductDto {
    constructor(
        public category: string,
        public created_at: Date,
        public currency_price: string,
        public description: string,
        public discount_price: number,
        public expired_at: Date,
        public id: string,
        public is_promotion: boolean,
        public manufacturer_id: string,
        public name: string,
        public store_conditions: string,
        public unit_price: number,
        public updated_at: Date,
        public url_photo: string
    ) {}
}

export interface PaginatedProducts {
    data: ProductDto[];
    page: number;
    per_page: number;
    total: number;
    total_pages: number;
}