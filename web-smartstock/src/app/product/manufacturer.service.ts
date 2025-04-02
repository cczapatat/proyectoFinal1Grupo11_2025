import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Manufacturer } from './manufacturer';

@Injectable({
  providedIn: 'root'
})
export class ManufacturerService {

  private apiManufactuerUrl = environment.apiManufacturerUrl;

  constructor(
    private http: HttpClient
  ) { }

  getManufacturerList(): Observable<Manufacturer[]> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
      'x-token': environment.xToken
    })
    return this.http.get<Manufacturer[]>(`${this.apiManufactuerUrl}/manufacturers/all`, { headers: headers })
  }

}
