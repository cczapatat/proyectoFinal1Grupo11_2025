export class UtilAToken {
  public static isAdmin(): boolean {
    const type = localStorage.getItem('type');
    const isAdmin = type === 'ADMIN';

    return isAdmin;
  }

  public static getEntityId(): string | null {
    const userId = localStorage.getItem('entity_id');
    return userId;
  }

  public static getToken(): string {
    const token = localStorage.getItem('token');
    return token;
  }
}
