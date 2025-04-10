import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseService } from './base.service';
import { Observable } from 'rxjs';
import { ProductStockDTO } from '../dtos/stock.dto';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class StockService extends BaseService {

  private stockApi = environment.stockUrl;

  constructor(protected http: HttpClient) {
    super();
  }

  getProductsOnStock(page: number, perPage: number): Observable<ProductStockDTO[]> {
    return this.http.get<ProductStockDTO[]>(`${this.stockApi}/stocks/all?page=${page}&per_page=${perPage}`, {
      headers: this.defaultHeaders,
    });
  }
}