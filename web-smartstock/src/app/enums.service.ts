import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Banco, CategoriaMovimiento, EstadoMantenimiento, TipoMantenimiento, TipoMovimiento } from './enums';

@Injectable({
  providedIn: 'root'
})
export class EnumsService {

  private apiUrl = environment.apiUserSessionUrl;

  constructor(private http: HttpClient) { }

  bancos(): Observable<Banco[]> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    })
    return this.http.get<Banco[]>(`${this.apiUrl}/bancos`, { headers: headers });
  }

  tiposMovimiento(): Observable<TipoMovimiento[]> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    })
    return this.http.get<Banco[]>(`${this.apiUrl}/tipo-movimientos`, { headers: headers });
  }

  categoriaMovimiento(): Observable<CategoriaMovimiento[]> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    })
    return this.http.get<CategoriaMovimiento[]>(`${this.apiUrl}/categoria-movimientos`, { headers: headers });
  }

  obtenerTiposMantenimiento(): Observable<TipoMantenimiento[]> {
    return this.http.get<TipoMantenimiento[]>(`${this.apiUrl}/tipo-mantenimientos`, {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      }),
    });
  }

  obtenerEstadosMantenimiento(): Observable<EstadoMantenimiento[]> {
    return this.http.get<EstadoMantenimiento[]>(`${this.apiUrl}/estado-mantenimientos`, {
      headers: new HttpHeaders({
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      }),
    });
  }
}
