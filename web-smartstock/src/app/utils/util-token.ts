export class UtilAToken {
  public static isAdmin(): boolean {
    const type = localStorage.getItem('type');
    const isAdmin = type === 'ADMIN';

    return isAdmin;
  }

  public static getUserId(): string | null {
    const userId = localStorage.getItem('userId');
    return userId;
  }

  public static getToken(): string {
    const token = localStorage.getItem('token');
    return token;
  }
}
