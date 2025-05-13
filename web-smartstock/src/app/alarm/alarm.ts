export class Alarm {
    id: string;
    manufacture_id: string;
    product_id: string;
    minimum_value: number | null;
    maximum_value: number | null;
    notes: string;

    public constructor(
        id: string,
        manufacture_id: string,
        product_id: string,
        min_value: number = 1,
        max_value: number = 0,
        notes: string
    ) {
        this.id = id;
        this.manufacture_id = manufacture_id;
        this.product_id = product_id;
        this.minimum_value = Number(min_value);
        this.maximum_value = Number(max_value);
        this.notes = notes;
    }
}
