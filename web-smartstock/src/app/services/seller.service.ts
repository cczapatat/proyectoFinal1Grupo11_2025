import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseService } from './base.service';
import { Observable } from 'rxjs';
import { SellerDTO } from '../dtos/seller.dto';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class SellerService extends BaseService {

  private userManagerAPI = environment.apiUserSessionUrl;

  constructor(protected http: HttpClient) {
    super();
  }

  createSeller(seller: SellerDTO): Observable<any> {
    const createEndpoint = this.userManagerAPI + '/create';
    return this.http.post<any>(createEndpoint, seller, {
      headers: this.defaultHeaders,
    });
  }
}