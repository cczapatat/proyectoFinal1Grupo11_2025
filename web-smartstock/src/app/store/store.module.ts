import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { TranslateModule } from '@ngx-translate/core';

import { StoreRoutingModule } from './store-routing-module';
import { StoreRegisterComponent } from './store-register/store-register.component';
import { StoreAssignProductComponent } from './store-assign-product/store-assign-product.component';

@NgModule({
  imports: [
    CommonModule,
    RouterModule,
    ReactiveFormsModule,
    TranslateModule,
    StoreRoutingModule,
    FormsModule
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
