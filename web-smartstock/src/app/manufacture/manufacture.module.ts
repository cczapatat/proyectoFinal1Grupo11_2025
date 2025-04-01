import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { ManufactureRoutingModule } from './manufacture-routing-module';
import { ManufactureListProductsComponent } from './manufacture-list-products/manufacture-list-products.component';

@NgModule({
  imports: [
    CommonModule,
    RouterModule,
    ManufactureRoutingModule
  ],
  declarations: [
    ManufactureListProductsComponent,
  ],
  exports: [
    ManufactureListProductsComponent,
  ]
})
export class ManufactureModule { }
