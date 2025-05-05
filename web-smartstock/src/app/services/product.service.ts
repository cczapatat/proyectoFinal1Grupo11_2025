import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment'
import { Product } from '../product/product';
import { BulkTask } from '../dtos/bulk-task';
import { ProductCategory } from '../dtos/product-category';
import { ProductCurrency } from '../dtos/product-currency';
import { PaginatedProducts } from '../dtos/product';

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

  createMassiveProducts(fileId: string): Observable<BulkTask> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
      'x-token': environment.xToken
    })
    return this.http.post<BulkTask>(`${this.apiProductUrl}/massive/create`,
      {
        file_id: fileId
      },
      { headers: headers }
    )
  }

  updateMassiveProducts(fileId: string): Observable<BulkTask> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
      'x-token': environment.xToken
    })
    return this.http.put<BulkTask>(`${this.apiProductUrl}/massive/update`,
      {
        file_id: fileId
      },
      { headers: headers }
    )
  }

  getProductById(id: string): Observable<Product> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
      'x-token': environment.xToken
    })
    return this.http.get<Product>(`${this.apiProductUrl}/get/${id}`, { headers: headers })
  }

  updateProduct(productId: string, product: Product): Observable<Product> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
      'x-token': environment.xToken
    })
    return this.http.put<Product>(`${this.apiProductUrl}/update/${productId}`, product, { headers: headers })
  }

  getProducts(): Observable<Product[]> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
      'x-token': environment.xToken
    })
    return this.http.get<Product[]>(`${this.apiProductUrl}/list?all=true`, { headers: headers })
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

  getProductsPaginated(page: number = 1, perPage: number = 10, sortOrder: string = 'asc'): Observable<PaginatedProducts> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
      'x-token': environment.xToken
    })
    return this.http.get<PaginatedProducts>(`${this.apiProductUrl}/paginated_full?page=${page}&per_page=${perPage}&sort_order=${sortOrder}`, { headers: headers })
  }

}

