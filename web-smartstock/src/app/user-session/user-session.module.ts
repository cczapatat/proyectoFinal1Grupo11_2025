import { ReactiveFormsModule } from '@angular/forms';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserSessionSignUpComponent } from './user-session-sign-up/user-session-sign-up.component';
import { UserRoutingModule } from './user-session-routing-module';

import { JWT_OPTIONS, JwtHelperService } from '@auth0/angular-jwt';
import { UserSessionLoginComponent } from './user-session-login/user-session-login.component';

@NgModule({
  imports: [
    CommonModule, 
    ReactiveFormsModule,
    UserRoutingModule
  ],
  exports: [UserSessionLoginComponent, UserSessionSignUpComponent],
  declarations: [UserSessionLoginComponent, UserSessionSignUpComponent],
  providers: [
    { provide: JWT_OPTIONS, useValue: {} },  
    JwtHelperService,
  ],
})
export class UserSessionModule { }