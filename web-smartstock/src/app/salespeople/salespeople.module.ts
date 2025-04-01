import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { SalespeopleRoutingModule } from './salespeople-routing-module';
import { SalespeopleAssignCustomersComponent } from './salespeople-assign-customers/salespeople-assign-customers.component';
import { SalespeopleRegisterComponent } from './salespeople-register/salespeople-register.component';
import { SalespeopleListCustomersComponent } from './salespeople-list-customers/salespeople-list-customers.component';

@NgModule({
  imports: [
    CommonModule,
    RouterModule,
    SalespeopleRoutingModule
  ],
  declarations: [
    SalespeopleAssignCustomersComponent,
    SalespeopleRegisterComponent,
    SalespeopleListCustomersComponent
  ],
  exports: [
    SalespeopleAssignCustomersComponent,
    SalespeopleRegisterComponent,
    SalespeopleListCustomersComponent
  ]
})
export class SalespeopleModule { }