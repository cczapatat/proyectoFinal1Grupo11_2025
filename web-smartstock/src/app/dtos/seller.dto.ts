export interface SellerDTO {
    id?: string;
    name: string;
    phone: string;
    email: string;
    password: string;
    user_id?: string;
    type: string; 
    zone: string;
    quota_expected: number;
    currency_quota: string;
    quartely_target: number;
    currency_target: string;
    performance_recomendations: string;
    created_at?: string;
    updated_at?: string;
  }

export interface PaginatedSellers {
    data: SellerDTO[];
    page: number;
    per_page: number;
    total: number;
    total_pages: number;
  }