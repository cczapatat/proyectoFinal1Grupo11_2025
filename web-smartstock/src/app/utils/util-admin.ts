export class UtilAdmin {
  public static isAdmin(): boolean {
    const type = localStorage.getItem('type');
    const isAdmin = type === 'ADMIN';

    return isAdmin;
  }

  public static getUserId(): string | null {
    const userId = localStorage.getItem('userId');
    return userId;
  }
}
