export interface Client {
  id: string;
  name: string;
  email: string;
  phone: string;
  zone: string;
  user_id: string;
  address: string;
  created_at: string;
  updated_at: string;
  client_type: string;
}

export interface PaginatedClients {
    data: Client[];
    page: number;
    per_page: number;
    total: number;
    total_pages: number;
  }