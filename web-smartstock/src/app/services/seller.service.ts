import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseService } from './base.service';
import { Observable } from 'rxjs';
import { SellerDTO, PaginatedSellers } from '../dtos/seller.dto';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class SellerService extends BaseService {

  private readonly userManagerAPI = environment.apiUserSessionUrl;

  constructor(protected http: HttpClient) {
    super();
  }

  createSeller(seller: SellerDTO): Observable<any> {
    const createEndpoint = this.userManagerAPI + '/create';
    return this.http.post<any>(createEndpoint, seller, {
      headers: this.defaultHeaders,
    });
  }

  getSellersPaginated(page: number = 1, perPage: number = 10, sortBy: string = 'name', sortOrder: string = 'asc'): Observable<PaginatedSellers> {
    const getAllSellerPag = `${this.userManagerAPI}/sellers/pag?page=${page}&per_page=${perPage}&sort_by=${sortBy}&sort_order=${sortOrder}`;
    return this.http.get<PaginatedSellers>(getAllSellerPag);
  }


}