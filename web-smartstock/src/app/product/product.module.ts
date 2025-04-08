import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProductCreateComponent } from './product-create/product-create.component';
import { ProductEditComponent } from './product-edit/product-edit.component';
import { ReactiveFormsModule } from '@angular/forms';
import { TranslateModule } from '@ngx-translate/core';
import { RouterModule } from '@angular/router';
import { ProductRoutingModule } from './product-routing-module';
import { Product } from './product';
import { ProductListComponent } from './product-list/product-list.component';

@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule,
    TranslateModule,
    RouterModule,
    ProductRoutingModule
  ],
  declarations: [
    ProductCreateComponent,
    ProductEditComponent,
    ProductListComponent
  ],
  exports: [
    ProductCreateComponent,
    ProductEditComponent,
    ProductListComponent
  ]
})
export class ProductModule { }