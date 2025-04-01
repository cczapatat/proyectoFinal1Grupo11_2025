import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { ProductRoutingModule } from './product-routing-module';
import { ProductCreateComponent } from './product-create/product-create.component';
import { ProductEditComponent } from './product-edit/product-edit.component';

@NgModule({
  imports: [
    CommonModule,
    RouterModule,
    ProductRoutingModule
  ],
  declarations: [
    ProductCreateComponent,
    ProductEditComponent
  ],
  exports: [
    ProductCreateComponent,
    ProductEditComponent
  ]
})
export class ProductModule { }
