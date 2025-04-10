export interface Seller {
  id: string;
  name: string;
  email: string;
  phone: string;
  zone: string;
  currency_quota: string;
  currency_target: string;
  quartely_target: number;
  quota_expected: number;
  performance_recomendations: string;
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface PaginatedSellers {
    data: Seller[];
    page: number;
    per_page: number;
    total: number;
    total_pages: number;
  }