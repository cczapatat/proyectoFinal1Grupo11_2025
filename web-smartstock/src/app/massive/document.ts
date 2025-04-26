export class Document {
    id: string;
    file_name: string;
    path_source: string;
    user_id: string;
    created_at: string;
    updated_at: string;

    public constructor(
        id: string,
        file_name: string,
        path_source: string,
        user_id: string,
        created_at: string,
        updated_at: string
    ) {
        this.id = id;
        this.file_name = file_name;
        this.path_source = path_source;
        this.user_id = user_id;
        this.created_at = created_at;
        this.updated_at = updated_at;
    }
}