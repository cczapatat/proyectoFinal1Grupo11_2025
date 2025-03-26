export class UserSession {
    email: string;
    password: string;
    type: string;

    public constructor(email: string, password:string, type:string = "") {
        this.email = email
        this.password = password
        this.type = type
    }
}
