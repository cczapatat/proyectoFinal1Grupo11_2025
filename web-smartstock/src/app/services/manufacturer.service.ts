import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Manufacturer, ManufacturerPaginateDTO } from '../dtos/manufacturer';
import { BulkTask } from '../dtos/bulk-task';

@Injectable({
  providedIn: 'root'
})
export class ManufacturerService {

  private apiManufactureUrl = environment.apiManufacturerUrl;

  constructor(
    private http: HttpClient
  ) { }

  getManufacturerList(): Observable<Manufacturer[]> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
      'x-token': environment.xToken
    })
    return this.http.get<Manufacturer[]>(`${this.apiManufactureUrl}/manufacturers/all`, { headers: headers })
  }

  createMassiveManufacturers(fileId: string): Observable<BulkTask> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
      'x-token': environment.xToken
    })
    return this.http.post<BulkTask>(`${this.apiManufactureUrl}/manufacturers/massive/create`,
      {
        file_id: fileId
      },
      { headers: headers }
    )
  }

  getManufacturersByList(page: number, perPage: number): Observable<ManufacturerPaginateDTO> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${sessionStorage.getItem('token')}`,
      'x-token': environment.xToken
    })
    return this.http.get<ManufacturerPaginateDTO>(
      `${this.apiManufactureUrl}/manufacturers/list?page=${page}&per_page=${perPage}`,
      { headers: headers },
    )
  }
}
