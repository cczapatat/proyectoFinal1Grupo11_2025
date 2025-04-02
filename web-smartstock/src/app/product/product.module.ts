import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProductCreateComponent } from './product-create/product-create.component';
import { ProductEditComponent } from './product-edit/product-edit.component';
import { ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { ProductRoutingModule } from './product-routing-module';

@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule,
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