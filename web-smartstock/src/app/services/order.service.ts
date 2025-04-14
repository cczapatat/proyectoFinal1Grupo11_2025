import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';
import { BaseService } from './base.service';
import { OrderCreateDTO, OrderCreatedDTO } from '../dtos/order.dto';
import { UtilAToken } from 'src/app/utils/util-token';

@Injectable({
  providedIn: 'root',
})
export class OrderService extends BaseService {
  private orderApi = environment.apiOrderUrl;

  constructor(private http: HttpClient) {
    super();
  }

  getPaymentMethods(): Observable<string[]> {
    return this.http.get<string[]>(`${this.orderApi}/all-payment-methods`, {
      headers: this.defaultHeaders,
    });
  }

  createOrder(order: OrderCreateDTO): Observable<OrderCreatedDTO> {
    const headers = this.defaultHeaders;
    headers.append('Authorization', `Bearer ${UtilAToken.getToken()}`);
    return this.http.post<OrderCreatedDTO>(`${this.orderApi}/create`, order, {
      headers: headers,
    });
  }
}