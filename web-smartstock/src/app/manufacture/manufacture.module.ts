import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
import { ReactiveFormsModule } from '@angular/forms';

import { ManufactureRoutingModule } from './manufacture-routing-module';
import { ManufactureListProductsComponent } from './manufacture-list-products/manufacture-list-products.component';

@NgModule({
  imports: [
    CommonModule,
    RouterModule,
    ReactiveFormsModule,
    ManufactureRoutingModule,
    TranslateModule,
  ],
  declarations: [
    ManufactureListProductsComponent,
  ],
  exports: [
    ManufactureListProductsComponent,
  ]
})
export class ManufactureModule { }
