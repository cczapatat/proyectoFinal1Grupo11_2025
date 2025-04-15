import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseService } from './base.service';
import { Observable } from 'rxjs';
import { ClientDTO } from '../dtos/client.dto';
import { AssociateSeller, PaginatedClients } from '../dtos/client';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ClientService extends BaseService {

  private readonly clientApi = environment.apiClientUrl;
  private readonly userManagerAPI = environment.apiUserSessionUrl;

  constructor(protected http: HttpClient) {
    super();
  }

  getClientsBySellerId(clientId: string, page: number = 1, perPage: number = 10, sortBy: string = 'name', sortOrder: string = 'asc'): Observable<PaginatedClients> {
    const getAllClientsPag = `${this.userManagerAPI}/clients/seller/${clientId}?page=${page}&per_page=${perPage}&sort_by=${sortBy}&sort_order=${sortOrder}`;
    return this.http.get<PaginatedClients>(getAllClientsPag,
      {
        headers: this.defaultHeaders
      });
  }

  getClientsBySellerIdList(sellerId: string): Observable<ClientDTO[]> {
    return this.http.get<ClientDTO[]>(`${this.clientApi}/seller/${sellerId}`, {
      headers: this.defaultHeaders,
    });
  }

  getAllClients(page: number = 1, perPage: number = 10, sortBy: string = 'name', sortOrder: string = 'asc'): Observable<PaginatedClients> {
    const getAllClientsPag = `${this.userManagerAPI}/clients/pag?page=${page}&per_page=${perPage}&sort_by=${sortBy}&sort_order=${sortOrder}`;
    return this.http.get<PaginatedClients>(getAllClientsPag,
      {
        headers: this.defaultHeaders
      });
  }
  saveAssociationSellerClients(association: AssociateSeller, page: number = 1, perPage: number = 10, sortBy: string = 'name', sortOrder: string = 'asc'){
    const associateSeller = `${this.userManagerAPI}/clients/associate_seller?page=${page}&per_page=${perPage}&sort_by=${sortBy}&sort_order=${sortOrder}`;
    return this.http.post<PaginatedClients>(associateSeller, association, 
      {
        headers: this.defaultHeaders
      });
  }
}
