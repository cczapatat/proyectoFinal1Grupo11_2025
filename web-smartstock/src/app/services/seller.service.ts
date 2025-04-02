import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseService } from './base.service';
import { Observable } from 'rxjs';
import { SellerDTO } from '../dtos/seller.dto';

@Injectable({
  providedIn: 'root'
})
export class SellerService extends BaseService {

  private sellerEndpoint = '{{server-user_session_manager}}/user_sessions/create';

  constructor(protected http: HttpClient) {
    super();
  }

  createSeller(seller: SellerDTO): Observable<any> {
    return this.http.post<any>(this.sellerEndpoint, seller);
  }
}