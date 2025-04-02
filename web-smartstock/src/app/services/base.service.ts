import { HttpHeaders } from '@angular/common/http';

export class BaseService {
  protected defaultHeaders: HttpHeaders;

  constructor() {
    this.defaultHeaders = new HttpHeaders({
      'Content-Type': 'application/json',
      'x-token': 'internal_token',
    });
  }
}