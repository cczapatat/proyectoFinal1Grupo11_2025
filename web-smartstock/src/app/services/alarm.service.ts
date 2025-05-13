import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment'
import { Alarm } from '../alarm/alarm';
import { UtilAToken } from '../utils/util-token';
import { BaseService } from './base.service';

@Injectable({
  providedIn: 'root'
})
export class AlarmService extends BaseService {

  private apiAlarmUrl = environment.apiAlarmUrl;

  constructor(private http: HttpClient) {
    super();
  }

  createAlarm(alarm: any): Observable<Alarm> {
    const headers = this.defaultHeaders;
    headers.append('Authorization', `Bearer ${UtilAToken.getToken()}`);

    console.log('Payload de alarma:', alarm);
    
    return this.http.post<Alarm>(`${this.apiAlarmUrl}/new`, alarm, { headers: headers })
  }

}

