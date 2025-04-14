import { Injectable } from "@angular/core";
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';
import { BaseService } from "./base.service";
import { PaginatedStores, StoreDto } from "../dtos/store.dto";

@Injectable({
  providedIn: 'root',
})
export class StoreService extends BaseService {
  private apiStoreUrl = environment.apiStoresUrl;

  constructor(private http: HttpClient) {
    super();
  }

  getPaginatedStores(page: number = 1, perPage: number = 10, sortOrder: string = 'asc'): Observable<PaginatedStores> {
    const paginatedStores = `${this.apiStoreUrl}/paginated_full?page=${page}&per_page=${perPage}&sort_order=${sortOrder}`;
    return this.http.get<PaginatedStores>(paginatedStores,
      {
        headers: this.defaultHeaders
      });
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