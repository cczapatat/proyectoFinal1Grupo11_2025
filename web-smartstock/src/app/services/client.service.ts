import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { BaseService } from './base.service';
import { Observable } from 'rxjs';
import { PaginatedClients } from '../dtos/client';

@Injectable({
  providedIn: 'root'
})
export class ClientService extends BaseService  {

  private readonly userManagerAPI = environment.apiUserSessionUrl;

  constructor(protected http: HttpClient) { 
    super();
  }

  getClientsBySellerId(clientId: string, page: number = 1, perPage: number = 10, sortBy: string = 'name', sortOrder: string = 'asc'): Observable<PaginatedClients> {
    const getAllClientsPag = `${this.userManagerAPI}/clients/seller/${clientId}?page=${page}&per_page=${perPage}&sort_by=${sortBy}&sort_order=${sortOrder}`;
    return this.http.get<PaginatedClients>(getAllClientsPag);
  }
}
