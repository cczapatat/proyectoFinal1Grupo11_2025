import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map, switchMap } from 'rxjs/operators';
import { UserSession } from '../user-session/user-session';
import { JwtHelperService } from '@auth0/angular-jwt';

import { environment } from '../../environments/environment';
import { Router } from '@angular/router';


@Injectable({
  providedIn: 'root',
})
export class SessionManager {
  private apiUserSessionUrl = environment.apiUserSessionUrl;

  private defaultHeaders = new HttpHeaders({
    'Content-Type': 'application/json',
    'x-token': 'internal_token',
  });

  // Variables para manejar la duración de la sesión y el temporizador de cierre de sesión.
  private duracionSesionMinutos: number = 30; //Duración de la sesión en minutos.
  private temporizadorCierreSesion: any;


  constructor(private http: HttpClient, private jwtHelper: JwtHelperService, private router: Router) {}

  // Método para iniciar sesión (llamada a la API)
  login(userSession: UserSession): Observable<any> {
    return this.http.post<any>(
      `${this.apiUserSessionUrl}/login`,
      { email: userSession.email, password: userSession.password },
      { headers: this.defaultHeaders }
    );
  }

  // Método para registrar un usuario (llamada a la API)
  registro(usuario: UserSession): Observable<UserSession> {
    return this.http.post<UserSession>(
      `${this.apiUserSessionUrl}/signin`,
      usuario,
      { headers: this.defaultHeaders }
    );
  }

  //Guarda el token y el tiempo de inicio de sesión en localStorage.
  guardarSesion(token: string, userId: string, type: string): void {
    localStorage.setItem('token', token);
    localStorage.setItem('loginTime', Date.now().toString());
    localStorage.setItem('userId', userId);
    localStorage.setItem('type', type);
    localStorage.setItem('decodedToken', this.jwtHelper.decodeToken(token));
    this.limpiarContadorSesion();
    this.iniciarContadorSesion();
  }

  // Recupera el token almacenado en localStorage.
  obtenerToken(): string | null {
    return localStorage.getItem('token');
  }

  // Recupera el tiempo de inicio de sesión almacenado.
  obtenerTiempoInicio(): number | null {
    const tiempo = localStorage.getItem('loginTime');
    return tiempo ? parseInt(tiempo, 10) : null;
  }

  esSesionActiva(): boolean {
    if (this.obtenerToken() !== null) {
      return true;
    }
    return false;
  }

// Verifica si la sesión es válida comprobando primero a nivel local y luego a nivel del servidor.
esSesionValida(): Observable<boolean> {
  const token = this.obtenerToken();
  if (!token) {
    return of(false);
  }

  // Si la validación local es correcta, se valida el token en el servidor.
  return this.validarToken();
}

// Valida el token usando el endpoint /auth.
validarToken(): Observable<boolean> {
  const token = this.obtenerToken();
  if (!token) {
    return of(false);
  }
  const urlAuth = `${this.apiUserSessionUrl}/auth`;
  const cabeceras = new HttpHeaders({
    'Content-Type': 'application/json',
    'x-token': 'internal_token',
    Authorization: `Bearer ${token}`,
  });
  return this.http.get<any>(urlAuth, { headers: cabeceras }).pipe(
    // Si el servidor responde exitosamente (200), se considera que el token es válido.
    map(() => true),
    catchError((error) => {
      console.error('Error al validar el token en el servidor:', error);
      this.cerrarSesion();
      return of(false);
    })
  );
}
  // Inicia un temporizador para cerrar la sesión automáticamente cuando expire.
  private iniciarContadorSesion(): void {
    const tiempoInicio = this.obtenerTiempoInicio();
    if (tiempoInicio) {
      const tiempoRestante = this.duracionSesion - (Date.now() - tiempoInicio);
      if (tiempoRestante > 0) {
        this.temporizadorCierreSesion = setTimeout(() => {
          console.warn('La sesión ha expirado. Cerrando sesión automáticamente.');
          this.cerrarSesion();
        }, tiempoRestante);
      } else {
        this.cerrarSesion();
      }
    }
  }

  // Limpia el temporizador de cierre de sesión si existe.
  private limpiarContadorSesion(): void {
    if (this.temporizadorCierreSesion) {
      clearTimeout(this.temporizadorCierreSesion);
      this.temporizadorCierreSesion = null;
    }
  }

  // Cierra la sesión: elimina el token y el tiempo de inicio del localStorage y limpia el temporizador.
  cerrarSesion(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('loginTime');
    localStorage.removeItem('userId');
    localStorage.removeItem('type');
    localStorage.removeItem('decodedToken');
    this.limpiarContadorSesion();

    this.router.navigate(['/user-sessions/login']);
  }

  //Cambia la duración de la sesión en minutos.
  private get duracionSesion(): number {
    return this.duracionSesionMinutos * 60 * 1000;
  }
}
