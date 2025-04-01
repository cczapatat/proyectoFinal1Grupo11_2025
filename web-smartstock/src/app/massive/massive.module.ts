import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { MassiveRoutingModule } from './massive-routing-module';
import { MassiveManufacturesComponent } from './massive-manufactures/massive-manufactures.component';
import { MassiveProductsCreateComponent } from './massive-products-create/massive-products-create.component';
import { MassiveProductEditComponent } from './massive-product-edit/massive-product-edit.component';

@NgModule({
  imports: [
    CommonModule,
    RouterModule,
    MassiveRoutingModule
  ],
  declarations: [
    MassiveManufacturesComponent,
    MassiveProductsCreateComponent,
    MassiveProductEditComponent
  ],
  exports: [
    MassiveManufacturesComponent,
    MassiveProductsCreateComponent,
    MassiveProductEditComponent
  ]
})
export class MassiveModule { }