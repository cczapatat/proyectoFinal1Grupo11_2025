import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { StoreRoutingModule } from './store-routing-module';
import { StoreRegisterComponent } from './store-register/store-register.component';
import { StoreAssignProductComponent } from './store-assign-product/store-assign-product.component';

@NgModule({
  imports: [
    CommonModule,
    RouterModule,
    StoreRoutingModule
  ],
  declarations: [
    StoreRegisterComponent,
    StoreAssignProductComponent
  ],
  exports: [
    StoreRegisterComponent,
    StoreAssignProductComponent
  ]
})
export class StoreModule { }
