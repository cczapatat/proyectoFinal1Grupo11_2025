// src/app/guards/auth.guard.ts
import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { Observable, of } from 'rxjs';
import { SessionManager } from '../services/session-manager.service';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  constructor(private sessionManager: SessionManager, private router: Router) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<boolean> {
    //Verifica si la sesión está activa y si es válida.
    if (!this.sessionManager.esSesionActiva()) {
      this.router.navigate(['/user-sessions/login']);
      return of(false);
    }
  
    return this.sessionManager.esSesionValida().pipe(
      tap((valid) => {
        if (!valid) {
          this.router.navigate(['/user-sessions/login']);
        }
      })
    );
  }
}