import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';

import { environment } from '../../environments/environment';
import { BaseService } from "./base.service";
import { StoreDto } from "../dtos/store.dto";

@Injectable({
  providedIn: 'root',
})
export class StoreService extends BaseService {
  private apiStoreUrl = environment.storesUrl;

  constructor(private http: HttpClient) {
    super();
  }

  getStates(): Observable<string[]> {
    return this.http.get<string[]>(`${this.apiStoreUrl}/all-states`, {
      headers: this.defaultHeaders,
    });
  }

  getSecurityLevels(): Observable<string[]> {
    return this.http.get<string[]>(`${this.apiStoreUrl}/all-security-levels`, {
      headers: this.defaultHeaders,
    });
  }

  registerStore(store: any): Observable<StoreDto> {
    return this.http.post<any>(
      `${this.apiStoreUrl}/create`,
      store,
      { headers: this.defaultHeaders }
    );
  }
}