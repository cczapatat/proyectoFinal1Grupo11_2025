import { ReactiveFormsModule } from '@angular/forms';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserSesionLoginComponent } from './user-session-login/user-session-login.component';
import { UserSessionSignUpComponent } from './user-session-sign-up/user-session-sign-up.component';
import { UsuarioRoutingModule } from './user-session-routing-module';
import { JWT_OPTIONS, JwtHelperService } from '@auth0/angular-jwt';

@NgModule({
  imports: [
    CommonModule, 
    ReactiveFormsModule,
    UsuarioRoutingModule
  ],
  exports: [UserSesionLoginComponent, UserSessionSignUpComponent],
  declarations: [UserSesionLoginComponent, UserSessionSignUpComponent],
  providers: [
    { provide: JWT_OPTIONS, useValue: {} },  
    JwtHelperService,
  ],
})
export class UserSessionModule { }