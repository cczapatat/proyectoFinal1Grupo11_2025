import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { BaseService } from './base.service';
import { Observable } from 'rxjs';
import { AssignedStockDto } from '../dtos/assignedStock';


@Injectable({
  providedIn: 'root'
})
export class StocksService extends BaseService  {

  private readonly stocksAPI = environment.apiStocksUrl;

  constructor(protected http: HttpClient) { 
    super();
  }

  getStocksByStore(storeId : string): Observable<AssignedStockDto> {
    const getAllClientsPag = `${this.stocksAPI}/stocks/by-store-id?id_store=${storeId}`;
    return this.http.get<AssignedStockDto>(getAllClientsPag,
      {
        headers: this.defaultHeaders
      });
  }

  assignStockToStore(assignedStock : AssignedStockDto): Observable<any> {
    const assignStock = `${this.stocksAPI}/stocks/assign-stock-store`;
    return this.http.put<any>(assignStock, assignedStock,
      {
        headers: this.defaultHeaders
      });
  }
}
