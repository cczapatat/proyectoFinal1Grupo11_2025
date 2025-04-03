import { Injectable } from '@angular/core';
import {
  HttpInterceptor,
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpErrorResponse,
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

import { Router } from '@angular/router';
import { SessionManager } from '../services/session-manager.service';

@Injectable()
export class SessionInterceptorService implements HttpInterceptor {
  constructor(private sessionManager: SessionManager, private router: Router) {}

  intercept(
    req: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    // Si la sesión está activa, se realiza la validación.
    if (this.sessionManager.esSesionActiva) {
      if (!this.sessionManager.esSesionValida()) {
        this.sessionManager.closeSession();
        return throwError(() => new Error('Sesión expirada'));
      }

      // Si existe un token, se adjunta el header de autorización.
      const token = this.sessionManager.getToken();
      if (token) {
        req = req.clone({
          setHeaders: {
            Authorization: `Bearer ${token}`,
          },
        });
      }

      // Se maneja la respuesta y errores HTTP, por ejemplo, si se recibe un 401.
      return next.handle(req).pipe(
        catchError((error: HttpErrorResponse) => {
          if (error.status === 401) {
            this.sessionManager.closeSession();
            this.router.navigate(['/login']);
          }
          return throwError(() => error);
        })
      );
    } else {
      // Si la sesión no está activa, se continúa con la petición sin modificarla.
      return next.handle(req);
    }
  }
}