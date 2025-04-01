import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { OrderRoutingModule } from './order-routing-module';
import { OrderCreateComponent } from './order-create/order-create.component';

@NgModule({
  imports: [
    CommonModule,
    RouterModule,
    OrderRoutingModule
  ],
  declarations: [
    OrderCreateComponent,
  ],
  exports: [
    OrderCreateComponent,
  ]
})
export class OrderModule { }
