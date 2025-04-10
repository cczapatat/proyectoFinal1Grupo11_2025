import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseService } from './base.service';
import { Observable } from 'rxjs';
import { ClientDTO } from '../dtos/client.dto';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ClientService extends BaseService {

  private clientApi = environment.clientUrl;

  constructor(protected http: HttpClient) {
    super();
  }

  getClientsBySellerId(sellerId: string): Observable<ClientDTO[]> {
    return this.http.get<ClientDTO[]>(`${this.clientApi}/seller/${sellerId}`, {
      headers: this.defaultHeaders,
    });
  }
}