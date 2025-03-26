import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { UserSession } from './user-session';

import { environment } from '../../environments/environment'

@Injectable({
  providedIn: 'root'
})
export class UserSessionService {
  private apiUserSessionUrl = environment.apiUserSessionUrl;

  private defaultHeaders = new HttpHeaders({
    'Content-Type': 'application/json',
    'x-token': 'internal_token'
  });

  constructor(private http: HttpClient) { }

  login(userSession: UserSession): Observable<any> {
    return this.http.post<any>(
      `${this.apiUserSessionUrl}/login`,
      { "email": userSession.email, "password": userSession.password },
      { headers: this.defaultHeaders },
    );
  }

  registro(usuario: UserSession): Observable<UserSession> {
    return this.http.post<UserSession>(
      `${this.apiUserSessionUrl}/signin`,
      usuario,
      { headers: this.defaultHeaders },
    )
  }
}
