import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SalespeopleAssignCustomersComponent } from './salespeople-assign-customers/salespeople-assign-customers.component';
import { SalesPeopleRegisterComponent } from './salespeople-register/salespeople-register.component';
import { SalespeopleListCustomersComponent } from './salespeople-list-customers/salespeople-list-customers.component';
import { JWT_OPTIONS, JwtHelperService } from '@auth0/angular-jwt';
import { ReactiveFormsModule } from '@angular/forms';
import { UserRoutingModule } from '../user-session/user-session-routing-module';
import { TranslateModule } from '@ngx-translate/core';

@NgModule({
  imports: [
    CommonModule, 
    ReactiveFormsModule,
    UserRoutingModule,
    TranslateModule
  ],
  declarations: [
    SalespeopleAssignCustomersComponent,
    SalesPeopleRegisterComponent,
    SalespeopleListCustomersComponent
  ],
  exports: [
    SalespeopleAssignCustomersComponent,
    SalesPeopleRegisterComponent,
    SalespeopleListCustomersComponent
  ],
  providers: [
    { provide: JWT_OPTIONS, useValue: {} },  
    JwtHelperService,
  ],
})
export class SalesPeopleModule { }