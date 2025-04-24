export class BulkTask {
    constructor(
        public created_at: Date,
        public file_id: string,
        public id: string,
        public status: string,
        public updated_at: Date,
    ) {}
}