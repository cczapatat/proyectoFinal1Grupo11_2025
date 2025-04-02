export class Manufacturer {
    id: string;
    name: string;
    address: string;
    phone: string;
    email: string;
    country: string;
    tax_conditions: string;
    legal_conditions: string;
    rating_quality: number;

    public constructor(
        id: string,
        name: string,
        address: string,
        phone: string,
        email: string,
        country: string,
        tax_conditions: string,
        legal_conditions: string,
        rating_quality: number,
    ) {
        this.id = id;
        this.name = name;
        this.address = address;
        this.phone = phone;
        this.email = email;
        this.country = country;
        this.tax_conditions = tax_conditions;
        this.legal_conditions = legal_conditions;
        this.rating_quality = rating_quality;
    }
}
