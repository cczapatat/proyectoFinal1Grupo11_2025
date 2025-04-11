export class StoreDto {
  constructor(
    public name: string,
    public phone: string,
    public email: string,
    public address: string,
    public capacity: number,
    public state: string,
    public security_level: string,
    public id?: string,
    public created_at?: Date,
    public updated_at?: Date,
  ) {}
}

export interface PaginatedStores {
  data: StoreDto[];
  page: number;
  per_page: number;
  total: number;
  total_pages: number;
}
