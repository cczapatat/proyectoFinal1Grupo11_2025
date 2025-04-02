import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { environment } from '../../environments/environment'
import { Product } from './product';
import { ProductCategory } from './product-category';
import { ProductCurrency } from './product-currency';

@Injectable({
  providedIn: 'root'
})
export class ProductService {

  private apiProductUrl = environment.apiProductUrl;

  constructor(
    private http: HttpClient
  ) { }

  createProduct(product: Product): Observable<Product> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
      'x-token': environment.xToken
    })
    return this.http.post<Product>(`${this.apiProductUrl}/create`, product, { headers: headers })
  }

  getProductCategories(): Observable<ProductCategory[]> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
      'x-token': environment.xToken
    })
    return this.http.get<ProductCategory[]>(`${this.apiProductUrl}/categories`, { headers: headers })
  }

  getProductCurrencies(): Observable<ProductCurrency[]> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
      'x-token': environment.xToken
    })
    return this.http.get<ProductCurrency[]>(`${this.apiProductUrl}/currencies`, { headers: headers })
  }
}
