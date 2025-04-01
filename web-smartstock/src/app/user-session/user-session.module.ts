import { ReactiveFormsModule } from '@angular/forms';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserSessionLoginComponent } from './user-session-login/user-session-login.component';
import { UserSessionSignUpComponent } from './user-session-sign-up/user-session-sign-up.component';
import { UserRoutingModule } from './user-session-routing-module';

@NgModule({
  imports: [
    CommonModule, 
    ReactiveFormsModule,
    UserRoutingModule
  ],
  exports: [UserSessionLoginComponent, UserSessionSignUpComponent],
  declarations: [UserSessionLoginComponent, UserSessionSignUpComponent]

})

export class UserSessionModule { }
