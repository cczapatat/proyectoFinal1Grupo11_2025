export class StoreDto {
  name: string;
  phone: string;
  email: string;
  address: string;
  capacity: number;
  state: string;
  security_level: string;

  id?: string;
  created_at?: Date;
  updated_at?: Date;

  constructor(
    name: string,
    phone: string,
    email: string,
    address: string,
    capacity: number,
    state: string,
    security_level: string,

    id?: string,
    created_at?: Date,
    updated_at?: Date,
  ) {
    this.name = name;
    this.phone = phone;
    this.email = email;
    this.address = address;
    this.capacity = capacity;
    this.state = state;
    this.security_level = security_level;

    this.id = id;
    this.created_at = created_at;
    this.updated_at = updated_at;
  }
}